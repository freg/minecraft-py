#!/usr/bin/env python3

import os
import magic

def read_file(path, offset=1, limit=None):
    # Vérification du type de fichier avant lecture : utilisation de magic.from_file
    if magic.from_file(path, mime=True).startswith('application/'):
        raise ValueError(f"File {path} is binary, cannot be read as text.")
    
    # Lecture du fichier texte
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        total_lines = len(lines)
        start = max(0, offset - 1)
        end = start + limit if limit is not None else total_lines
        return ''.join(lines[start:end])