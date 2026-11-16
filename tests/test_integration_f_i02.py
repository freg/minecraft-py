import unittest
import subprocess
import sys
import os
import time
import socket
import json
from client import GameClient

# Ajout du répertoire courant au PYTHONPATH pour éviter les erreurs d'importation
sys.path.insert(0, '.')

class TestIntegrationFI02(unittest.TestCase):
    def setUp(self):
        # Démarrer le serveur sur un port libre via subprocess en mode serve_forever
        self.server_process = subprocess.Popen([sys.executable, 'server.py'])
        time.sleep(1)  # Attendre que le serveur démarre

    def tearDown(self):
        # Arrêter le serveur
        self.server_process.terminate()
        self.server_process.wait()

    def test_mining_block(self):
        """F-I02 : Test de minage d'un bloc via le protocole."""
        # Créer un client avec les paramètres par défaut du serveur
        client = GameClient("127.0.0.1", 25565)
        client.connect()
        
        # Simuler une tentative de minage
        response = client.send_mining(0, 0, 0)  # Minage du bloc à (0, 0, 0)
        time.sleep(0.1)
        
        # La méthode send_mining devrait renvoyer un message de succès
        self.assertIsNotNone(response)
        
        # Fermer la connexion
        client.close()

    def test_mining_protocol_compliance(self):
        """F-I02 : Test que le protocole utilise les types MINING_ATTEMPT et BLOCK_UPDATE."""
        # Vérification du type de message envoyé par le client au serveur lors du minage
        from protocole import encode_player_mining
        msg = encode_player_mining(0, 0, 0, "STONE", "test_id")
        # Le message doit être de type MINING_ATTEMPT
        self.assertIn("MINING_ATTEMPT", json.dumps(msg))
        
        # Vérification qu'un bloc est bien mis à jour (exemple simple)
        from protocole import encode_block_update
        update_msg = encode_block_update(0, 0, 0, "DIRT", "AIR")
        self.assertIn("BLOCK_UPDATE", json.dumps(update_msg))

    def test_block_update_after_mining(self):
        """F-I02 : Test que le bloc est bien mis à jour après minage."""
        client = GameClient("127.0.0.1", 25565)
        client.connect()
        
        # Effectuer une tentative de minage et attendre
        client.send_mining(0, 0, 0)
        time.sleep(0.2)  # Laisser le temps au serveur de répondre
        
        # S'assurer qu'une réponse a été reçue
        self.assertTrue(client.received_block_update is not None)
        
        # Fermer la connexion
        client.close()

if __name__ == '__main__':
    unittest.main()