#!/bin/bash
mkdir -p /var/lib/apt/lists/partial
mkdir -p /opt/data/ateliers/_deploiements/minecraft-py/serveur
mkdir -p /opt/data/ateliers/_deploiements/minecraft-py/client
cp server.py /opt/data/ateliers/_deploiements/minecraft-py/serveur/
cp client.py /opt/data/ateliers/_deploiements/minecraft-py/client/
cp protocole.py /opt/data/ateliers/_deploiements/minecraft-py/serveur/
cp protocole.py /opt/data/ateliers/_deploiements/minecraft-py/client/
cp world_manager.py /opt/data/ateliers/_deploiements/minecraft-py/serveur/
cp world_manager.py /opt/data/ateliers/_deploiements/minecraft-py/client/
cp worldgen.py /opt/data/ateliers/_deploiements/minecraft-py/serveur/
cp worldgen.py /opt/data/ateliers/_deploiements/minecraft-py/client/
cp test*.py /opt/data/ateliers/_deploiements/minecraft-py/client/
cp qa_cdc.py /opt/data/ateliers/_deploiements/minecraft-py/client/
test -f /opt/data/ateliers/_deploiements/minecraft-py/serveur/server.py || exit 1
test -f /opt/data/ateliers/_deploiements/minecraft-py/client/client.py || exit 1