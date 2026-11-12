## Spécification : Persistance des chunks sur disque

### Objectif
Implémenter une persistance binaire versionnée des chunks (.bin.v1) avec sauvegarde à l'arrêt et restauration au redémarrage, conformément au CAHIER_DES_CHARGES.md.

### Fichiers à modifier/créer
- `world_manager.py`: Ajouter méthodes `save_chunk()`/`load_chunk()` utilisant `BlockID` et format binaire versionné (.bin.v1).
- `test_chunk_persistence.py`: Ajouter tests d'aller-retour (sauvegarder/charger chunk, vérifier intégrité post-redémarrage).

### Ce qui ne doit PAS changer
- Port serveur (25565) défini dans `DEPLOIEMENT.json`.
- Protocole JSON existant (protocole.py).
- Mécanisme de connexion client (client.py).

### Critères d'acceptation
```verifs
test -f DEPLOIEMENT.json ## attendu: succes
rg -q '25565' DEPLOIEMENT.json ## attendu: succes
test -f world_manager.py ## attendu: succes
rg -q 'def save_chunk' world_manager.py ## attendu: succes
test -f test_chunk_persistence.py ## attendu: succes
rg -q 'test_load_chunk' test_chunk_persistence.py ## attendu: succes
python3 -m pytest test_chunk_persistence.py ## attendu: succes
ls chunks/chunk_*.bin.v1 ## attendu: contient:chunk_0_0.bin.v1
file chunks/chunk_0_0.bin.v1 ## attendu: contient:binary
SPEC_FIN
```