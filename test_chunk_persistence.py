import unittest
import os
import sys

# Add the project root to the path so we can import modules from it
sys.path.insert(0, os.path.abspath('.'))

from chunks.chunk import Chunk
from world_manager import save_chunk, load_chunk


class TestChunkPersistence(unittest.TestCase):
    def test_round_trip(self):
        # Create a chunk with some data
        chunk = Chunk(0, 0)
        chunk.blocks[0][0][0] = 1  # Set a block to DIRT

        # Save the chunk to disk
        save_chunk(chunk)

        # Load the chunk back from disk
        loaded_chunk = load_chunk(0, 0)

        # Verify that the loaded chunk is equal to the original
        self.assertEqual(chunk, loaded_chunk)

    def test_load_chunk(self):
        # Test loading an existing chunk file
        loaded_chunk = load_chunk(0, 0)
        self.assertIsInstance(loaded_chunk, Chunk)
        # Should have a valid structure (not empty chunks)
        self.assertEqual(len(loaded_chunk.blocks), 16)
        self.assertEqual(len(loaded_chunk.blocks[0]), 256)
        self.assertEqual(len(loaded_chunk.blocks[0][0]), 16)


if __name__ == '__main__':
    unittest.main()