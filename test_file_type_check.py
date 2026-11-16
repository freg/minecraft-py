#!/usr/bin/env python3

import unittest
import subprocess
import os

class TestFileTypeCheck(unittest.TestCase):
    
    def test_binary_file_detection(self):
        """Test that binary files are correctly detected"""
        # Test on a binary file
        result = subprocess.run(['file', '--brief', '--mime-type', 'chunks/chunk_-1_-1.bin.v1'], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
        mime_type = result.stdout.strip()
        self.assertTrue(mime_type.startswith('application/') or mime_type == 'inode/x-empty' or 'binary' in mime_type.lower(), 
                        f"Expected binary file detection for chunk_-1_-1.bin.v1, got: {mime_type}")
    
    def test_json_file_detection(self):
        """Test that text files are correctly detected"""
        # Test on a JSON file
        result = subprocess.run(['file', '--brief', '--mime-type', 'DEPLOIEMENT.json'], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
        mime_type = result.stdout.strip()
        self.assertTrue(mime_type.startswith('application/json') or mime_type.startswith('text/'), 
                        f"Expected JSON file detection for DEPLOIEMENT.json, got: {mime_type}")
    
    def test_chunk_file_exists(self):
        # Vérification de l'existence du fichier avant lecture
        chunk_path = 'chunks/chunk_0_0.bin.v1'
        self.assertTrue(os.path.isfile(chunk_path), f"Le fichier {chunk_path} est requis mais n'existe pas.")

        # Utilisation de la commande file pour vérifier le type MIME
        result = subprocess.run(['file', '--brief', '--mime-type', chunk_path], capture_output=True, text=True)
        mime_type = result.stdout.strip()
        self.assertIn('application/octet-stream', mime_type, f"Le fichier {chunk_path} n'est pas un fichier binaire.")

    def test_file_command_availability(self):
        """Test that the 'file' command is available and can check file types."""
        # Vérifier que la commande 'file' est disponible
        result = subprocess.run(['which', 'file'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 0, "La commande 'file' n'est pas disponible.")
        
        # Test sur un fichier texte simple
        test_file = 'test_f_i04.py'
        if os.path.exists(test_file):
            result = subprocess.run(['file', '--brief', '--mime-type', test_file], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 0, f"Échec de la vérification du type de fichier pour {test_file}")
            # Assurer que le fichier est reconnu comme texte
            self.assertIn('text/', result.stdout.decode().strip())

if __name__ == '__main__':
    unittest.main()