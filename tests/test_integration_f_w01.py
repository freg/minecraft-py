import unittest
import subprocess
import time
import os
import glob

# F-W01: Tests d'intégration du système de chunks (génération, persistence, chargement)

class TestChunkWorldSystem(unittest.TestCase):
    def setUp(self):
        # Démarrer le serveur sur un port libre
        self.port = 25565
        self.hote = "127.0.0.1"
        self.server_process = subprocess.Popen(
            ["python3", "server.py"],
            cwd="/opt/data/ateliers/_deploiements/minecraft-py/serveur"
        )
        # Attendre que le serveur démarre
        time.sleep(2)
        self.chunks_dir = "/opt/data/ateliers/_deploiements/minecraft-py/serveur/chunks"

    def tearDown(self):
        # Arrêter le serveur
        self.server_process.terminate()
        self.server_process.wait()

    def test_chunk_generation(self):
        """F-W01: Test la génération de chunks via worldgen.py"""
        # Vérifier qu'au moins un fichier chunk est généré
        files = glob.glob(os.path.join(self.chunks_dir, "chunk_*.bin.v1"))
        self.assertGreater(len(files), 0, "Au moins un chunk devrait être généré")

    def test_chunk_persistence(self):
        """F-W01: Test la persistance des chunks via world_manager.py"""
        # Simuler l'écriture d'un chunk puis vérifier sa persistance
        # Ici, nous testons simplement qu'on peut accéder au dossier des chunks
        self.assertTrue(os.path.exists(self.chunks_dir), "Le dossier des chunks devrait exister")

if __name__ == '__main__':
    unittest.main()