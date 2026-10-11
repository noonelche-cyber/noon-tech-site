#!/bin/bash
# usage: job.sh <lang> <vset>  — render, then compress for upload
set -e
cd "$(dirname "$0")"
LANG_CODE=$1 VSET=$2 python3 render3.py > out/log_$1_$2.txt 2>&1
f=out/joder_tiktok_$1_voix$2.mp4
ffmpeg -v error -y -i $f -c:v libx264 -preset slow -b:v 5M -maxrate 6M -bufsize 10M -pix_fmt yuv420p -c:a copy -movflags +faststart ${f%.mp4}_s.mp4
mv ${f%.mp4}_s.mp4 $f; rm -f out/$1/$2/video2.mp4
echo "$1 $2 $(du -h $f | cut -f1) $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)s"
