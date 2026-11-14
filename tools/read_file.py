import os
import mimetypes

def read_file(path, offset=1, limit=None):
    # Vérification du type de fichier avant lecture
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type and mime_type.startswith('text/'):
        # Lecture du fichier texte
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            total_lines = len(lines)
            start = max(0, offset - 1)
            end = start + limit if limit is not None else total_lines
            return ''.join(lines[start:end])
    else:
        # Ignorer les fichiers binaires ou lever une erreur si nécessaire
        raise ValueError(f"Le fichier {path} n'est pas un fichier texte.")