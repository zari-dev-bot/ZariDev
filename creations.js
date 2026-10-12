// =====================================================================
//  LISTE DE TES CRÉATIONS (galerie)
//
//  Pour AJOUTER une création :
//   1) dépose le fichier dans le dossier  media/
//      et sa petite version dans            media/mini/   (même nom de fichier)
//      (pour une vidéo : media/mini/NOM.mp4 = petit aperçu muet, media/mini/NOM.jpg = image fixe)
//   2) ajoute UNE ligne dans la liste ci-dessous, en copiant une ligne existante
//
//  categorie : 3d, mapper, vfx, gfx, ui, luau, ugc
//              (tu peux en mettre plusieurs séparées par un espace : "3d ugc")
//  outil     : ce qui s'affiche au clic ("Réalisé sur ...") : Blender, After Effects, Roblox Studio...
//  titre     : facultatif, décrit l'image (accessibilité)
//
//  L'ordre de la liste = l'ordre d'affichage dans la galerie.
//  Attention : garde bien la virgule à la fin de chaque ligne.
// =====================================================================

const DOSSIER_MEDIA = "media/";

const CREATIONS = [
  { fichier: "zari-herbe.jpg", categorie: "3d", outil: "Blender", titre: "Zari dans l'herbe, scène 3D" },
  { fichier: "edit-train.jpg", categorie: "3d", outil: "Blender", titre: "Édit : scène du train" },
  { fichier: "edit-know.jpg", categorie: "3d", outil: "Blender", titre: "Édit : KNOW en 3D" },
  { fichier: "banniere-lelouch.jpg", categorie: "gfx", outil: "After Effects", titre: "Bannière Lelouch pour Zari" },
  { fichier: "poteau-champ-de-force.jpg", categorie: "3d", outil: "Blender", titre: "Poteau barrière champ de force" },
  { fichier: "video-vfx-1.mp4", categorie: "vfx", outil: "Roblox Studio", titre: "Vidéo VFX 1" },
  { fichier: "video-vfx-2.mp4", categorie: "vfx", outil: "Roblox Studio", titre: "Vidéo VFX 2" },
  { fichier: "video-vfx-3.mp4", categorie: "vfx", outil: "Roblox Studio", titre: "Vidéo VFX 3" },
  { fichier: "epee-zari.jpg", categorie: "ugc", outil: "Blender", titre: "Épée Zari" },
  { fichier: "bouton-faire-un-don.webp", categorie: "ui", outil: "After Effects", titre: "Bouton « Faire un don », UI" },
];
