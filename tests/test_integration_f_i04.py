import unittest
import subprocess
import sys
import os
import time
from client import GameClient

# Ajout du répertoire courant au PYTHONPATH pour éviter les erreurs d'importation
sys.path.insert(0, '.')

class TestIntegrationFI04(unittest.TestCase):
    def setUp(self):
        # Démarrer le serveur sur un port libre via subprocess en mode serve_forever
        self.server_process = subprocess.Popen([sys.executable, 'server.py'])
        time.sleep(1)  # Attendre que le serveur démarre

    def tearDown(self):
        # Arrêter le serveur
        self.server_process.terminate()
        self.server_process.wait()

    def test_inventory_prediction_integration(self):
        """F-I04 : Test que la prédiction d'inventaire fonctionne en simulation d'intégration."""
        # Simulation d'un client
        client = GameClient("127.0.0.1", 25565)
        # Ajout d’un item dans l'inventaire
        client.add_item('dirt', 1)
        # On vérifie qu’il est bien présent
        self.assertEqual(client.inventory['dirt'], 1)

    def test_inventory_consistency_check(self):
        """F-I04 : Test que les items ajoutés dans l'inventaire sont correctement gérés."""
        client = GameClient("127.0.0.1", 25565)
        # Ajout d’une série d'items
        client.add_item('wood', 3)
        client.add_item('stone', 2)
        client.add_item('dirt', 5)
        
        self.assertTrue(client.inventory['wood'] == 3)
        self.assertTrue(client.inventory['stone'] == 2)
        self.assertTrue(client.inventory['dirt'] == 5)

    def test_inventory_update_after_mining(self):
        """F-I04 : Test de mise à jour de l'inventaire suite à un minage."""
        client = GameClient("127.0.0.1", 25565)
        
        # Effectuer un minage et mettre à jour l'inventaire
        original_inventory = dict(client.inventory)  # Copie avant minage
        client.add_item('stone', 1)
        client.add_item('dirt', 2)
        
        self.assertTrue(client.inventory['stone'] == 1)
        self.assertTrue(client.inventory['dirt'] == 2)

if __name__ == '__main__':
    unittest.main()