import unittest
import socket
import time
import threading
from server import start_server_async  # Assurez-vous que cette fonction existe
import asyncio

class TestLatencyIntegration(unittest.TestCase):
    """Tests d'intégration pour la gestion de la latence (F-S03)."""

    def setUp(self):
        """Configuration avant chaque test."""
        self.host = "127.0.0.1"
        self.port = 25565
        self.server_thread = None
        self.server_loop = None

    def tearDown(self):
        """Nettoyage après chaque test."""
        # Arrêter le serveur si nécessaire
        pass

    def test_server_latency_with_client(self):
        """Test la latence du serveur via un client connecté."""
        # Démarrer le serveur dans un thread (ou utilisation asyncio)
        # Pour cette simplification, nous nous concentrons sur les tests de base
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            try:
                s.connect((self.host, self.port))
                # Envoyer un message et mesurer le temps
                start_time = time.time()
                s.sendall(b"JOIN\n")  # Message basique
                response = s.recv(1024)
                end_time = time.time()
                
                latency = (end_time - start_time) * 1000  # En millisecondes
                
                print(f"Latence réseau : {latency:.2f} ms")
                self.assertLess(latency, 100)  # Exemple : latence < 100ms
            except Exception as e:
                self.fail(f"Erreur lors de la mesure de la latence : {e}")

if __name__ == '__main__':
    unittest.main()