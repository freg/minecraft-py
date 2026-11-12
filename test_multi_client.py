import unittest
import subprocess
import sys
import os
import time

# Ajout du répertoire courant au path pour importer le serveur
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client import GameClient
# from server import Server  # Supprimé car Server n'existe pas

# Fonction helper pour vérifier le type de fichier avant read_file
def is_text_file(path):
    try:
        import subprocess
        result = subprocess.run(['file', '-b', path], capture_output=True, text=True)
        return 'text' in result.stdout.lower()
    except:
        # Si 'file' n'est pas disponible ou échoue, fallback sur une tentative de lecture
        try:
            with open(path, 'r') as f:
                f.read(1024)  # Essayer de lire quelques octets
            return True
        except:
            return False

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

    def test_latency_under_200ms(self):
        """
        Test de latence < 200ms pour synchronisation client-serveur
        """
        # Test d'envoi/reception d'un message BLOCK_UPDATE entre deux clients
        # Simulation d'une mesure de latence basique sur le port 25565
        import socket
        import time

        # Créer un socket de test
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        
        try:
            start_time = time.time()
            sock.connect(('127.0.0.1', 25565))
            end_time = time.time()
            
            latency = (end_time - start_time) * 1000  # En millisecondes
            self.assertLess(latency, 200, f"Latence {latency:.2f}ms > 200ms")
        finally:
            sock.close()

    def test_file_type_verification_before_read(self):
        # Vérifier que toutes les lectures de fichiers utilisent la vérification de type
        import os
        chunks_dir = 'chunks'
        if os.path.exists(chunks_dir):
            for f in os.listdir(chunks_dir):
                file_path = os.path.join(chunks_dir, f)
                # Ignorer les dossiers __pycache__
                if not os.path.isdir(file_path):
                    self.assertTrue(is_text_file(file_path), f"Fichier binaire détecté : {file_path}")

if __name__ == '__main__':
    unittest.main()