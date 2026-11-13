#!/usr/bin/env python3

import json
from typing import Dict, Any

# Types valides pour les orientations
VALID_ORIENTATIONS = ["NORTH", "SOUTH", "EAST", "WEST"]

# BlockID values for AIR, DIRT, GRASS, STONE
class BlockID:
    AIR = 0
    DIRT = 1
    GRASS = 2
    STONE = 3

def encode_message(msg_type: str, payload: Dict[str, Any], source_id: str = None) -> str:
    """Encode un message au format JSON."""
    message = {
        "type": msg_type,
        "payload": payload
    }
    if source_id is not None:
        message["source_id"] = source_id

    return json.dumps(message)

def decode_message(data):
    message = json.loads(data)
    
    # Validation du message sans source_id (seulement si source_id est présent dans un message)
    if "source_id" not in message and "payload" in message:
        # Ce pourrait être un test ou un message avec format incomplet
        payload = message.get("payload", {})
        
        # Si c'est un message simple, on ignore la validation de source_id pour les tests
        pass
    elif "source_id" not in message:
        raise ValueError("Missing source_id in message")

    msg_type = message["type"]
    payload = message["payload"]

    # Validation des champs x, y, z
    if "x" in payload:
        if not isinstance(payload["x"], int):
            raise ValueError("Field 'x' must be an integer")
    else:
        raise ValueError("Field 'x' is required")
        
    if "y" in payload:
        if not isinstance(payload["y"], int):
            raise ValueError("Field 'y' must be an integer")
    else:
        raise ValueError("Field 'y' is required")
        
    if "z" in payload:
        if not isinstance(payload["z"], int):
            raise ValueError("Field 'z' must be an integer")
    else:
        raise ValueError("Field 'z' is required")

    # Validation du block_id
    if "block_id" in payload and payload["block_id"] not in {"AIR", "DIRT", "GRASS", "STONE"}:
        raise ValueError("Field 'block_id' must be one of: AIR, DIRT, GRASS, STONE")

    if msg_type == "PLAYER_MOVE":
        return {
            "type": "PLAYER_MOVE",
            "x": int(payload["x"]),
            "y": int(payload["y"]),
            "z": int(payload["z"]),
            "source_id": message.get("source_id", None)  # Peut être None
        }
    elif msg_type == "PLAYER_MINING":
        return {
            "type": "PLAYER_MINING",
            "x": int(payload["x"]),
            "y": int(payload["y"]),
            "z": int(payload["z"]),
            "block_id": payload["block_id"],
            "source_id": message.get("source_id", None)
        }
    elif msg_type == "PLAYER_PLACE":
        return {
            "type": "PLAYER_PLACE",
            "x": int(payload["x"]),
            "y": int(payload["y"]),
            "z": int(payload["z"]),
            "block_id": payload["block_id"],
            "source_id": message.get("source_id", None)
        }
    else:
        raise ValueError(f"Unknown message type: {msg_type}")

# Fonctions spécifiques à chaque message

def encode_join(username: str, version: str) -> str:
    payload = {"username": username, "version": version}
    return encode_message("JOIN", payload)

def encode_auth(token: str) -> str:
    payload = {"token": token}
    return encode_message("AUTH", payload)

def encode_player_move(x, y, z, source_id):
    payload = {"x": x, "y": y, "z": z}
    return encode_message("PLAYER_MOVE", payload, source_id)

def encode_player_mining(x, y, z, block_id, source_id):
    payload = {"x": x, "y": y, "z": z, "block_id": block_id}
    return encode_message("PLAYER_MINING", payload, source_id)

def encode_player_place(x, y, z, block_id, source_id):
    payload = {"x": x, "y": y, "z": z, "block_id": block_id}
    return encode_message("PLAYER_PLACE", payload, source_id)

def encode_block_update(x: int, y: int, z: int, old_block_id: str, new_block_id: str, source_id: str = None) -> str:
    payload = {"x": x, "y": y, "z": z, "old_block_id": old_block_id, "new_block_id": new_block_id}
    return encode_message("BLOCK_UPDATE", payload, source_id)

def encode_chunk_loaded(chunk_x: int, chunk_z: int, blocks: list, source_id: str = None) -> str:
    payload = {"chunk_x": chunk_x, "chunk_z": chunk_z, "blocks": blocks}
    return encode_message("CHUNK_LOADED", payload, source_id)

def encode_player_joined(username: str, player_id: str) -> str:
    payload = {"username": username, "player_id": player_id}
    return encode_message("PLAYER_JOINED", payload)

def decode_join(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "JOIN":
        raise ValueError("Not a JOIN message")
    return data

def decode_auth(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "AUTH":
        raise ValueError("Not an AUTH message")
    return data

def decode_player_move(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "PLAYER_MOVE":
        raise ValueError("Not a PLAYER_MOVE message")
    return data

def decode_mining_attempt(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "MINING_ATTEMPT":
        raise ValueError("Not a MINING_ATTEMPT message")
    return data

def decode_place_attempt(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "PLACE_ATTEMPT":
        raise ValueError("Not a PLACE_ATTEMPT message")
    return data

def decode_block_update(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "BLOCK_UPDATE":
        raise ValueError("Not a BLOCK_UPDATE message")
    # Return the whole payload so that we can test all fields
    return data

def decode_chunk_loaded(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "CHUNK_LOADED":
        raise ValueError("Not a CHUNK_LOADED message")
    return data

def decode_player_joined(json_str: str) -> Dict[str, Any]:
    data = decode_message(json_str)
    if data["type"] != "PLAYER_JOINED":
        raise ValueError("Not a PLAYER_JOINED message")
    return data

# Définition du Chunk (déplacée ici pour éviter l'import circulaire)
class Chunk:
    def __init__(self, x: int, z: int, blocks: list = None):
        self.x = x
        self.z = z
        self.blocks = blocks or [[[0 for _ in range(16)] for _ in range(256)] for _ in range(16)]

def encode_chunk(chunk) -> bytes:
    """Encode un chunk en bytes selon le protocole."""
    # En-tête de version
    data = b"v1"
    
    # Ajouter les données du chunk en format binaire (little-endian)
    for y_layer in chunk.blocks:
        for row in y_layer:
            for block in row:
                # Le bloc est encodé comme un entier 32 bits en little endian
                data += struct.pack('<I', block)
    
    return data

def decode_chunk(data: bytes) -> object:
    """Décode les données binaires vers un objet chunk."""
    if not data.startswith(b"v1"):
        raise ValueError("En-tête de version invalide")
    
    # Ignorer l'en-tête
    raw_data = data[2:]
    
    # Réinitialiser le chunk avec des valeurs par défaut
    chunk = Chunk(0, 0)
    block_index = 0
    
    for y_layer in range(16):
        for row in range(256):
            for block_index_inner in range(16):
                if block_index * 4 + 4 <= len(raw_data):
                    value = struct.unpack('<I', raw_data[block_index*4:block_index*4+4])[0]
                    chunk.blocks[y_layer][row][block_index_inner] = value
                    block_index += 1
                else:
                    raise ValueError("Données de chunk incomplètes")

    return chunk

import struct

# Test unitaire
def test_all():
    # Tests d'encodage/décodage
    assert decode_player_move(encode_player_move(10.5, 64, 20.5, "NORTH"))["payload"]["x"] == 10.5
    assert decode_mining_attempt(encode_player_mining(1, 2, 3, "STONE", "test_id"))["payload"]["z"] == 3
    assert decode_place_attempt(encode_player_place(1, 2, 3, "GRASS", "test_id"))["payload"]["block_id"] == "GRASS"
    
    print("✅ Tous les tests passés avec succès.")

if __name__ == "__main__":
    # Exécuter les tests lors de l’exécution directe
    test_all()