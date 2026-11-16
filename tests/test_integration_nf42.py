import unittest
import socket
import requests
import time
import subprocess
import os

class TestSecurityRobustness(unittest.TestCase):
    """
    Tests NF-4.2 : Sécurité et Robustesse
    """

    def setUp(self):
        # Démarrer le serveur dans un sous-processus
        self.server_process = subprocess.Popen(
            ["python3", "../_deploiements/minecraft-py/serveur/server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Attendre que le serveur démarre
        time.sleep(2)

    def tearDown(self):
        # Fermer le serveur à la fin du test
        self.server_process.terminate()
        try:
            self.server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.server_process.kill()

    def test_connection_timeout(self):
        """NF-4.2: Vérifie la gestion des timeouts de connexion."""
        # Arrêter le serveur temporairement
        self.server_process.terminate()
        try:
            self.server_process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            self.server_process.kill()
        
        # Attendre que le port soit libéré
        time.sleep(1)
        
        # Essayer de se connecter, cela devrait échouer avec une erreur de timeout ou connexion refusée
        with self.assertRaises(requests.exceptions.RequestException):
            requests.get("http://127.0.0.1:25565/api/serveur", timeout=1)

    def test_invalid_input_handling(self):
        """NF-4.2: Vérifie la gestion des inputs invalides."""
        # Envoyer une requête mal formée
        response = requests.post(
            "http://127.0.0.1:25565/api/serveur",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        # On attend un code d'erreur 400 ou 500 selon l'implémentation du serveur
        self.assertIn(response.status_code, [400, 500])

    def test_server_restart_handling(self):
        """NF-4.2: Vérifie la robustesse du serveur face aux redémarrages."""
        # Fermer le serveur brutalement
        self.server_process.terminate()
        try:
            self.server_process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            self.server_process.kill()

        # Redémarrer le serveur
        self.server_process = subprocess.Popen(
            ["python3", "../_deploiements/minecraft-py/serveur/server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)

        # Vérifier qu'il est de nouveau opérationnel
        response = requests.get("http://127.0.0.1:25565/api/serveur")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()