#!/bin/bash

# Vérifier si jq est installé
if ! command -v jq &> /dev/null; then
    echo "jq n'est pas installé. Installation en cours..."
    # Installer jq avec apt-get (nécessite sudo)
    sudo apt-get update
    sudo apt-get install -y jq
else
    echo "jq est déjà installé."
fi

# Créer le répertoire partiel s'il n'existe pas
sudo mkdir -p /var/lib/apt/lists/partial
sudo chmod -R 755 /var/lib/apt/lists/partial

echo "Installation terminée."