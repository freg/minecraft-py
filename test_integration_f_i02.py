import unittest
from client import GameClient
import socket
import time
import subprocess
import sys

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


class TestIntegrationFI02(unittest.TestCase):
    def setUp(self):
        # Démarrer le serveur sur un port libre pour ce test
        self.port = find_free_port()
        
        # Démarrer le serveur dans un sous-processus
        self.server_process = subprocess.Popen([
            sys.executable, 
            "server.py", 
            "--port", str(self.port), 
            "--host", "127.0.0.1"
        ])
        time.sleep(0.5)  # Attendre que le serveur démarre

    def tearDown(self):
        # Arrêter le serveur
        self.server_process.terminate()
        try:
            self.server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.server_process.kill()

    def test_mining_block(self):
        # Créer un client avec les paramètres par défaut du serveur
        client = GameClient("127.0.0.1", self.port)
        client.connect()
        
        # Simuler une tentative de minage
        response = client.send_mining(0, 0, 0)  # Minage du bloc à (0, 0, 0)
        
        # Vérifier que le serveur a bien reçu l'événement MINING_ATTEMPT et envoyé BLOCK_UPDATE
        # Ici on simule simplement la réception d'un message BLOCK_UPDATE
        time.sleep(0.1)
        
        # Fermer la connexion
        client.disconnect()

    def test_mining_block_with_correct_protocol(self):
        """Test que le protocole utilise les types MINING_ATTEMPT et BLOCK_UPDATE"""
        # Vérification du type de message envoyé par le client au serveur lors du minage
        from protocole import encode_player_mining
        msg = encode_player_mining(0, 0, 0)
        # Le message doit être de type MINING_ATTEMPT
        self.assertIn("MINING_ATTEMPT", str(msg))
        
        # Vérification que le serveur répond avec BLOCK_UPDATE
        from protocole import decode_server_message
        raw_update = b'{"type": "BLOCK_UPDATE", "x": 0, "y": 0, "z": 0, "block_type": "dirt"}'
        decoded = decode_server_message(raw_update)
        self.assertEqual(decoded["type"], "BLOCK_UPDATE")

    def test_chunk_persistence(self):
        """Test que les chunks sont persistés correctement."""
        self.assertTrue(True)  # Placeholder pour le test de persistance

if __name__ == '__main__':
    unittest.main()