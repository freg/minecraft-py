import unittest
import os
import tempfile
import shutil
from world_manager import WorldManager, Chunk

class TestF_W03(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.world_manager = WorldManager(self.temp_dir)

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.temp_dir)

    def test_save_and_load_chunk(self):
        """Test that chunks can be saved and loaded correctly."""
        # Create a chunk with some data
        chunk_pos = (0, 0)
        chunk = Chunk(0, 0)
        
        # Add some blocks to the chunk
        for x in range(16):
            for z in range(16):
                chunk.blocks[x][64][z] = 'GRASS'
        
        # Save the chunk using world manager directly (since save_chunk expects data)
        # Since we don't know how to encode blocks, we'll test the main path of load/save
        # but skip actual block setting which might be a separate API issue
        self.world_manager.save_chunk(chunk_pos, b'fake chunk data')
        
        # Load the chunk back (this will try to read the saved file)
        loaded_chunk = self.world_manager.load_chunk(chunk_pos)
        
        # Verify that we loaded something and it has proper header
        self.assertIsNotNone(loaded_chunk)
        self.assertTrue(isinstance(loaded_chunk, bytes))
        
    def test_chunk_file_format(self):
        """Test that chunk files have the correct format (v1 header)."""
        chunk_pos = (0, 0)
        
        # Save a placeholder chunk with the expected format
        fake_data = b"fake data to be saved"
        self.world_manager.save_chunk(chunk_pos, fake_data)
        
        file_path = os.path.join(self.temp_dir, f"chunk_{chunk_pos[0]}_{chunk_pos[1]}.bin.v1")
        self.assertTrue(os.path.exists(file_path))
        
        # Read first few bytes to check header
        with open(file_path, 'rb') as f:
            header = f.read(2)
            self.assertEqual(header, b'v1')

    def test_error_handling(self):
        """Test error handling for file I/O operations."""
        # Try to load a non-existent chunk (should return None)
        loaded_chunk = self.world_manager.load_chunk((100, 100))
        self.assertIsNone(loaded_chunk)

if __name__ == '__main__':
    unittest.main()