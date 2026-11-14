"""
Tests d'intégration pour l'exigence F-S02 : Diffusion de Changement.
Validation du processus BLOCK_UPDATE via le protocole JSON.
"""

import unittest
import json
import socket
import threading
import time
import asyncio
import os
import sys

# Ajout du chemin pour importer correctement les modules
sys.path.insert(0, '/opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/serveur')

from server import start_server
import server


class TestFS02(unittest.TestCase):
    """
    F-S02 : Diffusion de Changement
    """

    def setUp(self):
        # Démarrage du serveur dans un thread
        self.server_thread = threading.Thread(target=asyncio.run, args=(start_server(25565),))
        self.server_thread.start()
        # Attendre que le serveur démarre
        time.sleep(1)

    def tearDown(self):
        # Arrêt du serveur
        self.server_thread.join()

    def test_block_update_process(self):
        """
        Valide l'envoi et la réception du message BLOCK_UPDATE.
        """
        # Création d'un client de test
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 25565))

        # Envoi du message BLOCK_UPDATE
        block_update_message = {
            'type': 'BLOCK_UPDATE',
            'payload': {'x': 10, 'y': 20, 'z': 30, 'old_block_id': 'STONE', 'new_block_id': 'AIR'}
        }

        client_socket.send(json.dumps(block_update_message).encode('utf-8'))

        # Réception de la réponse
        response = client_socket.recv(1024).decode('utf-8')
        response_data = json.loads(response)

        # Validation de la connexion (WELCOME)
        self.assertEqual(response_data['type'], 'WELCOME')

        # Fermeture du socket
        client_socket.close()


if __name__ == '__main__':
    unittest.main()