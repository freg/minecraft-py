import unittest
import subprocess
import sys
import os
import time
import socket
import asyncio
import threading
from server import Server
from client import GameClient

# Ajout du répertoire courant au PYTHONPATH pour éviter les erreurs d'importation
sys.path.insert(0, '.')

class TestF_i04(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Démarrer le serveur sur un port libre en utilisant asyncio.run()
        cls.server = Server("127.0.0.1", 25565)
        cls.server_thread = threading.Thread(target=asyncio.run, args=(cls.server.serve_forever(),))
        cls.server_thread.start()
        time.sleep(1)  # Attendre que le serveur démarre

    @classmethod
    def tearDownClass(cls):
        # Arrêter le serveur
        asyncio.run(cls.server.close())
        cls.server_thread.join()

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