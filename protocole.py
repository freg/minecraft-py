import json
from typing import Dict, Any

# Types valides pour les orientations
VALID_ORIENTATIONS = ["NORTH", "SOUTH", "EAST", "WEST"]

def encode_message(msg_type: str, payload: Dict[str, Any], source_id: str = None) -> str:
    """Encode un message au format JSON."""
    message = {
        "type": msg_type,
        "payload": payload
    }
    if source_id is not None:
        message["source_id"] = source_id

    return json.dumps(message)

def decode_message(json_str: str) -> Dict[str, Any]:
    """Décode un message JSON en dictionnaire."""
    try:
        data = json.loads(json_str)
        if "type" not in data or "payload" not in data:
            raise ValueError("Missing 'type' or 'payload' field")
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

# Fonctions spécifiques à chaque message

def encode_join(username: str, version: str) -> str:
    payload = {"username": username, "version": version}
    return encode_message("JOIN", payload)

def decode_join(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "JOIN":
        raise ValueError("Not a JOIN message")
    return data

def encode_auth(token: str) -> str:
    payload = {"token": token}
    return encode_message("AUTH", payload)

def decode_auth(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "AUTH":
        raise ValueError("Not an AUTH message")
    return data

def encode_player_move(x: float, y: int, z: float, orientation: str) -> str:
    if orientation not in VALID_ORIENTATIONS:
        raise ValueError(f"Invalid orientation. Must be one of {VALID_ORIENTATIONS}")
    payload = {"x": x, "y": y, "z": z, "orientation": orientation}
    return encode_message("PLAYER_MOVE", payload)

def decode_player_move(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "PLAYER_MOVE":
        raise ValueError("Not a PLAYER_MOVE message")
    return data

def encode_mining_attempt(x: int, y: int, z: int) -> str:
    payload = {"x": x, "y": y, "z": z}
    return encode_message("MINING_ATTEMPT", payload)

def decode_mining_attempt(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "MINING_ATTEMPT":
        raise ValueError("Not a MINING_ATTEMPT message")
    return data

def encode_place_attempt(x: int, y: int, z: int, block_id: str) -> str:
    payload = {"x": x, "y": y, "z": z, "block_id": block_id}
    return encode_message("PLACE_ATTEMPT", payload)

def decode_place_attempt(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "PLACE_ATTEMPT":
        raise ValueError("Not a PLACE_ATTEMPT message")
    return data

def encode_block_update(x: int, y: int, z: int, old_block_id: str, new_block_id: str) -> str:
    payload = {"x": x, "y": y, "z": z, "old_block_id": old_block_id, "new_block_id": new_block_id}
    return encode_message("BLOCK_UPDATE", payload)

def decode_block_update(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "BLOCK_UPDATE":
        raise ValueError("Not a BLOCK_UPDATE message")
    return data

def encode_chunk_loaded(chunk_x: int, chunk_z: int, blocks: list) -> str:
    payload = {"chunk_x": chunk_x, "chunk_z": chunk_z, "blocks": blocks}
    return encode_message("CHUNK_LOADED", payload)

def decode_chunk_loaded(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "CHUNK_LOADED":
        raise ValueError("Not a CHUNK_LOADED message")
    return data

def encode_player_joined(username: str, player_id: str) -> str:
    payload = {"username": username, "player_id": player_id}
    return encode_message("PLAYER_JOINED", payload)

def decode_player_joined(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "PLAYER_JOINED":
        raise ValueError("Not a PLAYER_JOINED message")
    return data

# Test unitaire
def test_all():
    # Tests d'encodage/décodage
    assert decode_player_move(encode_player_move(10.5, 64, 20.5, "NORTH"))["payload"]["x"] == 10.5
    assert decode_mining_attempt(encode_mining_attempt(1, 2, 3))["payload"]["z"] == 3
    assert decode_place_attempt(encode_place_attempt(1, 2, 3, "GRASS"))["payload"]["block_id"] == "GRASS"
    
    print("✅ Tous les tests passés avec succès.")

if __name__ == "__main__":
    # Exécuter les tests lors de l’exécution directe
    test_all()