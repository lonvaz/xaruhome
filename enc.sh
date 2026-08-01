#!/bin/bash
# $1=src  $2=name  $3=start  $4=dur
SRC="$1"; N="$2"; SS="$3"; T="$4"
R=/home/claude/work/site/xaru
ffmpeg -v error -ss "$SS" -t "$T" -i "$SRC" -an -vf "scale=1920:-2:flags=lanczos,fps=25" \
  -c:v libx264 -preset slow -crf 25 -profile:v high -pix_fmt yuv420p -movflags +faststart \
  -y "$R/assets/video/$N.mp4"
ffmpeg -v error -ss "$SS" -t "$T" -i "$SRC" -an -vf "scale=1280:-2:flags=lanczos,fps=25" \
  -c:v libvpx-vp9 -crf 38 -b:v 0 -row-mt 1 -deadline good -cpu-used 4 \
  -y "$R/assets/video/$N.webm"
ffmpeg -v error -ss "$SS" -i "$SRC" -frames:v 1 -vf "scale=1920:-2:flags=lanczos" -q:v 3 \
  -y "$R/assets/img/xaru/video-posters/$N.jpg"
python3 - "$R/assets/img/xaru/video-posters/$N.jpg" <<'PY'
import sys
from PIL import Image
p=sys.argv[1]; im=Image.open(p).convert("RGB")
im.save(p.replace(".jpg",".webp"),"WEBP",quality=78,method=6)
PY
echo "$N mp4=$(du -k $R/assets/video/$N.mp4|cut -f1)K webm=$(du -k $R/assets/video/$N.webm|cut -f1)K"
