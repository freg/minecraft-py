#!/usr/bin/env bash

set -e

# Définir les chemins
DEPLOIEMENT_DIR="/opt/data/ateliers/_deploiements/minecraft-py"
SERVEUR_DIR="${DEPLOIEMENT_DIR}/serveur"
CLIENT_DIR="${DEPLOIEMENT_DIR}/client"
TESTS_CLIENT_DIR="${CLIENT_DIR}/tests_client"

# Créer les répertoires
mkdir -p "${SERVEUR_DIR}"
mkdir -p "${CLIENT_DIR}"
mkdir -p "${TESTS_CLIENT_DIR}"

# Copier les fichiers serveur
cp server.py "${SERVEUR_DIR}/server.py"
cp protocole.py "${SERVEUR_DIR}/protocole.py"
cp world_manager.py "${SERVEUR_DIR}/world_manager.py"
cp worldgen.py "${SERVEUR_DIR}/worldgen.py"

# Copier le répertoire chunks
if [ -d "chunks" ]; then
    cp -r chunks "${SERVEUR_DIR}/chunks"
fi

# Copier les fichiers client
cp client.py "${CLIENT_DIR}/client.py"
cp protocole.py "${CLIENT_DIR}/protocole.py"
cp world_manager.py "${CLIENT_DIR}/world_manager.py"

# Copier le répertoire de tests clients (pour inclure tous les tests unitaires)
cp -r tests_client/* "${TESTS_CLIENT_DIR}/"

# Vérifier l'existence des fichiers essentiels avant de quitter
required_files=(
    "${SERVEUR_DIR}/server.py"
    "${CLIENT_DIR}/client.py"
    "${TESTS_CLIENT_DIR}/test_protocole.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "Erreur: Le fichier $file est requis mais n'existe pas."
        exit 1
    fi
done

echo "Déploiement terminé avec succès."