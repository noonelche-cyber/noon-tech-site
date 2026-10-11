# ¡JODER! video studio

Ce dossier génère les vidéos TikTok / Reels / Shorts et les affiches de ¡JODER!. Il n'est pas publié avec le site : à ne pas fusionner dans `main`.

À lire en premier : **[REGLES_VIDEOS.md](REGLES_VIDEOS.md)** (règles validées : prononciation de « ¡Joder! », public cible, format).

## Ce qu'il faut
- Python 3 avec `pillow` (raqm activé pour l'hébreu) et `numpy`, plus `ffmpeg`.
- Un accès Azure Speech (région `francecentral`). Dans une session Claude Code cloud, la clé est injectée par le proxy. En local, ajoute l'en-tête `Ocp-Apim-Subscription-Key` aux appels `curl` de `tts_lang.py` et `render_short.py`.

Toutes les commandes se lancent depuis ce dossier. Les résultats vont dans `out/`, qui n'est pas suivi par git.

## Série courte « L'insulte du jour » (10 à 15 s)
1. Ajoute un épisode dans `episodes.py` : `[accroche, §expression espagnole, littéral, sens, contexte, CTA]`. Le `§` indique une phrase dite par la voix espagnole.
2. `python3 render_short.py fr 4` produit `out/short/joder_short_fr_4.mp4`.
3. Pour un aperçu image : `python3 render_short.py fr 4 6.0 apercu.png` (image à 6 s).

## Vidéo longue multilingue (environ 35 s) et affiches
- Les textes de chaque langue sont dans `lang.py` (fr, en, de, it, nl, es, he, pt, pl).
- Pour générer les voix : `python3 tts_lang.py en A,B`.
- Pour générer une vidéo : `./job.sh en A` produit `out/joder_tiktok_en_voixA.mp4`.
- Pour générer les affiches : `python3 poster.py` (toutes les langues) ou `python3 poster.py fr,en`, dans `out/posters/`.

## Fichiers
| Fichier | Rôle |
|---|---|
| `prims.py` | Primitives graphiques : papier déchiré, taches, bulles, polices, hébreu de droite à gauche |
| `poster.py` | Affiche bêta-testeurs reconstruite, une par langue |
| `render3.py` | Vidéo longue en 5 scènes, avec l'affiche en plan final |
| `render_short.py` | Épisode court « insulte du jour » |
| `subs.py` | Calage des sous-titres sur les pauses de la voix |
| `tts_lang.py` | Voix Azure : jeu A (native + Espagnole) et jeu B (Espagnole seule) |
| `assets/` | Logo, affiche originale, photo de profil TikTok |
