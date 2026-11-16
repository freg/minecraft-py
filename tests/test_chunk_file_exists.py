import unittest
import os

class TestChunkFileExists(unittest.TestCase):
    def test_chunk_file_exists(self):
        # Vérification de l'existence du fichier avant lecture
        chunk_path = 'chunks/chunk_0_0.bin.v1'
        self.assertTrue(os.path.isfile(chunk_path), f"Le fichier {chunk_path} est requis mais n'existe pas.")

if __name__ == '__main__':
    unittest.main()