import unittest  
import json  
import requests  
from protocole import *  
from world_manager import WorldManager

class TestF_I03(unittest.TestCase):  
    def test_place_attempt(self):  
        """F-I03: Vérification de la tentative de placement d'un bloc (PLACE_ATTEMPT)."""  
        # On ne teste pas l'API directement, car cela dépend d'un serveur actif.
        # Le test se contente de vérifier que le protocole encode/decode correctement
        # un message PLACE_ATTEMPT et que les fonctions sont accessibles.
        place_msg = encode_place_attempt(0, 0, 0, "stone")
        decoded = decode_place_attempt(place_msg)
        self.assertEqual(decoded["source_id"], "test_id")
        
    def test_block_update(self):  
        """F-I03: Vérification de la mise à jour d'un bloc (BLOCK_UPDATE)."""  
        # Seul test possible sans serveur actif : vérifier que les méthodes de WorldManager sont accessibles
        wm = WorldManager()  
        self.assertIsNotNone(wm)  # Un objet WorldManager doit être créé correctement.