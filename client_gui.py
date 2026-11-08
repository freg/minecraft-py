#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import socket
import sys
import argparse
import threading
import time
import json
from protocole import *

class MinecraftClientGUI:
    def __init__(self, host='127.0.0.1', port=25565, username='Player'):
        self.host = host
        self.port = port
        self.username = username
        self.socket = None
        self.running = False
        self.root = None
        self.canvas = None
        self.status_bar = None
        
        # États du monde (simulé pour l'instant)
        self.world_data = {}
        self.players = {}
        
        # Gestion des événements réseau
        self.event_handlers = {
            "CHUNK_LOADED": self.handle_chunk_loaded,
            "BLOCK_UPDATE": self.handle_block_update,
            "PLAYER_MOVE": self.handle_player_move,
            "PLAYER_JOINED": self.handle_player_joined,
            "PLACE_ATTEMPT": self.handle_place_attempt,
            "MINING_ATTEMPT": self.handle_mining_attempt
        }
        
        # Initialiser l'interface
        self.init_gui()
        
    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("Minecraft-Py Client")
        self.root.geometry("1024x768")
        
        # Canvas pour le monde
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="lightblue")
        self.canvas.pack(pady=10)
        
        # Barre de statut
        self.status_bar = tk.Label(self.root, text="Connecté", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Gestion des événements clavier
        self.root.bind('<Key>', self.handle_key_press)
        
    def handle_key_press(self, event):
        print(f"Key pressed: {event.keysym}")
    
    def connect_to_server(self):
        """Se connecte au serveur en utilisant un thread séparé."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.status_bar.config(text=f"Connecté à {self.host}:{self.port}")
            
            # Envoie le message JOIN avec le nom d'utilisateur
            join_msg = encode_join(self.username, "1.0")
            self.socket.send(join_msg.encode())
            
            # Démarrage de la réception des messages
            self.running = True
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
        except Exception as e:
            print(f"[Erreur] Impossible de se connecter au serveur : {e}")
            self.status_bar.config(text=f"Erreur de connexion: {e}")
    
    def receive_messages(self):
        """Reçoit les messages du serveur."""
        try:
            while self.running:
                data = self.socket.recv(4096).decode()
                if not data:
                    print("[Info] Déconnexion du serveur.")
                    break
                    
                try:
                    msg = decode_message(data)
                    msg_type = msg["type"]
                    payload = msg["payload"]
                    
                    print(f"[DEBUG] Message reçu: {msg_type} - {payload}")
                    
                    # Appeler le handler approprié
                    if msg_type in self.event_handlers:
                        self.event_handlers[msg_type](payload)
                    else:
                        print(f"[Info] Type de message non géré : {msg_type}")
                        
                except Exception as e:
                    print(f"[Erreur] Problème de décodage : {e}")
                    
        except Exception as e:
            print(f"[Erreur] Erreur réseau : {e}")
            self.status_bar.config(text=f"Erreur réseau: {e}")
            
    def handle_chunk_loaded(self, payload):
        """Gère le chargement d'un chunk."""
        # Affiche un message de chargement (simulé)
        print("[INFO] Chunk chargé")
        
    def handle_block_update(self, payload):
        """Gère la mise à jour d'un bloc."""
        print(f"[INFO] Bloc mis à jour : {payload}")
        
    def handle_player_move(self, payload):
        """Gère le déplacement du joueur."""
        print(f"[INFO] Joueur déplacé : {payload}")
        
    def handle_player_joined(self, payload):
        """Gère l'arrivée d'un joueur."""
        print(f"[INFO] Un joueur a rejoint : {payload}")
        
    def handle_place_attempt(self, payload):
        """Gère une tentative de placement de bloc."""
        print(f"[INFO] Tentative de placement : {payload}")
        
    def handle_mining_attempt(self, payload):
        """Gère une tentative d'exploitation de bloc."""
        print(f"[INFO] Tentative d'exploitation : {payload}")
    
    def start(self):
        """Démarre le client."""
        self.connect_to_server()
        self.root.mainloop()

def test_demarrage():
    """Test de démarrage sans connexion au serveur."""
    print("Test de démarrage : ouverture et fermeture automatique...")
    root = tk.Tk()
    root.geometry("1024x768")
    root.title("Test Démarrage")
    
    canvas = tk.Canvas(root, width=800, height=600, bg="lightblue")
    canvas.pack(pady=10)
    
    status_bar = tk.Label(root, text="Test de démarrage", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def exit_app():
        root.quit()
        
    root.after(2000, exit_app)
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Client Minecraft-Py avec interface graphique')
    parser.add_argument("--hote", help="Adresse IP du serveur", default='127.0.0.1')
    parser.add_argument("--port", type=int, help="Port du serveur", default=25565)
    parser.add_argument("--nom", help="Nom d'utilisateur", default='Player')
    parser.add_argument("--test-demarrage", action='store_true', help="Test de démarrage (ouvre la fenêtre puis quitte)")

    args = parser.parse_args()
    
    # Test de démarrage
    if args.test_demarrage:
        test_demarrage()
        sys.exit(0)
        
    client = MinecraftClientGUI(args.hote, args.port, args.nom)
    client.start()