#!/usr/bin/env python3
"""
Prépare la galerie à partir du dossier media/ :
  - media/mini/...        petites versions des images, image du milieu + petit extrait des vidéos
  - media/galerie.json    la liste lue par le site
GitHub lance ce script tout seul à chaque mise en ligne : rien à faire à la main.
"""
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageOps

MEDIA = Path("media")
MINI = MEDIA / "mini"
IMAGES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEOS = {".mp4", ".webm", ".mov"}
CATEGORIES = {"3d", "mapper", "vfx", "gfx", "ui", "luau", "ugc"}
# Outil affiché par défaut selon la catégorie (modifiable). Laisse vide pour ne rien afficher.
OUTILS = {"3d": "Blender", "ugc": "Blender", "vfx": "Roblox Studio", "mapper": "Roblox Studio", "luau": "Roblox Studio"}
LARGEUR = 480  # largeur des miniatures (assez net sur écran retina)


def joli_titre(nom_fichier):
    nom = re.sub(r"^\d+[-_ ]+", "", Path(nom_fichier).stem)  # "01-" au début sert juste à ordonner
    nom = re.sub(r"[-_]+", " ", nom).strip()
    return nom[:1].upper() + nom[1:]


def lire_infos():
    """media/infos.txt (facultatif) : fichier | catégorie | outil | titre. Les champs vides prennent la valeur automatique."""
    infos = {}
    f = MEDIA / "infos.txt"
    if not f.exists():
        return infos
    for ligne in f.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#"):
            continue
        p = [x.strip() for x in ligne.split("|")]
        infos[p[0]] = {
            "categorie": (p[1] if len(p) > 1 else "").lower(),
            "outil": p[2] if len(p) > 2 else "",
            "titre": " | ".join(p[3:]) if len(p) > 3 else "",
        }
    return infos


def mini_image(src, dest):
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            im.thumbnail((LARGEUR, 10000))
            ext = src.suffix.lower()
            if ext in (".jpg", ".jpeg"):
                im.convert("RGB").save(dest, "JPEG", quality=80, optimize=True, progressive=True)
            elif ext == ".webp":
                im.save(dest, "WEBP", quality=80)
            elif ext == ".gif":
                im.save(dest, "GIF")
            else:
                im.save(dest, "PNG", optimize=True)
    except Exception as e:  # le site prendra l'image d'origine à la place
        print(f"  ! miniature impossible pour {src} : {e}")


def duree(src):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def mini_video(src, rel):
    """Image du MILIEU de la vidéo + extrait de 4 s centré sur ce milieu (le site se cale au milieu de l'extrait)."""
    base = rel.rsplit(".", 1)[0]
    poster, clip = MINI / (base + ".jpg"), MINI / (base + ".mp4")
    if poster.exists() and clip.exists():
        return
    poster.parent.mkdir(parents=True, exist_ok=True)
    d = duree(src)
    mid = d / 2
    echelle = f"scale={LARGEUR}:-2"
    if not poster.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{mid:.2f}", "-i", str(src), "-frames:v", "1",
                        "-vf", echelle, "-q:v", "4", str(poster)])
    if not clip.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(0.0, mid - 2):.2f}", "-i", str(src), "-t", "4",
                        "-vf", echelle + ",fps=24", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "32",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(clip)])


def main():
    infos = lire_infos()
    trouves = {}
    for p in sorted(MEDIA.rglob("*")):
        if not p.is_file() or MINI in p.parents or p.suffix.lower() not in IMAGES | VIDEOS:
            continue
        rel = p.relative_to(MEDIA).as_posix()
        if re.search(r"[#?%]", rel):
            print(f"  ! ignoré (caractère # ? ou % dans le nom) : {rel}")
            continue
        trouves[rel] = p
    for rel in infos:
        if rel not in trouves:
            print(f"  ! infos.txt : fichier introuvable dans media/ : {rel}")

    # d'abord l'ordre de infos.txt, ensuite le reste par nom de fichier (préfixe "01-", "02-"... pour choisir l'ordre)
    ordre = [r for r in infos if r in trouves] + [r for r in trouves if r not in infos]
    liste = []
    for rel in ordre:
        src, info = trouves[rel], infos.get(rel, {})
        dossier = rel.split("/")[0].lower() if "/" in rel else ""
        cat = info.get("categorie") or (dossier if dossier in CATEGORIES else "")
        liste.append({
            "fichier": rel,
            "categorie": cat,
            "outil": info.get("outil") or OUTILS.get(cat, ""),
            "titre": info.get("titre") or joli_titre(rel.split("/")[-1]),
        })
        if src.suffix.lower() in IMAGES:
            mini_image(src, MINI / rel)
        else:
            mini_video(src, rel)

    (MEDIA / "galerie.json").write_text(json.dumps(liste, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Galerie : {len(liste)} créations.")


if __name__ == "__main__":
    main()
