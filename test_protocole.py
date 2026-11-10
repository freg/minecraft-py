import unittest
import sys
import os

# Ajout du chemin pour importer protocole
sys.path.insert(0, os.path.abspath('.'))

from protocole import *

class TestProtocole(unittest.TestCase):
    def setUp(self):
        # Initialisation avant chaque test
        pass

    def test_encode_decode_player_move(self):
        payload = {"x": 10, "y": 64, "z": 20}
        msg = encode_player_move(10, 64, 20, "NORTH")
        decoded = decode_player_move(msg)
        self.assertEqual(decoded["type"], "PLAYER_MOVE")
        self.assertEqual(decoded["payload"]["x"], 10)
        self.assertEqual(decoded["payload"]["y"], 64)
        self.assertEqual(decoded["payload"]["z"], 20)
        self.assertEqual(decoded["source_id"], "NORTH")

    def test_encode_decode_player_mining(self):
        payload = {"x": 1, "y": 2, "z": 3, "block_id": "STONE"}
        msg = encode_player_mining(1, 2, 3, "STONE", "test_id")
        decoded = decode_mining_attempt(msg)
        self.assertEqual(decoded["type"], "MINING_ATTEMPT")
        self.assertEqual(decoded["payload"]["x"], 1)
        self.assertEqual(decoded["payload"]["y"], 2)
        self.assertEqual(decoded["payload"]["z"], 3)
        self.assertEqual(decoded["payload"]["block_id"], "STONE")
        self.assertEqual(decoded["source_id"], "test_id")

    def test_encode_decode_player_place(self):
        payload = {"x": 1, "y": 2, "z": 3, "block_id": "GRASS"}
        msg = encode_player_place(1, 2, 3, "GRASS", "test_id")
        decoded = decode_place_attempt(msg)
        self.assertEqual(decoded["type"], "PLACE_ATTEMPT")
        self.assertEqual(decoded["payload"]["x"], 1)
        self.assertEqual(decoded["payload"]["y"], 2)
        self.assertEqual(decoded["payload"]["z"], 3)
        self.assertEqual(decoded["payload"]["block_id"], "GRASS")
        self.assertEqual(decoded["source_id"], "test_id")

    def test_encode_decode_block_update(self):
        msg = encode_block_update(1, 50, 3, "DIRT", "STONE", "test_id")
        decoded = decode_block_update(msg)
        self.assertEqual(decoded["type"], "BLOCK_UPDATE")
        self.assertEqual(decoded["payload"]["x"], 1)
        self.assertEqual(decoded["payload"]["y"], 50)
        self.assertEqual(decoded["payload"]["z"], 3)
        self.assertEqual(decoded["payload"]["old_block_id"], "DIRT")
        self.assertEqual(decoded["payload"]["new_block_id"], "STONE")
        self.assertEqual(decoded["source_id"], "test_id")

    def test_encode_decode_chunk_loaded(self):
        blocks = [{"x": 0, "y": 50, "z": 0, "block_id": "STONE"}]
        msg = encode_chunk_loaded(0, 0, blocks, "test_id")
        decoded = decode_chunk_loaded(msg)
        self.assertEqual(decoded["type"], "CHUNK_LOADED")
        self.assertEqual(decoded["payload"]["chunk_x"], 0)
        self.assertEqual(decoded["payload"]["chunk_z"], 0)
        self.assertEqual(decoded["payload"]["blocks"], blocks)
        self.assertEqual(decoded["source_id"], "test_id")

    def test_encode_decode_player_joined(self):
        msg = encode_player_joined("Player1", "player_001")
        decoded = decode_player_joined(msg)
        self.assertEqual(decoded["type"], "PLAYER_JOINED")
        self.assertEqual(decoded["payload"]["username"], "Player1")
        self.assertEqual(decoded["payload"]["player_id"], "player_001")

    def test_encode_decode_join(self):
        msg = encode_join("Player1", "1.0")
        decoded = decode_join(msg)
        self.assertEqual(decoded["type"], "JOIN")
        self.assertEqual(decoded["payload"]["username"], "Player1")
        self.assertEqual(decoded["payload"]["version"], "1.0")

    def test_encode_decode_auth(self):
        msg = encode_auth("token_abc123")
        decoded = decode_auth(msg)
        self.assertEqual(decoded["type"], "AUTH")
        self.assertEqual(decoded["payload"]["token"], "token_abc123")

if __name__ == '__main__':
    unittest.main()