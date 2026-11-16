#!/usr/bin/env python3

import os
import mimetypes
import subprocess

def read_file(path, offset=1, limit=None):
    # Vérification du type de fichier avant lecture avec file --brief --mime-type
    try:
        result = subprocess.run(['file', '--brief', '--mime-type', path], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True, 
                                check=True)
        mime_type = result.stdout.strip()
        
        # Détection des fichiers binaires : si le type n'est ni text/ ni application/octet-stream
        # et qu'il ne s'agit pas d'une catégorie de fichiers non-textuels comme image/, video/, audio/
        if (not mime_type.startswith('text/') and 
            not mime_type == 'application/octet-stream' and 
            not mime_type.startswith(('image/', 'video/', 'audio/', 'application/'))):
            raise ValueError(f"read_file: fichier non textuel détecté: {path}")
    except subprocess.CalledProcessError:
        # Si la commande file échoue, on utilise la méthode fallback
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type and mime_type.startswith('text/'):
            pass  # C'est OK, c'est un fichier texte
        else:
            # Fallback final : vérification par extension pour les fichiers binaires
            binary_extensions = {'.bin', '.dat', '.exe', '.dll', '.so', '.class', '.jar'}
            _, ext = os.path.splitext(path)
            if ext.lower() in binary_extensions:
                raise ValueError(f"read_file: fichier non textuel détecté: {path}")
            # Pour les autres types de fichiers, on laisse la lecture se faire (potentiellement en erreur plus tard)
    
    # Lecture du fichier texte
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        total_lines = len(lines)
        start = max(0, offset - 1)
        end = start + limit if limit is not None else total_lines
        return ''.join(lines[start:end])