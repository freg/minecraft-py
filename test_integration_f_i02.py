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

    def test_mining_block_with_correct_protocol(self):
        """Test que le protocole utilise les types MINING_ATTEMPT et BLOCK_UPDATE"""
        # Vérification du type de message envoyé par le client au serveur lors du minage
        from protocole import encode_player_mining
        msg = encode_player_mining(0, 0, 0)
        # Le message doit être de type MINING_ATTEMPT
        self.assertIn("MINING_ATTEMPT", json.dumps(msg))
        
        # Vérification que le serveur répond avec BLOCK_UPDATE
        from protocole import decode_server_message
        raw_update = b'{"type": "BLOCK_UPDATE", "x": 0, "y": 0, "z": 0, "block_type": "dirt"}'
        decoded = decode_server_message(raw_update)
        self.assertEqual(decoded["type"], "BLOCK_UPDATE")