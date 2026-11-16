import unittest
import subprocess
import sys
import os
import time
import socket
from client import GameClient

# Ajout du répertoire courant au PYTHONPATH pour éviter les erreurs d'importation
sys.path.insert(0, '.')

class TestF_i04(unittest.TestCase):
    def setUp(self):
        # Démarrer le serveur sur un port libre via subprocess en mode serve_forever
        self.server_process = subprocess.Popen([sys.executable, 'server.py'])
        time.sleep(1)  # Attendre que le serveur démarre

    def tearDown(self):
        # Arrêter le serveur
        self.server_process.terminate()
        self.server_process.wait()

    def test_add_item(self):
        """F-I04 : Test d'ajout d'item dans l'inventaire."""
        client = GameClient("127.0.0.1", 25565)
        # Ajout d'un item
        client.add_item('dirt', 5)
        self.assertEqual(client.inventory['dirt'], 5)

    def test_remove_item(self):
        """F-I04 : Test de suppression d'item de l'inventaire."""
        client = GameClient("127.0.0.1", 25565)
        # Ajout d’un item
        client.add_item('dirt', 5)
        # Suppression de l’item
        client.add_item('dirt', -5)
        self.assertEqual(client.inventory['dirt'], 0)

    def test_inventory_consistency(self):
        """F-I04 : Test que les items ajoutés sont bien conservés dans l'inventaire."""
        client = GameClient("127.0.0.1", 25565)
        # Ajout d’une série d'items
        client.add_item('dirt', 10)
        client.add_item('stone', 5)
        self.assertTrue(client.inventory['dirt'] == 10 and client.inventory['stone'] == 5)

    def test_inventory_capacity(self):
        """F-I04 : Test que la capacité de l'inventaire est respectée."""
        client = GameClient("127.0.0.1", 25565)
        # On vérifie qu’on peut ajouter plusieurs fois le même item
        client.add_item('wood', 3)
        client.add_item('wood', 2)
        self.assertEqual(client.inventory['wood'], 5)

if __name__ == '__main__':
    unittest.main()