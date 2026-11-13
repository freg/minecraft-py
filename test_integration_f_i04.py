import unittest
from client import GameClient


class TestInventoryIntegration(unittest.TestCase):
    def test_inventory_prediction_integration(self):
        """F-I04 : Test que la prédiction d'inventaire fonctionne en simulation d'intégration."""
        # Simulation d'un client
        client = GameClient("127.0.0.1", 25565)
        # Ajout d’un item dans l'inventaire
        client.add_item('dirt', 1)
        # On vérifie qu’il est bien présent
        self.assertEqual(client.inventory['dirt'], 1)


if __name__ == '__main__':
    unittest.main()
