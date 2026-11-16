import unittest
import subprocess
import sys
import os
import time
import tempfile
import socket

# Ajout du répertoire courant au path pour importer le serveur
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestLatencyIntegration(unittest.TestCase):
    def test_latency_scenario(self):
        """F-S03: Simuler des scénarios de latence réseau et valider le comportement"""
        # Tester avec un port libre
        port = 25568
        with tempfile.TemporaryDirectory() as d:
            # Démarrer le serveur sur un port spécifique
            env = os.environ.copy()
            env['PORT'] = str(port)
            env['HOTE'] = '127.0.0.1'
            
            # Lancer le serveur en arrière-plan
            server_process = subprocess.Popen([sys.executable, 'server.py'], 
                                              env=env, 
                                              stdout=subprocess.DEVNULL, 
                                              stderr=subprocess.DEVNULL)
            
            try:
                time.sleep(1)  # Attendre que le serveur démarre
                
                # Simuler un client qui se connecte et envoie une requête
                client_output = subprocess.run([sys.executable, 'client.py', '--hote', '127.0.0.1', '--port', str(port), '--test'], 
                                              capture_output=True, text=True, timeout=10)
                
                # Vérifier que le client s'est terminé avec succès
                self.assertEqual(client_output.returncode, 0)
                
            finally:
                server_process.terminate()
                try:
                    server_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server_process.kill()

    def test_server_response_time(self):
        """F-S03: Teste le temps de réponse du serveur"""
        # Lancer le serveur sur un port libre
        port = 25569

        env = os.environ.copy()
        env['PORT'] = str(port)
        env['HOTE'] = '127.0.0.1'

        server_process = subprocess.Popen([sys.executable, 'server.py'], 
                                          env=env, 
                                          stdout=subprocess.DEVNULL, 
                                          stderr=subprocess.DEVNULL)

        try:
            time.sleep(1)  # Attendre que le serveur démarre

            # Vérifier qu'on peut se connecter au serveur
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            self.assertEqual(result, 0)  # La connexion doit réussir

        finally:
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()

if __name__ == '__main__':
    unittest.main()