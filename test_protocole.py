import unittest
import protocole

class TestProtocole(unittest.TestCase):
    def test_encode_decode_player_move(self):
        # Test d'encodage/décodage du message PLAYER_MOVE
        msg = protocole.encode_player_move(10.5, 64, 20.5, "NORTH")
        decoded = protocole.decode_player_move(msg)
        self.assertEqual(decoded["payload"]["x"], 10.5)
        self.assertEqual(decoded["payload"]["y"], 64)
        self.assertEqual(decoded["payload"]["z"], 20.5)
        self.assertEqual(decoded["payload"]["orientation"], "NORTH")

    def test_encode_decode_mining_attempt(self):
        # Test d'encodage/décodage du message MINING_ATTEMPT
        msg = protocole.encode_mining_attempt(1, 2, 3)
        decoded = protocole.decode_mining_attempt(msg)
        self.assertEqual(decoded["payload"]["x"], 1)
        self.assertEqual(decoded["payload"]["y"], 2)
        self.assertEqual(decoded["payload"]["z"], 3)

    def test_encode_decode_place_attempt(self):
        # Test d'encodage/décodage du message PLACE_ATTEMPT
        msg = protocole.encode_place_attempt(1, 2, 3, "GRASS")
        decoded = protocole.decode_place_attempt(msg)
        self.assertEqual(decoded["payload"]["x"], 1)
        self.assertEqual(decoded["payload"]["y"], 2)
        self.assertEqual(decoded["payload"]["z"], 3)
        self.assertEqual(decoded["payload"]["block_id"], "GRASS")

if __name__ == "__main__":
    unittest.main()