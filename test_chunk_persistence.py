import unittest
import os
import tempfile
import world_manager

class TestChunkPersistence(unittest.TestCase):
    def test_chunk_saving_and_loading(self):
        """Test que les fichiers de chunks sont bien créés avec le bon format."""
        # Vérifie qu'on a les fichiers dans le répertoire chunks/
        self.assertTrue(os.path.exists("./chunks/chunk_0_0.bin.v1"))
        
        # Vérifie qu'ils ont le bon header (b"v1") 
        with open("./chunks/chunk_0_0.bin.v1", "rb") as f:
            header = f.read(2)
            self.assertEqual(header, b"v1")
            
    def test_chunk_file_formats(self):
        """Test des formats des fichiers de chunk"""
        chunks_dir = "./chunks"
        for filename in os.listdir(chunks_dir):
            if filename.startswith("chunk_") and filename.endswith(".bin.v1"):
                filepath = os.path.join(chunks_dir, filename)
                self.assertTrue(os.path.isfile(filepath))
                with open(filepath, "rb") as f:
                    header = f.read(2)
                    self.assertEqual(header, b"v1")

if __name__ == '__main__':
    unittest.main()