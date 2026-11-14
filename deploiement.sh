#!/bin/bash
cd /opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/serveur
export PYTHONPATH="/opt/data/ateliers/minecraft-py:/opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/serveur"
# Kill any existing server on port 25565
kill -9 $(lsof -t -i:25565) 2>/dev/null || true
python3 server.py
cd /opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/client
export PYTHONPATH="/opt/data/ateliers/minecraft-py:/opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/client"
python3 client.py --hote 127.0.0.1 --port 25565 --test