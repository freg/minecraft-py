"""
F-I04
Test d'intégration pour la vérification du type de fichier.
"""
import unittest
import os
from tools.read_file import read_file

class TestIntegrationFI04(unittest.TestCase):
    def test_read_text_file(self):
        # Créer un fichier texte temporaire
        with open('temp_test_file.txt', 'w') as f:
            f.write('Ceci est un fichier texte de test.')
        
        # Vérifier que la méthode read_file peut lire le fichier
        content = read_file('temp_test_file.txt')
        self.assertEqual(content.strip(), 'Ceci est un fichier texte de test.')
        
        # Supprimer le fichier temporaire
        os.remove('temp_test_file.txt')

    def test_read_binary_file_raises_error(self):
        # Créer un fichier binaire temporaire (ex: image ou exécutable)
        with open('temp_test_binary.bin', 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01')

        # Vérifier que read_file lève une erreur pour les fichiers binaires
        with self.assertRaises(ValueError) as context:
            read_file('temp_test_binary.bin')
        
        self.assertIn("is binary, cannot be read as text", str(context.exception))
        
        # Supprimer le fichier temporaire
        os.remove('temp_test_binary.bin')

if __name__ == '__main__':
    unittest.main()