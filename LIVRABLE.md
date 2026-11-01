# Livrable — minecraft-py

Jeu de construction virtuel type Minecraft en Python : serveur autoritaire + client, protocole JSON, chunks persistants (cahier des charges : CAHIER_DES_CHARGES.md dans le projet).

Produit par l'atelier de codage hermes-web 0.25.1 le 2026-11-01 18:25. Cahier des charges : `CAHIER_DES_CHARGES.md`.

## Items du backlog

- **Schéma des messages réseau (JSON)** — revue (priorité 1, 2 ronde(s))
  - demande : Depuis CAHIER_DES_CHARGES.md § II.3 : définir dans protocole.md + protocole.py le format exact de chaque message (JOIN, AUTH, PLAYER_MOVE, MINING_ATTEMPT, PLACE_ATTEMPT, BLOCK_UPDATE, CHUNK_LOADED, PLAYER_JOINED) : champs, types, exemples, erreurs. Critère : python3 -m py_compile protocole.py ; un test unitaire encode/décode chaque message.
  - ronde 1 : 2026-11-01 04:29 → **accepte** ; bilan : Le schéma JSON et l'implémentation des messages réseau sont validés avec des tests. Le blocage vient de commandes terminal avec flags dangereux (-e/-c) exécutées sans vérification utilisateur.
  - ronde 2 : 2026-11-01 05:12 → **accepte** ; bilan : Le schéma JSON des messages réseau a été validé par py_compile et rg. 6 fichiers ont été modifiés. Aucun blocage détecté lors de la vérification finale.
- **Squelette du serveur : WorldManager + boucle d'événements** — a_faire (priorité 2, 0 ronde(s))
  - demande : server.py + world_manager.py : classes Chunk (16x256x16), BlockID (AIR, DIRT, GRASS, STONE), WorldManager (chargement/purge des chunks autour des joueurs), boucle asyncio acceptant plusieurs clients, validation serveur des actions (autorité, § F-S01). Critère : le serveur démarre, accepte une connexion, répond à JOIN ; tests unitaires du WorldManager.
- **Squelette du client : GameClient (sans rendu graphique)** — a_faire (priorité 3, 0 ronde(s))
  - demande : client.py : classe GameClient (connexion, envoi PLAYER_MOVE/MINING_ATTEMPT/PLACE_ATTEMPT, réception des événements, inventaire 9 slots), interface texte pour l'instant (pas de moteur graphique, § V). Critère : un scénario client->serveur->client joué par un script de test.
- **Persistance des chunks sur disque** — a_faire (priorité 4, 0 ronde(s))
  - demande : Sauvegarde/restauration de l'état du monde (§ F-W03) dans un format binaire compact (pas pickle brut : format versionné), à l'arrêt et périodiquement. Critère : redémarrage du serveur avec le monde intact, test unitaire aller-retour.
- **Synchronisation multi-clients et banc de test à 2 joueurs** — a_faire (priorité 5, 0 ronde(s))
  - demande : Diffusion immédiate des BLOCK_UPDATE à tous les clients (§ F-S02), heartbeats et reconnexion (§ 4.2), prédiction simple côté client (§ F-S03). Critère : script lançant un serveur et deux clients, l'un place un bloc, l'autre le voit ; latence mesurée < 200 ms en local.

## Fichiers du projet (7)

- `.gitignore` (69 o)
- `CAHIER_DES_CHARGES.md` (8636 o)
- `DEPLOIEMENT.json` (746 o)
- `LIVRABLE.md` (3204 o)
- `protocole.md` (1786 o)
- `protocole.py` (4536 o)
- `test_protocole.py` (615 o)

## Historique git

- `4b26c80` 2026-11-01 18:12:53 — atelier : livrable
- `4eb2923` 2026-11-01 11:03:43 — atelier : validation
- `b3ac1d9` 2026-11-01 04:26:12 — état initial (atelier)
