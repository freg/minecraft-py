import random

def generer_chunk(cx, cz, graine):
    # Initialiser le générateur de nombres aléatoires avec la graine
    random.seed(graine + cx * 1000 + cz * 10000)
    
    # Création d'un chunk 16x256x16 rempli d'AIR
    chunk = [[[None for _ in range(16)] for _ in range(256)] for _ in range(16)]
    
    # Générer la hauteur du terrain entre 60 et 72 (inclus)
    hauteur_solo = random.randint(60, 73)
    
    # Remplir le chunk selon les couches
    for x in range(16):
        for z in range(16):
            for y in range(256):
                # Couche de STONE en profondeur
                if y < hauteur_solo - 3:
                    chunk[x][y][z] = 'STONE'
                # Couches de DIRT sur 3 blocs au-dessus du sol
                elif y < hauteur_solo:
                    chunk[x][y][z] = 'DIRT'
                # Couche de GRASS en surface
                elif y == hauteur_solo:
                    chunk[x][y][z] = 'GRASS'
                # AIR au-dessus
                else:
                    chunk[x][y][z] = None

    return type('Chunk', (), {'blocks': chunk})()