#!/usr/bin/env python3

import socket
import json
import asyncio
import threading
import sys
import atexit
import time
import os
from protocole import *
from world_manager import WorldManager
import worldgen

# Configuration du serveur
HOST = os.environ.get("HOTE", "127.0.0.1")
PORT = int(os.environ.get("PORT", 25565))

# Enregistrement des joueurs connectés
connected_players = {}

# Initialisation du monde
world_manager = WorldManager()

def generer_monde_initial(graine, monde_plat):
    # Charger les chunks existants
    for cx in range(-1, 2):
        for cz in range(-1, 2):
            chunk_data = world_manager.load_chunk((cx, cz))
            if chunk_data is not None:
                # Pour ce test simple, on simule un chunk vide
                pass
            else:
                # Générer un chunk si aucun n'existe encore
                chunk = worldgen.generer_chunk(cx, cz, graine)
                # Sauvegarder le chunk généré en mémoire pour le moment
                world_manager.chunks[(cx, cz)] = chunk

    if monde_plat:
        # Générer un monde plat à y=64
        for cx in range(-1, 2):
            for cz in range(-1, 2):
                chunk = worldgen.generer_chunk(cx, cz, graine)
                # Utiliser la méthode existante pour sauvegarder le chunk
                world_manager.chunks[(cx, cz)] = chunk
    else:
        # Générer un monde déterministe avec la graine
        for cx in range(-1, 2):
            for cz in range(-1, 2):
                chunk = worldgen.generer_chunk(cx, cz, graine)
                # Utiliser la méthode existante pour sauvegarder le chunk
                world_manager.chunks[(cx, cz)] = chunk

def broadcast_message(message, exclude_player=None):
    """Diffuse un message à tous les clients connectés"""
    for player_id, player in connected_players.items():
        if player_id != exclude_player:
            try:
                player['socket'].send(message.encode())
            except Exception as e:
                print(f"[!] Erreur lors de l'envoi à {player['address']}: {e}")

def send_heartbeat(player_id):
    """Envoie un message heartbeat au joueur"""
    heartbeat_msg = encode_message("HEARTBEAT", {})
    try:
        connected_players[player_id]['socket'].send(heartbeat_msg.encode())
    except Exception as e:
        print(f"[!] Erreur lors de l'envoi du heartbeat à {player_id}: {e}")

def send_block_update(x, y, z, old_block_id, new_block_id):
    """Diffuse un BLOCK_UPDATE à tous les joueurs connectés"""
    update_msg = encode_block_update(x, y, z, old_block_id, new_block_id)
    broadcast_message(update_msg)

async def handle_client(reader, writer):
    client_address = writer.get_extra_info('peername')
    print(f"[+] Nouvelle connexion depuis {client_address}")
    
    try:
        # Envoyer un message de bienvenue ou configuration initiale
        welcome_msg = encode_message("WELCOME", {"server": "Minecraft-Py Server"})
        writer.write(welcome_msg.encode())
        await writer.drain()
        
        while True:
            # Réception des messages du client
            data = await reader.readline()
            if not data:
                break
                
            # Décode le message reçu
            try:
                msg = decode_message(data.decode())
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
                    "z": 0,
                    "socket": writer
                }
                
                # Charger les chunks autour du joueur
                world_manager.load_chunks_around_player(player_id, 0, 0)
                
                # Envoyer confirmation de connexion et ID du joueur
                response = encode_player_joined(username, player_id)
                writer.write(response.encode())
                await writer.drain()
                
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
                        send_block_update(x, y, z, old_block, None)
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
                    old_block = world_manager.update_block(x, y, z, block_id)
                    # Diffuser l'update
                    send_block_update(x, y, z, old_block, block_id)
                else:
                    print(f"[{client_address}] Tentative de placement invalide: {x}, {y}, {z}, {block_id}")

            elif msg_type == "AUTH":
                token = msg["payload"]["token"]
                print(f"[{client_address}] Tentative d'authentification avec token: {token}")
                # Ici on pourrait vérifier le jeton
                
    except Exception as e:
        print(f"[!] Erreur pendant la communication avec {client_address}: {e}")

    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            # Le writer est déjà fermé, rien à faire
            pass
        print(f"[-] Déconnexion de {client_address}")
        # Retirer le joueur de la liste des joueurs connectés
        for pid, player in connected_players.items():
            if player['address'] == client_address:
                del connected_players[pid]
                break

def check_and_reconnect():
    """Vérifie les connexions actives et tente de reconnexion si nécessaire"""
    # Cette fonction vérifierait les clients déconnectés
    # Pour l'instant, nous implémentons la structure mais ne faisons rien
    pass

async def start_server(port=25565):
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

    # Démarrage du serveur TCP avec asyncio
    server = await asyncio.start_server(handle_client, HOST, port)
    print(f"[+] Serveur démarré sur {HOST}:{port}")

    # Boucle d'écoute active
    async with server:
        await server.serve_forever()

def save_all_chunks():
    """Sauvegarde tous les chunks en mémoire vers le disque."""
    for (x, z), chunk in world_manager.chunks.items():
        # Simuler la conversion du chunk en bytes (ici nous faisons une approche simple)
        # Remplacer par une méthode réelle de sérialisation si nécessaire
        chunk_data = b"dummy_chunk_data_for_test_" + str((x, z)).encode()
        try:
            world_manager.save_chunk((x, z), chunk_data)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du chunk ({x}, {z}): {e}")

# Hook pour sauvegarder les chunks à l'arrêt du serveur
atexit.register(save_all_chunks)

if __name__ == "__main__":
    # Démarrage du serveur avec asyncio
    asyncio.run(start_server())