#!/usr/bin/env python3
"""
Prépare la liste de la galerie : media/galerie.json (lue par le site). Rien n'est redimensionné ni coupé.

Nom des fichiers :  CATÉGORIE - outil - titre.png       (ex : SPOTIFY - Chaise - Mon titre.png)
  - la catégorie est créée toute seule ; même nom = même catégorie (SPOTIFY et spotify, c'est la même)
  - sans outil :  CATÉGORIE - titre.png      sans rien :  titre.png (visible seulement dans "Tout")
  - pour choisir l'ordre, mets un numéro devant :  01 - SPOTIFY - Chaise - Mon titre.png

Photos : l'original est affiché tel quel.
Vidéos : la photo de couverture est celle que tu ajoutes toi-même dans media/mini/, avec le MÊME NOM que la vidéo
         (ex : media/SPOTIFY - Chaise - Pub.mp4  ->  media/mini/SPOTIFY - Chaise - Pub.png)
"""
import json
import re
from pathlib import Path

MEDIA = Path("media")
MINI = MEDIA / "mini"
IMAGES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
VIDEOS = {".mp4", ".webm", ".mov"}
COUVERTURES = [".jpg", ".jpeg", ".png", ".webp", ".avif"]


def majuscules(texte):
    """figma -> Figma, after effects -> After Effects (seulement si tout est en minuscules)."""
    texte = texte.replace("_", " ").strip()
    if texte != texte.lower():
        return texte
    return " ".join(m[:1].upper() + m[1:] for m in texte.split())


def analyser(nom):
    """'SPOTIFY - Chaise - Mon titre' -> ('SPOTIFY', 'Chaise', 'Mon titre')"""
    parts = [x.strip() for x in re.split(r"\s+[-–—]\s+", nom) if x.strip()]
    if len(parts) >= 3 and parts[0].isdigit():  # "01 - " devant le nom : sert seulement à ordonner
        parts = parts[1:]
    if len(parts) >= 3:
        return parts[0], majuscules(parts[1]), " - ".join(parts[2:])
    if len(parts) == 2:
        return parts[0], "", parts[1]
    titre = re.sub(r"[-_]+", " ", parts[0] if parts else nom).strip()
    return "", "", titre[:1].upper() + titre[1:]


def cle_tri(chemin):
    """Tri naturel : 2 avant 10, sans tenir compte des majuscules."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", chemin.lower())]


def main():
    couvertures = {}
    if MINI.exists():
        for p in MINI.rglob("*"):
            if p.is_file() and p.suffix.lower() in COUVERTURES:
                couvertures[p.relative_to(MINI).as_posix().lower()] = p.relative_to(MEDIA).as_posix()

    fichiers = []
    for p in MEDIA.rglob("*"):
        if not p.is_file() or MINI in p.parents or p.suffix.lower() not in IMAGES | VIDEOS:
            continue
        rel = p.relative_to(MEDIA).as_posix()
        if re.search(r"[#?%]", rel):
            print(f"  ! ignoré (caractère # ? ou % dans le nom) : {rel}")
            continue
        fichiers.append(rel)
    fichiers.sort(key=cle_tri)

    analyses = {rel: analyser(Path(rel).stem) for rel in fichiers}
    # même catégorie = même nom, majuscules ou pas. Le nom affiché est l'écriture la plus utilisée (à égalité : celle avec le plus de majuscules)
    ecritures = {}
    for cat, _, _ in analyses.values():
        if cat:
            ecritures.setdefault(cat.lower(), {}).setdefault(cat, 0)
            ecritures[cat.lower()][cat] += 1
    categories = {k: max(v, key=lambda e: (v[e], sum(c.isupper() for c in e))) for k, v in ecritures.items()}

    liste = []
    for rel in fichiers:
        cat, outil, titre = analyses[rel]
        if cat:
            cat = categories[cat.lower()]
        miniature = ""
        if Path(rel).suffix.lower() in VIDEOS:
            base = rel.rsplit(".", 1)[0].lower()
            miniature = next((couvertures[base + e] for e in COUVERTURES if base + e in couvertures), "")
            if not miniature:
                print(f"  ! pas de photo de couverture pour {rel} : ajoute media/mini/{rel.rsplit('.', 1)[0]}.png")
        liste.append({"fichier": rel, "categorie": cat, "outil": outil, "titre": titre, "miniature": miniature})

    (MEDIA / "galerie.json").write_text(json.dumps(liste, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Galerie : {len(liste)} créations, {len(categories)} catégories.")


if __name__ == "__main__":
    main()
