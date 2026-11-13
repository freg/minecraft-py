#!/bin/bash

# Script de test pour F-I02

set -e 

echo "Démarrage du serveur..."
cd /opt/data/ateliers/minecraft-py/_deploiements/minecraft-py/serveur
python3 server.py &
SERVER_PID=$!

# Attendre que le serveur démarre
sleep 1

echo "Exécution du test F-I02..."
cd /opt/data/ateliers/minecraft-py
python3 -m unittest test_integration_f_i02.py

# Fermer le serveur
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null || true

echo "Test F-I02 terminé."