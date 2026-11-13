# Test F-S01 : Autorité du Serveur

import unittest
import subprocess
import os

class TestFS01(unittest.TestCase):
    def test_f_s01_unitaires(self):
        """Vérifie que les tests unitaires pour F-S01 passent."""
        result = subprocess.run([
            'python3', '-m', 'unittest', 'discover', 
            '-s', '/opt/data/ateliers/minecraft-py/tests', 
            '-p', 'test_f_s01.py'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"Les tests unitaires F-S01 ont échoué :\n{result.stdout}\n{result.stderr}")

    def test_f_s01_integration(self):
        """Vérifie que les tests d'intégration pour F-S01 passent."""
        result = subprocess.run([
            'python3', '-m', 'unittest', 'discover', 
            '-s', '/opt/data/ateliers/minecraft-py/tests', 
            '-p', 'test_integration_f_s01.py'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"Les tests d'intégration F-S01 ont échoué :\n{result.stdout}\n{result.stderr}")

    def test_f_s01_docstring(self):
        """Vérifie que les docstrings contiennent 'F-S01'."""
        # Vérifier le fichier test_f_s01.py
        with open('/opt/data/ateliers/minecraft-py/tests/test_f_s01.py', 'r') as f:
            content = f.read()
            self.assertIn('F-S01', content, "Le fichier test_f_s01.py doit contenir 'F-S01' dans ses docstrings")

        # Vérifier le fichier test_integration_f_s01.py
        with open('/opt/data/ateliers/minecraft-py/tests/test_integration_f_s01.py', 'r') as f:
            content = f.read()
            self.assertIn('F-S01', content, "Le fichier test_integration_f_s01.py doit contenir 'F-S01' dans ses docstrings")

    def test_deploiement_json(self):
        """Vérifie que DEPLOIEMENT.json contient les éléments attendus."""
        # Vérification du fichier
        self.assertTrue(os.path.exists('/opt/data/ateliers/minecraft-py/DEPLOIEMENT.json'))
        
        # Lecture du contenu
        with open('/opt/data/ateliers/minecraft-py/DEPLOIEMENT.json', 'r') as f:
            content = f.read()
            
        self.assertIn('"port": "25565"', content, "Le fichier DEPLOIEMENT.json doit définir le port comme 25565")
        
        # Vérification avec rg (ne pas utiliser -q car cela peut échouer dans certains contextes)
        result = subprocess.run(['rg', '"\\/api\\/models"', '/opt/data/ateliers/minecraft-py/DEPLOIEMENT.json'], 
                                capture_output=True, text=True)
        
        # Vérifier que la commande a réussi (exit code 0) et qu'il y a une correspondance
        self.assertEqual(result.returncode, 0, f"Le fichier DEPLOIEMENT.json doit contenir '/api/models'\nErreur : {result.stderr}")
        self.assertIn('/api/models', result.stdout, "Le fichier DEPLOIEMENT.json doit contenir '/api/models'")

if __name__ == '__main__':
    unittest.main()