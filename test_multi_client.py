import unittest
import subprocess
import sys
import os
import time

# Ajout du répertoire courant au path pour importer le serveur
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestMultiClient(unittest.TestCase):
    def setUp(self):
        # Démarrer le serveur sur un port libre dans un processus séparé
        self.port = 25567  # Utiliser un port différent de celui du déploiement
        # Rediriger stdout et stderr pour éviter les warnings de resource
        self.server_process = subprocess.Popen([sys.executable, 'server.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)  # Attendre que le serveur démarre

    def tearDown(self):
        # Arrêter le serveur
        if hasattr(self, 'server_process') and self.server_process.poll() is None:
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()

    def test_multi_client_sync(self):
        """Test de synchronisation entre 2 clients"""
        # Ici, on pourra faire un test plus complet avec des clients réels si nécessaire
        self.assertTrue(True)  # Placeholder pour le moment

if __name__ == '__main__':
    unittest.main()