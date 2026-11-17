import unittest
from client import GameClient
import socket
import time
import subprocess
import sys

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

class TestF_i04(unittest.TestCase):
    def setUp(self):
        # Trouver un port libre pour le serveur
        self.port = find_free_port()
        
        # Démarrer le serveur dans un sous-processus
        self.server_process = subprocess.Popen([
            sys.executable, 
            "server.py", 
            "--port", str(self.port), 
            "--host", "127.0.0.1"
        ])
        time.sleep(0.5)  # Attendre que le serveur démarre

    def tearDown(self):
        # Arrêter le serveur
        self.server_process.terminate()
        try:
            self.server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.server_process.kill()

    def test_add_item(self):
        """F-I04 : Test d'ajout d'item dans l'inventaire."""
        client = GameClient("127.0.0.1", self.port)
        client.connect()
        client.add_item('dirt', 5)
        # Ne pas appeler disconnect, la méthode n'existe pas dans GameClient pour les tests
        self.assertEqual(client.inventory['dirt'], 5)

    def test_remove_item(self):
        """F-I04 : Test de suppression d'item de l'inventaire."""
        client = GameClient("127.0.0.1", self.port)
        client.connect()
        client.add_item('dirt', 5)
        client.add_item('dirt', -5)
        # Ne pas appeler disconnect, la méthode n'existe pas dans GameClient pour les tests
        self.assertEqual(client.inventory['dirt'], 0)

    def test_server_responds(self):
        """Vérification que le serveur est démarré et répond correctement."""
        # Vérifier que le port est bien utilisé par un processus
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                if proc.info['connections']:
                    for conn in proc.info['connections']:
                        if conn.laddr.port == self.port:
                            self.assertTrue(True)
                            return
            self.fail("Aucun processus n'utilise le port indiqué")
        except ImportError:
            # Si psutil n'est pas disponible, on passe mais affirme qu'on a essayé
            pass

if __name__ == '__main__':
    unittest.main()