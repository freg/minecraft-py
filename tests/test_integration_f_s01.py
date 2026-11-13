# Test d'intégration F-S01 : Autorité du Serveur

import unittest
import subprocess
import os

class TestIntegrationFS01(unittest.TestCase):
    def test_f_s01_integration(self):
        """Vérifie que les tests d'intégration pour F-S01 passent."""
        result = subprocess.run([
            'python3', '-m', 'unittest', 'discover', 
            '-s', '/opt/data/ateliers/minecraft-py/tests', 
            '-p', 'test_integration_f_s01.py'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"Les tests d'intégration F-S01 ont échoué :\n{result.stdout}\n{result.stderr}")

if __name__ == '__main__':
    unittest.main()