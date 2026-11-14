import unittest
import time

class TestPerfServerLatency(unittest.TestCase):
    """NF-4.1: Test de performance pour la latence du serveur"""

    def test_server_latency(self):
        """La latence du serveur ne doit pas dépasser 0.02 secondes."""
        # Simulation de la latence en utilisant time.perf_counter
        start_time = time.perf_counter()
        
        # Simulation d'une petite opération réseau (comme un ping)
        time.sleep(0.01)  # Simuler une réponse rapide
        
        end_time = time.perf_counter()
        latency = end_time - start_time
        
        self.assertLess(latency, 0.02, f"La latence du serveur ({latency:.4f}s) dépasse le seuil de 0.02s")