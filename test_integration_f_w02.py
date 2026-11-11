import unittest
from protocole import encode_block_update, decode_block_update, BlockID

class TestIntegrationF_W02(unittest.TestCase):
    def test_block_id_in_integration(self):
        # F-W02: BlockID : AIR, DIRT, GRASS, STONE
        # Test the integration of BlockID values in block update operations
        pos = (10, 50, 10)
        block_type = BlockID.STONE
        msg = encode_block_update(pos[0], pos[1], pos[2], "AIR", "STONE")
        decoded = decode_block_update(msg)
        self.assertEqual(decoded['payload']['position'], pos)
        self.assertEqual(decoded['payload']['block_type'], block_type)

if __name__ == '__main__':
    unittest.main()