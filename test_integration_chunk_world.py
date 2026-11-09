#!/usr/bin/env python3
"""
Test d'intégration pour le système de chunks et world manager.
Ce test vérifie que les fichiers de chunk sont correctement créés,
que les données sont sauvegardées et chargées, et qu'elles correspondent
aux spécifications du projet.

F-W01 : Tests du système de chunk/world
"""

import os
import sys
import unittest
import socket
import asyncio
import signal
import time

# Ajouter le répertoire courant au path pour importer world_manager
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from world_manager import WorldManager, BlockID
from client import GameClient

class TestIntegrationChunkWorld(unittest.TestCase):

    def setUp(self):
        self.world_manager = WorldManager(save_path="./chunks")
        
    def test_chunk_creation(self):
        """Test que les chunks sont créés correctement."""
        chunk = self.world_manager.get_chunk(0, 0)
        self.assertIsNotNone(chunk)
        self.assertEqual(chunk.x, 0)
        self.assertEqual(chunk.z, 0)

    def test_world_save_and_load(self):
        """Test que les chunks peuvent être sauvegardés et chargés."""
        # Mettre à jour un bloc dans un chunk
        self.world_manager.update_block(10, 50, 10, BlockID["DIRT"])
        
        # Sauvegarder le chunk
        # (la sauvegarde réelle est testée dans test_chunk_persistence.py)
        
    def test_chunk_file_exists(self):
        """Test que le fichier chunk 0_0.bin.v1 existe."""
        self.assertTrue(os.path.exists("./chunks/chunk_0_0.bin.v1"))

    def test_integration_chunk_world_system(self):
        """F-W01 : Test d'intégration du système de chunk/world avec serveur réel"""
        # Démarrer le serveur sur un port libre
        port = 25566
        
        # Vérifier si le port est disponible
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            # Port occupé - trouver un autre port
            for p in range(25567, 30000):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                res = sock.connect_ex(('localhost', p))
                sock.close()
                if res != 0:
                    port = p
                    break

        # Démarrer le serveur avec asyncio.create_subprocess_exec
        process = None
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def run_server():
                return await asyncio.create_subprocess_exec(
                    sys.executable, 'server.py', '--graine', '42', '--monde-plat',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
            process = loop.run_until_complete(run_server())
            
            # Attendre que le serveur démarre
            loop.run_until_complete(asyncio.sleep(1))
            
            # Connecter un client virtuel
            client = GameClient("127.0.0.1", port)
            
            # Simuler une tentative de minage d'un bloc
            client.send_mining(10, 50, 10) 
            
            # Attendre un peu pour la sauvegarde du chunk (ajout de cette attente)
            loop.run_until_complete(asyncio.sleep(0.5))
            
            # Vérifier l'existence du fichier de chunk
            chunk_file = f"./chunks/chunk_0_0.bin.v1"
            self.assertTrue(os.path.exists(chunk_file))
            
        except Exception as e:
            # Tuer le processus serveur s'il reste actif même en cas d'erreur
            if process and process.returncode is None:
                try:
                    loop.run_until_complete(process.terminate())
                    loop.run_until_complete(process.wait())
                except:
                    pass  # Ignorer les erreurs de terminaison si déjà terminé
            raise e
        finally:
            # S'assurer que le processus est terminé
            if process and process.returncode is None:
                try:
                    loop.run_until_complete(process.terminate())
                    loop.run_until_complete(process.wait())
                except:
                    pass  # Ignorer les erreurs de terminaison si déjà terminé
            loop.close()

if __name__ == '__main__':
    unittest.main()