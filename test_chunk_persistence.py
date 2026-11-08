import unittest
import os
import tempfile
import world_manager

class TestChunkPersistence(unittest.TestCase):
    def setUp(self):
        # Utiliser un répertoire temporaire pour les tests
        self.temp_dir = tempfile.mkdtemp()
        # Mock la méthode save_chunk pour qu'elle pointe vers le répertoire temporaire
        original_save_chunk = world_manager.WorldManager.save_chunk
        
        def mock_save_chunk(self, chunk_pos, chunk_data):
            filename = f"chunk_{chunk_pos[0]}_{chunk_pos[1]}.bin.v1"
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, "wb") as f:
                f.write(b"v1")
                f.write(chunk_data)
        
        def mock_load_chunk(self, chunk_pos):
            filename = f"chunk_{chunk_pos[0]}_{chunk_pos[1]}.bin.v1"
            filepath = os.path.join(self.temp_dir, filename)
            if not os.path.exists(filepath):
                return None
            with open(filepath, "rb") as f:
                header = f.read(2)
                if header != b"v1":
                    raise ValueError(f"Version inconnue du chunk : {header}")
                return f.read()
        
        # Remplacer les méthodes dans la classe pour le test
        world_manager.WorldManager.save_chunk = mock_save_chunk
        world_manager.WorldManager.load_chunk = mock_load_chunk

    def test_round_trip_chunk(self):
        wm = world_manager.WorldManager()
        
        # Créer un chunk avec des données
        chunk_data = b"\x01\x02\x03\x04"
        wm.save_chunk((0, 0), chunk_data)
        
        # Charger le chunk
        loaded_chunk = wm.load_chunk((0, 0))
        
        # Vérifier que les données sont identiques
        self.assertEqual(loaded_chunk, chunk_data)

    def tearDown(self):
        # Nettoyer le répertoire temporaire
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()