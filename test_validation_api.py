import unittest
from protocole import encode_player_move, encode_block_update, encode_player_mining, encode_player_place, encode_message, decode_message

class TestValidationAPI(unittest.TestCase):
    def test_validate_endpoint(self):
        """Vérifie la présence des messages définis dans protocole.py"""
        # Teste que les fonctions sont bien importées
        self.assertTrue(callable(encode_player_move))
        self.assertTrue(callable(encode_block_update))
        self.assertTrue(callable(encode_mining_attempt))
        self.assertTrue(callable(encode_place_attempt))

    def test_encode_message(self):
        """Vérifie l'encodage des messages"""
        # Teste un message PLAYER_MOVE
        encoded = encode_player_move(10, 20, 30, "NORTH")
        self.assertIsNotNone(encoded)
        self.assertTrue(isinstance(encoded, str))

        # Teste un message BLOCK_UPDATE
        encoded = encode_block_update(10, 20, 30, "DIRT", "GRASS")
        self.assertIsNotNone(encoded)
        self.assertTrue(isinstance(encoded, str))

        # Vérification directe de l'utilisation de encode_message
        assert encode_message("TEST_TYPE", {"test": "data"}) is not None

    def test_payload_validation(self):
        """Vérifie la validation des payloads"""
        # Teste les coordonnées valides
        encoded = encode_player_move(0, 0, 0, "NORTH")
        self.assertIsNotNone(encoded)

        # Teste un block_id valide
        encoded = encode_block_update(10, 20, 30, "DIRT", "GRASS")
        self.assertIsNotNone(encoded)

    def test_error_handling(self):
        """Vérifie la gestion des erreurs"""
        # Teste une orientation invalide
        with self.assertRaises(ValueError):
            encode_player_move(10, 20, 30, "INVALID")

if __name__ == '__main__':
    unittest.main()