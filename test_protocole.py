import protocole

# Test unitaire pour vérifier que toutes les fonctions encode/decode fonctionnent correctement
def test_all():
    # Tests d'encodage/décodage
    assert protocole.decode_player_move(protocole.encode_player_move(10.5, 64, 20.5, "NORTH"))["payload"]["x"] == 10.5
    assert protocole.decode_mining_attempt(protocole.encode_mining_attempt(1, 2, 3))["payload"]["z"] == 3
    assert protocole.decode_place_attempt(protocole.encode_place_attempt(1, 2, 3, "GRASS"))["payload"]["block_id"] == "GRASS"
    
    print("✅ Tous les tests passés avec succès.")

if __name__ == "__main__":
    test_all()