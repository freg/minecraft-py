#!/usr/bin/env python3

import socket
import json
import asyncio
import threading
import sys
from protocole import *
from world_manager import WorldManager
import worldgen

# Configuration du serveur
HOST = '127.0.0.1'
PORT = 25565

# Enregistrement des joueurs connectés
connected_players = {}

# Initialisation du monde
world_manager = WorldManager()

def generer_monde_initial(graine, monde_plat):
    if monde_plat:
        # Générer un monde plat à y=64
        for cx in range(-1, 2):
            for cz in range(-1, 2):
                chunk = worldgen.generer_chunk(cx, cz, graine)
                world_manager.save_chunk(cx, cz, chunk)
    else:
        # Générer un monde déterministe avec la graine
        for cx in range(-1, 2):
            for cz in range(-1, 2):
                chunk = worldgen.generer_chunk(cx, cz, graine)
                world_manager.save_chunk(cx, cz, chunk)

def handle_client(client_socket, client_address):
    print(f"[+] Nouvelle connexion depuis {client_address}")
    
    try:
        # Envoyer un message de bienvenue ou configuration initiale
        welcome_msg = encode_message("WELCOME", {"server": "Minecraft-Py Server"})
        client_socket.send(welcome_msg.encode())
        
        while True:
            # Réception des messages du client
            data = client_socket.recv(1024).decode()
            if not data:
                break
                
            # Décode le message reçu
            try:
                msg = decode_message(data)
            except ValueError as e:
                print(f"[!] Erreur de décodage: {e}")
                continue
            
            msg_type = msg["type"]
            
            # Gestion du message JOIN
            if msg_type == "JOIN":
                username = msg["payload"]["username"]
                version = msg["payload"]["version"]
                
                # Enregistrer le joueur avec un ID aléatoire (ici simplifié)
                player_id = f"player_{len(connected_players) + 1}"
                connected_players[player_id] = {
                    "username": username,
                    "address": client_address,
                    "x": 0,
                    "y": 64,
                    "z": 0
                }
                
                # Charger les chunks autour du joueur
                world_manager.load_chunks_around_player(player_id, 0, 0)
                
                # Envoyer confirmation de connexion et ID du joueur
                response = encode_player_joined(username, player_id)
                client_socket.send(response.encode())
                
            elif msg_type == "PLAYER_MOVE":
                x = msg["payload"]["x"]
                y = msg["payload"]["y"]
                z = msg["payload"]["z"]
                orientation = msg["payload"]["orientation"]
                
                # Validation serveur des actions
                if world_manager.validate_action("PLAYER_MOVE", None, msg["payload"]):
                    print(f"[{client_address}] Mouvement reçu: {x}, {y}, {z}, {orientation}")
                    
                    # Mettre à jour la position du joueur
                    for pid, player in connected_players.items():
                        if player['address'] == client_address:
                            player['x'] = x
                            player['y'] = y
                            player['z'] = z
                            
                            # Charger chunks autour du joueur
                            world_manager.load_chunks_around_player(pid, x, z)
                            break

            elif msg_type == "MINING_ATTEMPT":
                x = msg["payload"]["x"]
                y = msg["payload"]["y"]
                z = msg["payload"]["z"]

                # Validation serveur des actions
                if world_manager.validate_action("MINING_ATTEMPT", None, msg["payload"]):
                    print(f"[{client_address}] Minage reçu: {x}, {y}, {z}")
                    
                    # Mettre à jour le monde
                    chunk = world_manager.get_chunk(x // 16, z // 16)
                    if (0 <= x % 16 < 16 and 0 <= y < 256 and 0 <= z % 16 < 16):
                        old_block = chunk.blocks[x % 16][y][z % 16]
                        chunk.blocks[x % 16][y][z % 16] = None
                        
                        # Envoyer une mise à jour du bloc miné aux joueurs proches
                else:
                    print(f"[{client_address}] Tentative de minage invalide: {x}, {y}, {z}")

            elif msg_type == "PLACE_ATTEMPT":
                x = msg["payload"]["x"]
                y = msg["payload"]["y"]
                z = msg["payload"]["z"]
                block_id = msg["payload"]["block_id"]

                # Validation serveur des actions
                if world_manager.validate_action("PLACE_ATTEMPT", None, msg["payload"]):
                    print(f"[{client_address}] Placement reçu: {x}, {y}, {z}, {block_id}")
                    
                    # Mettre à jour le monde
                    world_manager.update_block(x, y, z, block_id)
                else:
                    print(f"[{client_address}] Tentative de placement invalide: {x}, {y}, {z}, {block_id}")

            elif msg_type == "AUTH":
                token = msg["payload"]["token"]
                print(f"[{client_address}] Tentative d'authentification avec token: {token}")
                # Ici on pourrait vérifier le jeton
                
    except Exception as e:
        print(f"[!] Erreur pendant la communication avec {client_address}: {e}")

    finally:
        client_socket.close()
        print(f"[-] Déconnexion de {client_address}")


async def start_server():
    # Récupération des arguments de ligne de commande
    graine = 42
    monde_plat = False

    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv):
            if arg == "--graine":
                try:
                    graine = int(sys.argv[i+1])
                except (ValueError, IndexError):
                    print("Erreur: La graine doit être un entier.")
                    return
            elif arg == "--monde-plat":
                monde_plat = True

    # Générer le monde initial
    generer_monde_initial(graine, monde_plat)

    # Création du socket serveur
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    
    print(f"[+] Serveur démarré sur {HOST}:{PORT}")
    print(f"[+] Graine de génération: {graine}")
    print(f"[+] Mode monde plat: {monde_plat}")

    try:
        while True:
            # Accepter une nouvelle connexion
            client_socket, client_address = server.accept()
            
            # Gérer chaque client dans un thread séparé
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n[!] Serveur arrêté.")

if __name__ == "__main__":
    start_server()