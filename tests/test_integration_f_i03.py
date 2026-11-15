import unittest
import subprocess
import os
import time
import socket
import json

class TestIntegrationFI03(unittest.TestCase):
    def setUp(self):
        # Obtenir un port libre
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 0))
        sock.listen(1)
        port = sock.getsockname()[1]
        sock.close()
        
        # Lancer le serveur
        self.server_process = subprocess.Popen([os.sys.executable, "server.py"], env={**os.environ, "PORT": str(port), "HOTE": "127.0.0.1"})
        
        # Attendre que le port soit ouvert
        timeout = 10
        while timeout > 0:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", port))
                s.close()
                break
            except Exception:
                time.sleep(0.1)
                timeout -= 0.1
        
        self.port = port

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
        # Décoder un ou plusieurs messages JSON
        messages = []
        for line in data.strip().split('\n'):
            if line.strip():
                messages.append(json.loads(line))
        return messages[0] if messages else None

    def test_place_attempt_valid_emits_block_update(self):
        """F-I03 : placement valide déclenche un BLOCK_UPDATE confirmé."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", self.port))
        
        # Lire le message WELCOME
        welcome_msg = self._recv(s)
        self.assertIsNotNone(welcome_msg)
        self.assertEqual(welcome_msg["type"], "WELCOME")
        
        # Envoyer JOIN
        self._send(s, "JOIN", {"username": "test_player", "version": "1.0"})
        
        # Lire PLAYER_JOINED
        joined_msg = self._recv(s)
        self.assertIsNotNone(joined_msg)
        self.assertEqual(joined_msg["type"], "PLAYER_JOINED")
        
        # Envoyer PLACE_ATTEMPT
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

    def test_place_attempt_out_of_bounds_rejected(self):
        """F-I03 : placement hors limites est rejeté."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", self.port))
        
        # Lire le message WELCOME
        welcome_msg = self._recv(s)
        self.assertIsNotNone(welcome_msg)
        self.assertEqual(welcome_msg["type"], "WELCOME")
        
        # Envoyer JOIN
        self._send(s, "JOIN", {"username": "test_player", "version": "1.0"})
        
        # Lire PLAYER_JOINED
        joined_msg = self._recv(s)
        self.assertIsNotNone(joined_msg)
        self.assertEqual(joined_msg["type"], "PLAYER_JOINED")
        
        # Envoyer PLACE_ATTEMPT hors limites
        self._send(s, "PLACE_ATTEMPT", {"x": 0, "y": 999, "z": 0, "block_id": "STONE"})
        
        # Vérifier qu'aucun BLOCK_UPDATE avec y=999 n'est reçu dans 1 seconde
        update_msg = self._recv(s, 1.0)
        if update_msg:
            self.assertNotEqual(update_msg["payload"]["y"], 999)
        
        s.close()

    def test_place_attempt_on_occupied_block_rejected(self):
        """F-I03 : placement sur un bloc déjà occupé est rejeté."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", self.port))
        
        # Lire le message WELCOME
        welcome_msg = self._recv(s)
        self.assertIsNotNone(welcome_msg)
        self.assertEqual(welcome_msg["type"], "WELCOME")
        
        # Envoyer JOIN
        self._send(s, "JOIN", {"username": "test_player", "version": "1.0"})
        
        # Lire PLAYER_JOINED
        joined_msg = self._recv(s)
        self.assertIsNotNone(joined_msg)
        self.assertEqual(joined_msg["type"], "PLAYER_JOINED")
        
        # Placer un bloc à (5, 80, 5)
        self._send(s, "PLACE_ATTEMPT", {"x": 5, "y": 80, "z": 5, "block_id": "STONE"})
        
        # Lire le BLOCK_UPDATE
        update_msg = None
        for _ in range(10):  # Attendre jusqu'à 2 secondes
            update_msg = self._recv(s, 0.2)
            if update_msg and update_msg["type"] == "BLOCK_UPDATE":
                break
        
        self.assertIsNotNone(update_msg)
        
        # Envoyer un nouveau PLACE_ATTEMPT sur le même emplacement (devrait être rejeté)
        self._send(s, "PLACE_ATTEMPT", {"x": 5, "y": 80, "z": 5, "block_id": "DIRT"})
        
        # Vérifier qu'aucun BLOCK_UPDATE avec new_block_id="DIRT" n'est reçu dans 1 seconde
        update_msg = self._recv(s, 1.0)
        if update_msg:
            self.assertNotEqual(update_msg["payload"]["new_block_id"], "DIRT")
        
        s.close()

    def test_place_attempt_unknown_block_rejected(self):
        """F-I03 : placement d'un block_id inconnu est rejeté."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", self.port))
        
        # Lire le message WELCOME
        welcome_msg = self._recv(s)
        self.assertIsNotNone(welcome_msg)
        self.assertEqual(welcome_msg["type"], "WELCOME")
        
        # Envoyer JOIN
        self._send(s, "JOIN", {"username": "test_player", "version": "1.0"})
        
        # Lire PLAYER_JOINED
        joined_msg = self._recv(s)
        self.assertIsNotNone(joined_msg)
        self.assertEqual(joined_msg["type"], "PLAYER_JOINED")
        
        # Envoyer un PLACE_ATTEMPT avec block_id inconnu
        self._send(s, "PLACE_ATTEMPT", {"x": 5, "y": 80, "z": 5, "block_id": "LAVE"})
        
        # Vérifier qu'aucun BLOCK_UPDATE avec new_block_id="LAVE" n'est reçu dans 1 seconde
        update_msg = self._recv(s, 1.0)
        if update_msg:
            self.assertNotEqual(update_msg["payload"]["new_block_id"], "LAVE")
        
        s.close()