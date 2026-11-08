#!/usr/bin/env python3

import socket
import sys
import argparse
from protocole import *

class GameClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.inventory = [None] * 9  # Inventaire de 9 slots

    def connect(self):
        """Connecte le client au serveur."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.connect((self.host, self.port))
            print(f"[+] Connecté au serveur {self.host}:{self.port}")
            
            # Réception du message de bienvenue
            welcome = self.socket.recv(1024).decode()
            msg = decode_message(welcome)
            if msg["type"] == "WELCOME":
                print("[+] Bienvenue sur le serveur")
                
                # Exemple d'envoi d'un message JOIN
                join_msg = encode_join("Player1", "1.0")
                self.socket.send(join_msg.encode())
                
                # Réception de confirmation
                response = self.socket.recv(1024).decode()
                msg = decode_message(response)
                if msg["type"] == "PLAYER_JOINED":
                    print(f"[+] Connecté en tant que joueur {msg['payload']['username']}")
                    
                    # Lancement de la boucle d'écoute des événements
                    self.handle_events()
                else:
                    print("Erreur de connexion au serveur")
            else:
                print("Erreur de connexion au serveur")

        except Exception as e:
            print(f"[!] Erreur de connexion : {e}")
        finally:
            if self.socket:
                self.socket.close()

    def send_move(self, x: float, y: int, z: float, orientation: str):
        """Envoie un message de déplacement au serveur."""
        move_msg = encode_player_move(x, y, z, orientation)
        self.socket.send(move_msg.encode())
        print(f"Envoi du mouvement à ({x}, {y}, {z}) vers {orientation}")

    def send_mining(self, x: int, y: int, z: int):
        """Envoie une tentative de minage au serveur."""
        mining_msg = encode_mining_attempt(x, y, z)
        self.socket.send(mining_msg.encode())
        print(f"Bloc miné à ({x}, {y}, {z})")

    def send_place(self, x: int, y: int, z: int, block_id: str):
        """Envoie une tentative de placement de bloc au serveur."""
        place_msg = encode_place_attempt(x, y, z, block_id)
        self.socket.send(place_msg.encode())
        print(f"Bloc placé à ({x}, {y}, {z}) avec ID {block_id}")

    def handle_events(self):
        """Boucle d'écoute des événements du serveur."""
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    break
                
                msg = decode_message(data)
                msg_type = msg["type"]
                
                if msg_type == "PLAYER_MOVE":
                    print("Réception d'un joueur se déplaçant")
                elif msg_type == "MINING_ATTEMPT":
                    print("Réception d'une tentative de minage")
                elif msg_type == "PLACE_ATTEMPT":
                    print("Réception d'une tentative de placement")
                elif msg_type == "BLOCK_UPDATE":
                    print("Réception d'une mise à jour de bloc")
                    # Exemple d'affichage dans l'inventaire
                    if 'payload' in msg and 'x' in msg['payload']:
                        x, y, z = msg['payload']['x'], msg['payload']['y'], msg['payload']['z']
                        print(f"Mise à jour du bloc en {x}, {y}, {z}")
                elif msg_type == "CHUNK_LOADED":
                    print("Réception d'un chunk chargé")
                elif msg_type == "PLAYER_JOINED":
                    print("Un joueur s'est joint au jeu")
                else:
                    print(f"Message inconnu : {msg_type}")
            except Exception as e:
                print(f"[!] Erreur lors de la réception d'événements : {e}")
                break

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
        client = GameClient(args.hote, args.port)
        client.connect()