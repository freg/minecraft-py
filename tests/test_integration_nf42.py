import subprocess
import unittest
import time
import json
import os

class TestNF42(unittest.TestCase):
    def setUp(self):
        self.server_process = subprocess.Popen(["python3", "../_deploiements/minecraft-py/serveur/server.py"])
        # Attendre que le serveur démarre
        time.sleep(2)

    def tearDown(self):
        self.server_process.terminate()
        self.server_process.wait()

    def test_deployment_file_exists(self):
        """Vérifie que le fichier DEPLOIEMENT.json existe."""
        self.assertTrue(os.path.exists('DEPLOIEMENT.json'), "Le fichier DEPLOIEMENT.json n'existe pas.")

    def test_api_path_in_deployment(self):
        """Vérifie que l'API path est bien configuré dans DEPLOIEMENT.json."""
        with open('DEPLOIEMENT.json', 'r') as f:
            data = json.load(f)
        self.assertIn('api_path', data, "api_path non trouvé dans DEPLOIEMENT.json")
        self.assertEqual(data['api_path'], '/api/models', "L'api_path n'est pas correct.")

    def test_port_in_deployment(self):
        """Vérifie que le port est bien configuré dans DEPLOIEMENT.json."""
        with open('DEPLOIEMENT.json', 'r') as f:
            data = json.load(f)
        self.assertIn('port', data, "port non trouvé dans DEPLOIEMENT.json")
        self.assertEqual(data['port'], 25565, "Le port n'est pas correct.")

    def test_deployment_valid_json(self):
        """Vérifie que le fichier DEPLOIEMENT.json est un JSON valide."""
        with open('DEPLOIEMENT.json', 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, dict, "DEPLOIEMENT.json n'est pas un objet JSON valide.")

    def test_connection(self):
        # Exemple de test : vérifie la connexion au serveur
        pass

if __name__ == '__main__':
    unittest.main()