# 📄 Format des Messages Réseau

## 📦 Formats JSON pour chaque type de Message

### 1. `JOIN`
```json
{
  "type": "JOIN",
  "payload": {
    "username": "string",
    "version": "string"
  }
}
```

### 2. `AUTH`
```json
{
  "type": "AUTH",
  "payload": {
    "token": "string"
  }
}
```

### 3. `PLAYER_MOVE`
```json
{
  "type": "PLAYER_MOVE",
  "payload": {
    "x": "number",
    "y": "number",
    "z": "number",
    "orientation": "string"
  }
}
```

### 4. `MINING_ATTEMPT`
```json
{
  "type": "MINING_ATTEMPT",
  "payload": {
    "x": "number",
    "y": "number",
    "z": "number"
  }
}
```

### 5. `PLACE_ATTEMPT`
```json
{
  "type": "PLACE_ATTEMPT",
  "payload": {
    "x": "number",
    "y": "number",
    "z": "number",
    "block_id": "string"
  }
}
```

### 6. `BLOCK_UPDATE`
```json
{
  "type": "BLOCK_UPDATE",
  "payload": {
    "x": "number",
    "y": "number",
    "z": "number",
    "old_block_id": "string",
    "new_block_id": "string"
  }
}
```

### 7. `CHUNK_LOADED`
```json
{
  "type": "CHUNK_LOADED",
  "payload": {
    "chunk_x": "number",
    "chunk_z": "number",
    "blocks": [
      {
        "x": "number",
        "y": "number",
        "z": "number",
        "block_id": "string"
      }
    ]
  }
}
```

### 8. `PLAYER_JOINED`
```json
{
  "type": "PLAYER_JOINED",
  "payload": {
    "username": "string",
    "player_id": "string"
  }
}
```

## 🧪 Codes d'Erreur Possibles

- **400 Bad Request**: Format JSON invalide ou champ manquant.
- **401 Unauthorized**: Authentification échouée (`AUTH`).
- **403 Forbidden**: Action non autorisée (ex: placement à l'intérieur d'un bloc).
- **404 Not Found**: Coordonnées invalides pour `MINING_ATTEMPT` ou `PLACE_ATTEMPT`.
- **500 Internal Server Error**: Erreur dans le serveur pendant traitement.