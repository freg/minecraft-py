import unittest
from protocole import *

class TestProtocole(unittest.TestCase):
    def test_encode_decode_player_move(self):
        msg = encode_player_move(10, 64, 20, "NORTH")
        decoded = decode_player_move(msg)
        self.assertEqual(decoded["payload"]["x"], 10)
        self.assertEqual(decoded["payload"]["y"], 64)
        self.assertEqual(decoded["payload"]["z"], 20)

    def test_encode_decode_player_mining(self):
        msg = encode_player_mining(1, 2, 3, "STONE", "test_id")
        decoded = decode_mining_attempt(msg)
        self.assertEqual(decoded["payload"]["x"], 1)
        self.assertEqual(decoded["payload"]["z"], 3)
        self.assertEqual(decoded["payload"]["block_id"], "STONE")

    def test_encode_decode_player_place(self):
        msg = encode_player_place(1, 2, 3, "GRASS", "test_id")
        decoded = decode_place_attempt(msg)
        self.assertEqual(decoded["payload"]["x"], 1)
        self.assertEqual(decoded["payload"]["y"], 2)
        self.assertEqual(decoded["payload"]["block_id"], "GRASS")

if __name__ == '__main__':
    unittest.main()