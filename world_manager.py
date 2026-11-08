#!/usr/bin/env python3

import os

class Chunk:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        # Grille 16x256x16
        self.blocks = [[[None for _ in range(16)] for _ in range(256)] for _ in range(16)]

# Définition des identifiants de blocs
BlockID = {
    "AIR": 0,
    "DIRT": 1,
    "GRASS": 2,
    "STONE": 3
}

class WorldManager:
    def __init__(self, save_path="./chunks"):
        self.chunks = {}  # stockage des chunks par coordonnées (x, z)
        self.players = {}  # association joueur -> position (x, y, z)
        self.save_path = save_path
        
        # Créer le répertoire de sauvegarde s'il n'existe pas
        os.makedirs(save_path, exist_ok=True)

    def get_chunk(self, x, z):
        """Récupère un chunk existant ou le crée s'il n'existe pas."""
        if (x, z) not in self.chunks:
            self.chunks[(x, z)] = Chunk(x, z)
        return self.chunks[(x, z)]
    
    def load_chunks_around_player(self, player_id, x, z):
        """Charge les chunks autour de la position du joueur."""
        # On charge les chunks autour du joueur (par exemple dans un rayon de 2 chunks)
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                self.get_chunk(x // 16 + dx, z // 16 + dz)
    
    def purge_chunks_around_player(self, player_id, x, z):
        """Purge les chunks situés loin du joueur."""
        # Ici on pourrait implémenter une logique de purge des chunks éloignés
        pass
    
    def validate_action(self, action_type, player_id, payload):
        """Valide une action du client selon les règles du jeu."""
        if action_type == "MINING_ATTEMPT":
            x = payload["x"]
            y = payload["y"]
            z = payload["z"]
            
            # Vérifier que le bloc peut être miné
            chunk = self.get_chunk(x // 16, z // 16)
            if (0 <= x % 16 < 16 and 0 <= y < 256 and 0 <= z % 16 < 16):
                # Si le bloc n'est pas air, on peut le miner
                if chunk.blocks[x % 16][y][z % 16] is not None:
                    return True
            return False
        
        elif action_type == "PLACE_ATTEMPT":
            x = payload["x"]
            y = payload["y"]
            z = payload["z"]
            block_id = payload["block_id"]
            
            # Vérifier que l'emplacement est valide et qu'on peut placer le bloc
            if not (0 <= x % 16 < 16 and 0 <= y < 256 and 0 <= z % 16 < 16):
                return False
            
            chunk = self.get_chunk(x // 16, z // 16)
            
            # Vérifier que le bloc est un type valide (par exemple : pas d'air)
            if block_id in BlockID:
                if chunk.blocks[x % 16][y][z % 16] is None:  # On ne peut placer qu'à l'air
                    return True
            return False
        
        elif action_type == "PLAYER_MOVE":
            # Implémenter une validation de mouvement si nécessaire (collision, etc.)
            return True
            
        return False
    
    def update_block(self, x, y, z, block_id):
        """Met à jour un bloc dans le monde."""
        chunk = self.get_chunk(x // 16, z // 16)
        if 0 <= x % 16 < 16 and 0 <= y < 256 and 0 <= z % 16 < 16:
            chunk.blocks[x % 16][y][z % 16] = block_id

    def save_chunk(self, chunk_pos, chunk_data):
        """Sauvegarde un chunk en binaire dans un fichier."""
        filename = f"chunk_{chunk_pos[0]}_{chunk_pos[1]}.bin.v1"
        filepath = os.path.join(self.save_path, filename)
        
        # Écrire les données avec un header de version
        with open(filepath, "wb") as f:
            f.write(b"v1")  # Header de version
            f.write(chunk_data)

    def load_chunk(self, chunk_pos):
        """Charge un chunk depuis un fichier binaire."""
        filename = f"chunk_{chunk_pos[0]}_{chunk_pos[1]}.bin.v1"
        filepath = os.path.join(self.save_path, filename)
        
        if not os.path.exists(filepath):
            # Retourner None si le fichier n'existe pas
            return None
            
        with open(filepath, "rb") as f:
            header = f.read(2)  # Lire le header de version
            if header != b"v1":
                raise ValueError(f"Version inconnue du chunk : {header}")
            
            data = f.read()
            return data