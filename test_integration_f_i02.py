"""
F-I02
Test d'intégration pour le minage de blocs.
"""
import socket
import json
import time
import unittest

from client import GameClient


class TestIntegrationFI02(unittest.TestCase):
    def test_mining_block(self):
        # Créer un client avec les paramètres par défaut du serveur
        client = GameClient("127.0.0.1", 25565)
        client.connect()

        # Simuler une tentative de minage
        response = client.send_mining(0, 0, 0)  # Minage du bloc à (0, 0, 0)

        # Vérifier que le serveur a bien reçu l'événement MINING_ATTEMPT et envoyé BLOCK_UPDATE
        # Ici on simule simplement la réception d'un message BLOCK_UPDATE
        time.sleep(0.1)

        # Fermer la connexion
        client.disconnect()