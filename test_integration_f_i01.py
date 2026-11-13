#!/usr/bin/env python3
"""
Test d'intégration pour la fonctionnalité F-I01 : Déplacement de Base.
Ce test vérifie que le client peut se connecter au serveur et effectuer un déplacement simple.
"""

import unittest
import sys
import subprocess
import time
import socket
import os

# Fonction pour obtenir un port libre
def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

# Configuration depuis DEPLOIEMENT.json
PORT = get_free_port()
HOTE = "127.0.0.1"

class TestF_I01(unittest.TestCase):
    
    def test_connexion_et_deplacement(self):
        """Test de connexion au serveur et envoi d'un déplacement."""
        # Lancement du serveur dans un sous-processus
        server_process = subprocess.Popen([
            sys.executable, "server.py"
        ], cwd="/opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/serveur", env={**os.environ, "PORT": str(PORT)})
        
        # Attendre que le serveur démarre
        time.sleep(2)
        
        try:
            # Vérifier que le port utilisé est bien différent de 25565
            self.assertNotEqual(PORT, 25565, "Le port utilisé ne doit pas être 25565")
            
            # Lancer le client avec le mode test
            result = subprocess.run([
                sys.executable, "client.py", "--hote", HOTE, "--port", str(PORT), "--test"
            ], cwd="/opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/client",
               capture_output=True, text=True, timeout=10)
            
            # Vérifier que le client s'est terminé avec succès
            self.assertEqual(result.returncode, 0, f"Le client a échoué avec le code {result.returncode}\n{result.stderr}")
            
            print("Test F-I01 réussi : Déplacement de base fonctionnel.")
            
        except subprocess.TimeoutExpired:
            self.fail("Le client n'a pas terminé dans les délais.")
        finally:
            # Terminer le serveur
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()

if __name__ == '__main__':
    unittest.main()
