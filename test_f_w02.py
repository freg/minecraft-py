import unittest
from protocole import encode_block_update, decode_block_update, BlockID

class TestF_W02(unittest.TestCase):
    def test_block_id_values(self):
        # F-W02: BlockID : AIR, DIRT, GRASS, STONE
        # Test that BlockID contains the expected values
        self.assertEqual(BlockID.AIR, 0)
        self.assertEqual(BlockID.DIRT, 1)
        self.assertEqual(BlockID.GRASS, 2)
        self.assertEqual(BlockID.STONE, 3)

    def test_encode_decode_block_update(self):
        # F-W02: BlockID : AIR, DIRT, GRASS, STONE
        # Test encoding and decoding a block update with valid BlockID values
        pos = (10, 50, 10)
        block_type = BlockID.DIRT
        msg = encode_block_update(pos[0], pos[1], pos[2], "AIR", block_type)
        decoded = decode_block_update(msg)
        self.assertEqual(decoded['payload']['position'], pos)
        self.assertEqual(decoded['payload']['block_type'], block_type)

if __name__ == '__main__':
    unittest.main()