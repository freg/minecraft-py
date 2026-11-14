"""
F-I02
Test d'intégration pour le minage de blocs.
"""

import unittest
import socket
import threading
import time
import os
import sys

# Ajout du chemin du projet au PYTHONPATH pour les imports
sys.path.insert(0, '/opt/data/ateliers/minecraft-py')
sys.path.insert(0, '/opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/client')
sys.path.insert(0, '/opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/serveur')

from client import GameClient
import asyncio

class TestIntegrationFI02(unittest.TestCase):
    """Test d'intégration pour l'exigence F-I02 : Minage de Blocs"""

    def setUp(self):
        # Configuration du serveur
        self.port = 25565
        self.host = "127.0.0.1"
        
        # Lancement asynchrone du serveur via asyncio.run()
        self.server_thread = threading.Thread(target=asyncio.run, args=(self.start_server_async(),))
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Attendre que le serveur démarre
        time.sleep(0.5)
        
    async def start_server_async(self):
        from server import start_server
        await start_server(self.host, self.port)
        
    def test_mining_attempt_and_block_update(self):
        """Test de l'envoi d'une tentative de minage et réception d'une mise à jour du bloc."""
        client = GameClient(self.host, self.port)
        try:
            client.connect()
            
            # Simuler une tentative de minage sur un bloc
            response = client.send_mining(0, 0, 0)  # Coordonnées arbitraires
            
            # Vérifier que l'on reçoit une réponse BLOCK_UPDATE avec les bonnes propriétés
            self.assertIn("type", response)
            self.assertEqual(response["type"], "BLOCK_UPDATE")
            self.assertIn("x", response)
            self.assertIn("y", response)
            self.assertIn("z", response)
        except Exception as e:
            # En cas d'erreur, ne pas laisser échouer le test pour l'absence de serveur
            if "Connection refused" in str(e) or "Bad file descriptor" in str(e):
                self.fail(f"Erreur de connexion au serveur : {e}")
            else:
                raise e

    def tearDown(self):
        # Le serveur est démarré via asyncio, il faut gérer son arrêt proprement
        pass

if __name__ == '__main__':
    unittest.main()