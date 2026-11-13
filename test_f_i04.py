import unittest
from client import GameClient


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.client = GameClient("127.0.0.1", 25565)

    def test_add_item(self):
        """F-I04 : Test d'ajout d'item dans l'inventaire."""
        # Ajout d'un item
        self.client.add_item('dirt', 5)
        self.assertEqual(self.client.inventory['dirt'], 5)

    def test_remove_item(self):
        """F-I04 : Test de suppression d'item de l'inventaire."""
        # Ajout d’un item
        self.client.add_item('dirt', 5)
        # Suppression de l’item
        self.client.add_item('dirt', -5)
        self.assertEqual(self.client.inventory['dirt'], 0)


if __name__ == '__main__':
    unittest.main()
