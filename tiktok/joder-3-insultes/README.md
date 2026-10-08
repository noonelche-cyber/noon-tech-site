# TikTok ¡JODER! — « 3 insultes espagnoles que Duolingo ne t'apprendra JAMAIS »

Vidéo 1080×1920, ~29 s, animée en HTML et rendue image par image.

## Pipeline
1. **Voix off** → `vo_s1.wav` … `vo_s5.wav` (une réplique par scène, textes dans `tts.py`).
   - Actuel : Piper hors-ligne (`tts.py`, voix fr-siwis, trop robotique).
   - Prochaine étape : Azure TTS `fr-FR-RemyMultilingualNeural`
     (nécessite `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION` et l'accès réseau à `*.tts.speech.microsoft.com`).
     Si les fichiers s'appellent `vo_sN.wav`, retirer l'accélération `atempo` / adapter `load()` dans `build.py`.
2. `python3 build.py` → recalcule `timeline.js` sur les durées des voix + mixe les bruitages (`mix_vo.wav`, `mix_sfx.wav`).
3. `node render.js video` → `frames/` (Playwright/Chromium) ; `node render.js stills 2 7 24` pour des aperçus.
4. Encodage :
   `ffmpeg -framerate 30 -i frames/f%05d.jpg -i mix_vo.wav -af loudnorm=I=-14:TP=-1.5 -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -b:a 192k -movflags +faststart -shortest out.mp4`

Polices : Permanent Marker, Anton (Google Fonts, OFL).
