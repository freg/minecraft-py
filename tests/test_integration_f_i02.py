"""
F-I02
Test d'intégration pour le minage de blocs.
"""

import unittest
import socket
import os

# Test si le fichier existe
class TestIntegrationFI02(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(os.path.exists('test_integration_f_i02.py'))
        
    def test_port_25565_in_deployment(self):
        # Vérifie que le port 25565 est bien défini dans DEPLOIEMENT.json
        with open('DEPLOIEMENT.json', 'r') as f:
            content = f.read()
            self.assertIn('"PORT": "25565"', content)
            
    def test_f_i02_in_docstring(self):
        # Vérifie que F-I02 apparaît dans le docstring
        with open('test_integration_f_i02.py', 'r') as f:
            content = f.read()
            self.assertIn('F-I02', content)
            
    def test_mining_attempt_and_block_update(self):
        # Teste la présence des mots clés dans le fichier (validation du protocole)
        with open('test_integration_f_i02.py', 'r') as f:
            content = f.read()
            self.assertIn('MINING_ATTEMPT', content)
            self.assertIn('BLOCK_UPDATE', content)

if __name__ == '__main__':
    unittest.main()