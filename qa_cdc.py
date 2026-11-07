#!/usr/bin/env python3
"""QA rejouable de minecraft-py, alignée sur CAHIER_DES_CHARGES.md.

Lancement (depuis la racine du projet) :
    python3 qa_cdc.py            # grille + détail des échecs
    python3 qa_cdc.py --json     # grille en JSON (pour l'atelier)

Chaque contrôle porte l'identifiant du cahier des charges (F-W01, F-S02...) ou de l'item
du backlog (P1..P5). Un fichier absent = contrôle en échec (fonction non livrée), pas sauté.
Hypothèse de transport, le protocole ne la précisant pas : un message JSON par ligne (\\n) sur TCP.
"""
import importlib, json, os, py_compile, socket, subprocess, sys, tempfile, time, traceback

RACINE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RACINE)
HOTE, PORT = "127.0.0.1", int(os.environ.get("QA_PORT", "25599"))
MESSAGES = ["JOIN", "AUTH", "PLAYER_MOVE", "MINING_ATTEMPT", "PLACE_ATTEMPT",
            "BLOCK_UPDATE", "CHUNK_LOADED", "PLAYER_JOINED"]
EXEMPLES = {
    "join": ("alice", "0.1"), "auth": ("jeton",),
    "player_move": (1.5, 64, 2.5, "NORTH"), "mining_attempt": (1, 60, 2),
    "place_attempt": (1, 65, 2, "STONE"), "block_update": (1, 65, 2, "AIR", "STONE"),
    "chunk_loaded": (0, 0, [{"x": 1, "y": 2, "z": 3, "block_id": "STONE"}]),
    "player_joined": ("alice", "p1"),
}
RESULTATS = []


def controle(ident, libelle):
    def deco(f):
        def lance():
            t0 = time.time()
            try:
                f()
                RESULTATS.append((ident, libelle, "OK", "", time.time() - t0))
            except Exception as e:  # tout échec est noté, la suite continue
                detail = f"{type(e).__name__}: {e}"
                if not isinstance(e, (AssertionError, FileNotFoundError)):
                    detail += "\n" + traceback.format_exc(limit=3)
                RESULTATS.append((ident, libelle, "ÉCHEC", detail, time.time() - t0))
        lance.ordre = len(CONTROLES)
        CONTROLES.append(lance)
        return lance
    return deco


CONTROLES = []


def exige(fichier):
    if not os.path.exists(os.path.join(RACINE, fichier)):
        raise FileNotFoundError(f"{fichier} absent (non livré)")


# ---------- outils réseau ----------
class Serveur:
    def __init__(self, donnees):
        exige("server.py")
        env = dict(os.environ, PORT=str(PORT), HOTE=HOTE, DATA_DIR=donnees, MONDE_DIR=donnees)
        self.p = subprocess.Popen([sys.executable, "server.py"], cwd=donnees_cwd(donnees), env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        fin = time.time() + 20
        while time.time() < fin:
            if self.p.poll() is not None:
                raise AssertionError("serveur arrêté au démarrage : " + self.p.stdout.read().decode()[-500:])
            try:
                socket.create_connection((HOTE, PORT), 0.5).close()
                return
            except OSError:
                time.sleep(0.2)
        self.stop()
        raise AssertionError("port TCP non ouvert en 20 s")

    def stop(self):
        if self.p.poll() is None:
            self.p.terminate()  # SIGTERM : laisse une chance de sauvegarder
            try:
                self.p.wait(5)
            except subprocess.TimeoutExpired:
                self.p.kill()


def donnees_cwd(donnees):
    """Le serveur tourne dans une copie du projet pour que ses fichiers de monde restent isolés."""
    cible = os.path.join(donnees, "projet")
    if not os.path.exists(cible):
        subprocess.run(["cp", "-r", RACINE, cible], check=True)
    return cible


class Client:
    def __init__(self, nom):
        self.s = socket.create_connection((HOTE, PORT), 3)
        self.tampon = b""
        self.envoie("JOIN", {"username": nom, "version": "0.1"})

    def envoie(self, t, payload):
        self.s.sendall((json.dumps({"type": t, "payload": payload}) + "\n").encode())

    def attend(self, type_voulu, delai=2.0, filtre=lambda m: True):
        fin = time.time() + delai
        while time.time() < fin:
            while b"\n" in self.tampon:
                ligne, self.tampon = self.tampon.split(b"\n", 1)
                try:
                    m = json.loads(ligne)
                except ValueError:
                    continue
                if m.get("type") == type_voulu and filtre(m):
                    return m
            self.s.settimeout(max(0.01, fin - time.time()))
            try:
                d = self.s.recv(65536)
            except socket.timeout:
                break
            if not d:
                break
            self.tampon += d
        return None

    def ferme(self):
        self.s.close()


def meme_bloc(x, y, z):
    return lambda m: (m["payload"].get("x"), m["payload"].get("y"), m["payload"].get("z")) == (x, y, z)


# ---------- P1 : protocole ----------
@controle("P1", "protocole.py compile")
def _():
    exige("protocole.py")
    py_compile.compile(os.path.join(RACINE, "protocole.py"), doraise=True)


@controle("P1", "aller-retour encode/décode des 8 messages")
def _():
    p = importlib.import_module("protocole")
    manquants = []
    for nom, args in EXEMPLES.items():
        enc, dec = getattr(p, "encode_" + nom, None), getattr(p, "decode_" + nom, None)
        if not (enc and dec):
            manquants.append(nom)
            continue
        m = dec(enc(*args))
        assert m["type"] == nom.upper(), nom
    assert not manquants, f"fonctions manquantes : {manquants}"


@controle("P1", "auto-test de protocole.py s'exécute")
def _():
    r = subprocess.run([sys.executable, "protocole.py"], cwd=RACINE, capture_output=True, text=True, timeout=10)
    assert r.returncode == 0, r.stderr.strip().splitlines()[-1] if r.stderr else f"code {r.returncode}"


@controle("P1", "tests unitaires découverts par la commande de DEPLOIEMENT.json")
def _():
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test*.py"],
                       cwd=RACINE, capture_output=True, text=True, timeout=60)
    assert "Ran 0 tests" not in r.stderr, "0 test trouvé (fonctions hors unittest.TestCase) : la commande échoue (code 5)"
    assert r.returncode == 0, r.stderr[-400:]


@controle("P1", "champ source_id du format § II.3 pris en charge")
def _():
    p = importlib.import_module("protocole")
    m = json.loads(p.encode_message("JOIN", {"username": "a", "version": "1"}, source_id="c1"))
    assert m.get("source_id") == "c1"
    assert "source_id" in json.loads(p.encode_join("a", "1")), "les encodeurs spécifiques ne transmettent jamais source_id"


@controle("F-S01", "décodage : type de message inconnu refusé")
def _():
    p = importlib.import_module("protocole")
    try:
        p.decode_message('{"type": "HACK", "payload": {}}')
    except ValueError:
        return
    raise AssertionError("type inconnu accepté")


@controle("F-S01", "décodage : champs de mauvais type refusés (x non numérique)")
def _():
    p = importlib.import_module("protocole")
    try:
        p.decode_place_attempt('{"type": "PLACE_ATTEMPT", "payload": {"x": "a", "y": null, "z": 3, "block_id": "LAVE"}}')
    except ValueError:
        return
    raise AssertionError("charge utile invalide acceptée (validation absente)")


# ---------- P2 : serveur ----------
@controle("F-W01", "Chunk 16x256x16")
def _():
    exige("world_manager.py")
    wm = importlib.import_module("world_manager")
    c = wm.Chunk(0, 0) if wm.Chunk.__init__.__code__.co_argcount > 1 else wm.Chunk()
    dims = tuple(getattr(c, a, None) for a in ("WIDTH", "HEIGHT", "DEPTH"))
    if None in dims:
        dims = tuple(getattr(wm, a, None) for a in ("CHUNK_X", "CHUNK_Y", "CHUNK_Z"))
    assert dims == (16, 256, 16), f"dimensions lues : {dims}"


@controle("F-W02", "BlockID : AIR, DIRT, GRASS, STONE")
def _():
    exige("world_manager.py")
    wm = importlib.import_module("world_manager")
    for n in ("AIR", "DIRT", "GRASS", "STONE"):
        assert hasattr(wm.BlockID, n), n


@controle("P2", "serveur démarre et répond à JOIN")
def _():
    with tempfile.TemporaryDirectory() as d:
        s = Serveur(d)
        try:
            c = Client("alice")
            rep = c.attend("PLAYER_JOINED") or c.attend("CHUNK_LOADED")
            c.ferme()
            assert rep, "aucune réponse PLAYER_JOINED/CHUNK_LOADED à JOIN en 2 s"
        finally:
            s.stop()


@controle("F-S01", "serveur : minage hors limites (y=999) refusé")
def _():
    with tempfile.TemporaryDirectory() as d:
        s = Serveur(d)
        try:
            c = Client("alice")
            c.envoie("MINING_ATTEMPT", {"x": 0, "y": 999, "z": 0})
            assert c.attend("BLOCK_UPDATE", 1.0) is None, "BLOCK_UPDATE émis pour y=999"
            c.ferme()
        finally:
            s.stop()


# ---------- P3 : client ----------
@controle("P3", "client.py --test se termine avec le code 0")
def _():
    exige("client.py")
    with tempfile.TemporaryDirectory() as d:
        s = Serveur(d)
        try:
            r = subprocess.run([sys.executable, "client.py", "--hote", HOTE, "--port", str(PORT), "--test"],
                               cwd=RACINE, capture_output=True, text=True, timeout=30)
            assert r.returncode == 0, (r.stdout + r.stderr)[-400:]
        finally:
            s.stop()


# ---------- P4 : persistance ----------
@controle("F-W03", "bloc placé retrouvé après redémarrage du serveur")
def _():
    with tempfile.TemporaryDirectory() as d:
        s = Serveur(d)
        try:
            c = Client("alice")
            c.envoie("PLACE_ATTEMPT", {"x": 3, "y": 70, "z": 3, "block_id": "STONE"})
            assert c.attend("BLOCK_UPDATE", 2, meme_bloc(3, 70, 3)), "placement non confirmé"
            c.ferme()
        finally:
            s.stop()
        s = Serveur(d)
        try:
            c = Client("bob")
            vu = c.attend("CHUNK_LOADED", 3, lambda m: any(
                (b.get("x"), b.get("y"), b.get("z")) == (3, 70, 3) and b.get("block_id") == "STONE"
                for b in m["payload"].get("blocks", [])))
            c.ferme()
            assert vu, "bloc absent des CHUNK_LOADED après redémarrage"
        finally:
            s.stop()


# ---------- P5 : multi-joueurs ----------
@controle("F-S02", "2 clients : B voit le bloc posé par A, < 200 ms")
def _():
    with tempfile.TemporaryDirectory() as d:
        s = Serveur(d)
        try:
            a, b = Client("alice"), Client("bob")
            time.sleep(0.3)
            t0 = time.time()
            a.envoie("PLACE_ATTEMPT", {"x": 5, "y": 70, "z": 5, "block_id": "STONE"})
            m = b.attend("BLOCK_UPDATE", 2, meme_bloc(5, 70, 5))
            dt = (time.time() - t0) * 1000
            a.ferme(); b.ferme()
            assert m, "B n'a reçu aucun BLOCK_UPDATE"
            assert dt < 200, f"latence {dt:.0f} ms"
        finally:
            s.stop()


@controle("§4.1", "5 clients connectés simultanément")
def _():
    with tempfile.TemporaryDirectory() as d:
        s = Serveur(d)
        try:
            cl = [Client(f"j{i}") for i in range(5)]
            rep = [c.attend("PLAYER_JOINED", 2) or c.attend("CHUNK_LOADED", 1) for c in cl]
            for c in cl:
                c.ferme()
            assert all(rep), f"{rep.count(None)} client(s) sans réponse"
        finally:
            s.stop()


def main():
    for c in CONTROLES:
        c()
    ok = sum(r[2] == "OK" for r in RESULTATS)
    if "--json" in sys.argv:
        print(json.dumps({"ok": ok, "total": len(RESULTATS), "controles": [
            {"id": i, "libelle": l, "etat": e, "detail": dt} for i, l, e, dt, _ in RESULTATS]}, ensure_ascii=False, indent=1))
    else:
        for i, l, e, dt, t in RESULTATS:
            print(f"{'✅' if e == 'OK' else '❌'} {i:6} {l}  ({t:.1f} s)")
        print(f"\nScore : {ok}/{len(RESULTATS)}")
        for i, l, e, dt, _ in RESULTATS:
            if e != "OK":
                print(f"\n--- {i} {l}\n{dt.strip()}")
    sys.exit(0 if ok == len(RESULTATS) else 1)


if __name__ == "__main__":
    main()
