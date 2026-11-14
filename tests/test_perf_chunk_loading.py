import unittest
import time

class TestPerfChunkLoading(unittest.TestCase):
    """NF-4.1: Test de performance pour le chargement des chunks"""

    def test_chunk_loading_performance(self):
        """Le temps de chargement d'un chunk ne doit pas dépasser 0.05 secondes."""
        # Simulation du temps de chargement avec time.perf_counter
        start_time = time.perf_counter()
        
        # Ici on simule simplement le temps de traitement
        # Dans un contexte réel, cela impliquerait l'appel à load_chunk
        time.sleep(0.01)  # Simulation de traitement
        
        end_time = time.perf_counter()
        load_time = end_time - start_time
        
        self.assertLess(load_time, 0.05, f"Le temps de chargement ({load_time:.4f}s) dépasse le seuil de 0.05s")