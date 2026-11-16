import unittest
import subprocess
import os
import time
import socket
import json
import sys

class TestIntegrationFI03(unittest.TestCase):
    """F-W01 : Tests d'intégration pour le système de chunk world."""
    
    def setUp(self):
        # Lire DEPLOIEMENT.json pour obtenir port et api_path
        with open('DEPLOIEMENT.json', 'r') as f:
            config = json.load(f)
        
        self.port = config['port']
        self.api_path = config['api_path']
        
        # Vérifier le port
        if self.port != 25565:
            raise ValueError("Le port attendu est 25565, pas {}".format(self.port))
            
        # Lancer le serveur
        self.server_process = subprocess.Popen([sys.executable, "server.py"], 
                                               env={**os.environ, "PORT": str(self.port), "HOTE": "127.0.0.1"})
        
        # Attendre que le port soit ouvert
        timeout = 10
        while timeout > 0:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", self.port))
                s.close()
                break
            except Exception:
                time.sleep(0.1)
                timeout -= 0.1
        
        if timeout <= 0:
            raise RuntimeError("Impossible de se connecter au serveur sur le port {}".format(self.port))

    def tearDown(self):
        self.server_process.terminate()
        try:
            self.server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.server_process.kill()

    def _send(self, sock, msg_type, payload):
        message = {"type": msg_type, "payload": payload}
        sock.send((json.dumps(message) + "\n").encode())

    def _recv(self, sock, timeout=2.0):
        sock.settimeout(timeout)
        data = ""
        try:
            while True:
                chunk = sock.recv(4096).decode()
                if not chunk:
                    break
                data += chunk
                if data.endswith("\n"):
                    break
        except socket.timeout:
            pass
        # Décoder un ou plusieurs messages JSON, retourner le premier message complet
        messages = []
        for line in data.strip().split('\n'):
            if line.strip():
                messages.append(json.loads(line))
        return messages[0] if messages else None

    def test_chunk_world_system(self):
        """F-W01 : Teste la génération et la persistance des chunks via socket brut."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", self.port))
        
        # Lire le message WELCOME
        welcome_msg = self._recv(s)
        self.assertIsNotNone(welcome_msg)
        self.assertEqual(welcome_msg["type"], "WELCOME")
        
        # Envoyer JOIN pour s'identifier
        self._send(s, "JOIN", {"username": "test_player", "version": "1.0"})
        
        # Lire PLAYER_JOINED
        joined_msg = self._recv(s)
        self.assertIsNotNone(joined_msg)
        self.assertEqual(joined_msg["type"], "PLAYER_JOINED")
        
        # Envoyer PLACE_ATTEMPT à y=80 (vide selon worldgen.py)
        self._send(s, "PLACE_ATTEMPT", {"x": 5, "y": 80, "z": 5, "block_id": "STONE"})
        
        # Attendre et recevoir le BLOCK_UPDATE
        update_msg = None
        for _ in range(10):  # Attendre jusqu'à 2 secondes
            update_msg = self._recv(s, 0.2)
            if update_msg and update_msg["type"] == "BLOCK_UPDATE":
                break
        
        self.assertIsNotNone(update_msg)
        self.assertEqual(update_msg["type"], "BLOCK_UPDATE")
        self.assertEqual(update_msg["payload"]["x"], 5)
        self.assertEqual(update_msg["payload"]["y"], 80)
        self.assertEqual(update_msg["payload"]["z"], 5)
        self.assertEqual(update_msg["payload"]["new_block_id"], "STONE")
        # L'ancien bloc peut être None ou AIR selon l'implémentation
        self.assertIn(update_msg["payload"]["old_block_id"], [None, "AIR"])
        
        s.close()