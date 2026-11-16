import unittest
import subprocess
import os

class TestNF42(unittest.TestCase):
    """
    NF-4.2: Sécurité et Robustesse
    """

    @classmethod
    def setUpClass(cls):
        # Vérifier que le fichier DEPLOIEMENT.json existe
        assert os.path.isfile('DEPLOIEMENT.json'), "Le fichier DEPLOIEMENT.json est introuvable."
        
        # Vérifier les paramètres de configuration
        result = subprocess.run(['jq', '-e', '.server.port == 25565 and .api_path == "/api/models"', 'DEPLOIEMENT.json'], 
                                capture_output=True, text=True)
        assert result.returncode == 0, f"Erreur dans la configuration de DEPLOIEMENT.json : {result.stderr}"

    def test_configuration_check(self):
        """NF-4.2: Vérifie la configuration du serveur"""
        # Vérifier que le fichier DEPLOIEMENT.json existe et contient les bonnes valeurs
        assert os.path.isfile('DEPLOIEMENT.json'), "Le fichier DEPLOIEMENT.json est introuvable."
        
        # Vérifier avec jq
        result = subprocess.run(['jq', '-e', '.server.port == 25565 and .api_path == "/api/models"', 'DEPLOIEMENT.json'], 
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Erreur dans la configuration de DEPLOIEMENT.json : {result.stderr}")


if __name__ == '__main__':
    unittest.main()