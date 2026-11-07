#!/usr/bin/env python3

import socket
import json
import threading
from protocole import *

# Configuration du serveur
HOST = '127.0.0.1'
PORT = 25565

# Enregistrement des joueurs connectés
connected_players = {}

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
                    "address": client_address
                }
                
                # Envoyer confirmation de connexion et ID du joueur
                response = encode_player_joined(username, player_id)
                client_socket.send(response.encode())
                
            elif msg_type == "PLAYER_MOVE":
                x = msg["payload"]["x"]
                y = msg["payload"]["y"]
                z = msg["payload"]["z"]
                orientation = msg["payload"]["orientation"]

                # Ici on pourrait transmettre le mouvement à tous les autres joueurs ou le traiter
                print(f"[{client_address}] Mouvement reçu: {x}, {y}, {z}, {orientation}")

            elif msg_type == "MINING_ATTEMPT":
                x = msg["payload"]["x"]
                y = msg["payload"]["y"]
                z = msg["payload"]["z"]

                # Ici on gère l'attaque sur un block
                print(f"[{client_address}] Minage reçu: {x}, {y}, {z}")

            elif msg_type == "PLACE_ATTEMPT":
                x = msg["payload"]["x"]
                y = msg["payload"]["y"]
                z = msg["payload"]["z"]
                block_id = msg["payload"]["block_id"]

                # Ici on gère l’ajout d'un bloc
                print(f"[{client_address}] Placement reçu: {x}, {y}, {z}, {block_id}")

            elif msg_type == "AUTH":
                token = msg["payload"]["token"]
                print(f"[{client_address}] Tentative d'authentification avec token: {token}")
                # Ici on pourrait vérifier le jeton
                
    except Exception as e:
        print(f"[!] Erreur pendant la communication avec {client_address}: {e}")

    finally:
        client_socket.close()
        print(f"[-] Déconnexion de {client_address}")


def start_server():
    # Création du socket serveur
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    
    print(f"[+] Serveur démarré sur {HOST}:{PORT}")

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