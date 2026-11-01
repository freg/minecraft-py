<!-- Cahier des charges rédigé par google/gemma-4-e4b (LM Studio, yoga) le 01/11/2026 à la demande de Freg ; copié dans le dossier du projet par l'atelier -->

# 📄 Cahier des Charges : Développement d'un Système de Jeu de Construction Virtuel (Minecraft-Like)

## I. Introduction et Objectifs du Projet

### 1.1 Présentation Générale
Le projet vise la création d'une plateforme de jeu en monde ouvert, simulant l'expérience de construction et d'exploration libre telle que celle proposée par Minecraft. L'objectif est de construire un système robuste, jouable sur réseau (client-serveur), avec une forte emphase sur la gestion des données mondiales et la synchronisation entre les clients.

### 1.2 Objectifs Métier
*   **Construire un MVP (Minimum Viable Product) fonctionnel :** Permettre à deux joueurs connectés de construire, miner et voir leurs modifications apparaître en temps réel dans le monde partagé.
*   **Maîtriser la modélisation réseau des données 3D.**
*   **Développer une architecture scalable** permettant l'ajout futur d'éléments complexes (mobiles, mécanismes électriques).

### 1.3 Contraintes Techniques Majeures
*   **Langage Principal :** Python 3.x.
*   **Architecture :** Client/Serveur distincts.
*   **Réseau :** Utilisation de protocoles orientés messages (TCP ou UDP avec gestion des paquets).

## II. Architecture du Système

Le système doit être décomposé en trois modules indépendants mais fortement couplés par un protocole réseau strict.

### 2.1 Module Serveur (`server.py`)
*   **Rôle :** Cœur de la logique de jeu (Game Loop), gestion de l'état global du monde, autorité des actions des joueurs, et diffusion des événements.
*   **Responsabilités clés :** Sérialisation/Désérialisation des paquets, gestion des connexions clients, mise à jour de l'état du Chunk World.

### 2.2 Module Client (`client.py`)
*   **Rôle :** Interface utilisateur (GUI), rendu visuel en temps réel, capture d'entrées utilisateur et communication avec le serveur.
*   **Responsabilités clés :** Gestion de la caméra/vue de joueur, affichage du Chunk World reçu du serveur, transmission des intentions utilisateur (ex: "Miner bloc X à Y").

### 2.3 Protocole Réseau (API Inter-Module)
La communication doit se faire par un format de données standardisé (JSON est fortement recommandé). Le protocole doit être basé sur une gestion d'événements asynchrones :

*   **Format des messages :** `{ "type": "...", "payload": {...}, "source_id": "..." }`
*   **Canaux nécessaires :**
    1.  **Connexion/Authentification:** (Ex: `JOIN`, `AUTH`)
    2.  **Mouvement du joueur:** (Ex: `PLAYER_MOVE`, contenant les coordonnées et l'orientation.)
    3.  **Modification de monde:** (Ex: `BLOCK_UPDATE` ou `BLOCK_DESTROY`, contenant `{x, y, z}`, `old_block_id`, `new_block_id`).
    4.  **Événements du jeu:** (Ex: `CHUNK_LOADED`, `PLAYER_JOINED`).

## III. Périmètre Fonctionnel Détaillé (MVP)

### 3.1 Gestion et Représentation du Monde (Backend Serveur)

| ID | Fonctionnalité | Description Détaillée | Contraintes Techniques |
| :--- | :--- | :--- | :--- |
| **F-W01** | **Chunk World System** | Le monde doit être divisé en unités de $16 \times 256 \times 16$ blocs (Chunks). Seuls les chunks adjacents au joueur doivent être chargés et maintenus en mémoire. | Le système doit gérer l'instanciation, le stockage temporaire, et la purge des données de chunks non utilisés. |
| **F-W02** | **Blocs & ID** | Chaque bloc est identifié par un ID unique (`BlockID`). Les types minimum requis sont : Air (VIDE), Terre (GRASS/DIRT), Pierre (STONE). | Le système doit utiliser une structure de données 3D pour stocker le type de `BlockID` à chaque coordonnée $(x, y, z)$. |
| **F-W03** | **Persistance des Données** | L'état global du monde (l'ensemble des chunks) doit être sauvegardé sur disque et restauré au redémarrage du serveur. | Utilisation de sérialisation efficace (ex: Pickle ou un format binaire optimisé). |

### 3.2 Interaction Joueur-Monde (Client & Serveur)

| ID | Fonctionnalité | Description Détaillée | Protocole Réseau Impliqué |
| :--- | :--- | :--- | :--- |
| **F-I01** | **Déplacement de Base** | Le joueur peut se déplacer dans les 6 axes cardinaux (avant, arrière, gauche, droite) avec une vitesse définie. | `PLAYER_MOVE` message envoyé du Client vers le Serveur à intervalle régulier. |
| **F-I02** | **Minage de Blocs** | Le joueur vise un bloc et doit "miner" en cliquant/maintenant. L'action est initiée par le client, validée par le serveur (vérification des coordonnées). | Client $\to$ Serveur : `MINING_ATTEMPT` avec $(x, y, z)$. Serveur répond par l'émission d'un événement `BLOCK_UPDATE`. |
| **F-I03** | **Placement de Blocs** | Le joueur place un bloc devant lui. L'action est validée par le serveur pour éviter la triche. | Client $\to$ Serveur : `PLACE_ATTEMPT` avec $(x, y, z)$ et `BlockID`. Serveur valide et diffuse l'événement `BLOCK_UPDATE`. |
| **F-I04** | **Inventaire Simple** | Le client doit afficher une capacité limitée (ex: 9 slots) pour stocker les blocs minés. | Logique côté Client, mais la synchronisation des IDs de bloc est gérée par le Serveur. |

### 3.3 Synchronisation et Multijeu (Réseau)

| ID | Fonctionnalité | Description Détaillée | Priorité Technique |
| :--- | :--- | :--- | :--- |
| **F-S01** | **Autorité du Serveur** | Le serveur est l'unique autorité sur l'état du monde. Les modifications demandées par les clients sont des *suggestions* qui doivent être validées avant d'être appliquées et diffusées. | **Cruciale.** Prévention de la triche (ex: le joueur ne peut pas placer un bloc dans le vide). |
| **F-S02** | **Diffusion de Changement** | Lorsqu'un événement `BLOCK_UPDATE` se produit, le serveur doit immédiatement retransmettre cette modification à *tous* les autres clients connectés. | Gestion des flux d'événements en temps réel et optimisation pour ne transmettre que les coordonnées modifiées. |
| **F-S03** | **Gestion de la Latence** | Le client doit pouvoir prédire visuellement l'emplacement du joueur ou un bloc placé, même si le paquet serveur est en retard (client-side prediction). | Nécessite une interpolation simple des mouvements reçus. |

## IV. Contraintes Techniques et Non Fonctionnelles

### 4.1 Performance
*   **Latence Maximale Acceptable :** L'expérience de placement/destruction doit être quasi instantanée (< 200ms).
*   **Évolutivité (Scalability) :** Le système doit pouvoir supporter au minimum $N=5$ joueurs connectés simultanément sans dégradation majeure des performances.

### 4.2 Sécurité et Robustesse
*   **Gestion des erreurs réseau :** Implémentation de mécanismes de reconnexion automatique et gestion des paquets perdus (Heartbeats).
*   **Validation serveur stricte :** Toute donnée critique (coordonnées, ID bloc) doit être validée par le serveur pour prévenir les injections ou l'exploitation.

### 4.3 Stack Technique (Pour la Programmation IA)
*   **Bibliothèques Python recommandées :** `asyncio` ou `threading` (pour gérer plusieurs connexions réseau simultanément), des structures de données avancées (dictionnaires/hash maps pour les coordonnées).
*   **Structure de Code Attendue :** Utilisation intensive des classes et des modules séparés (ex: `world_manager.py`, `network_handler.py`).

## V. Périmètre d'Exclusion (Scope Boundaries)

Afin de garantir la livraison rapide du MVP, les fonctionnalités suivantes sont **hors périmètre** pour cette première phase :
1.  Système de combat ou projectile complexe.
2.  Créatures IA autonomes (mobs).
3.  Multithreading/Multi-processeurs avancés (le serveur peut commencer avec un modèle single-threaded efficace).
4.  Graphismes complexes ou rendu physique avancé (l'accent est mis sur la logique et le réseau, pas le moteur graphique AAA).

---
### Conclusion pour l'IA : Instructions de Développement

**Au vu de ce cahier des charges, je demande que vous génériez les éléments suivants en priorité :**

1.  **L'Architecture des Données (Data Schema) :** Définition précise du format JSON/Python utilisé pour les messages réseau (`PLAYER_MOVE`, `BLOCK_UPDATE`).
2.  **Le Squelette de Code Python :** Les classes principales et la boucle d'événement non fonctionnelles mais structurellement complètes pour le serveur (`WorldManager`) et le client (`GameClient`).
3.  **Les Interfaces API (API Contracts) :** La signature des fonctions clés que chaque module devra exposer pour pouvoir interagir ensemble de manière cohérente.
