#!/usr/bin/env python3

import socket
import sys
import argparse
from protocole import *

def connect_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f"[+] Connecté au serveur {host}:{port}")
        
        # Réception du message de bienvenue
        welcome = client_socket.recv(1024).decode()
        msg = decode_message(welcome)
        if msg["type"] == "WELCOME":
            print("[+] Bienvenue sur le serveur")
            
            # Exemple d'envoi d'un message JOIN
            join_msg = encode_join("Player1", "1.0")
            client_socket.send(join_msg.encode())
            
            # Réception de confirmation
            response = client_socket.recv(1024).decode()
            msg = decode_message(response)
            if msg["type"] == "PLAYER_JOINED":
                print(f"[+] Connecté en tant que joueur {msg['payload']['username']}")
                
                # Exemple d'envoi de mouvement
                move_msg = encode_player_move(10.0, 64, 20.0, "NORTH")
                client_socket.send(move_msg.encode())
                
                # Exemple d'attaque (mining)
                mining_msg = encode_mining_attempt(1, 2, 3)
                client_socket.send(mining_msg.encode())
                
                # Exemple de placement
                place_msg = encode_place_attempt(5, 6, 7, "STONE")
                client_socket.send(place_msg.encode())
                
        else:
            print("Erreur de connexion au serveur")

    except Exception as e:
        print(f"[!] Erreur de connexion : {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Client Minecraft-Py')
    parser.add_argument("--hote", help="Adresse IP du serveur", required=True)
    parser.add_argument("--port", type=int, help="Port du serveur", default=25565)
    parser.add_argument("--test", action='store_true', help="Exécuter des tests de base")
    
    args = parser.parse_args()
    
    if args.test:
        print("[-] Exécution des tests de base...")
        test_all()  # Test unitaire depuis protocole.py
    else:
        connect_client(args.hote, args.port)