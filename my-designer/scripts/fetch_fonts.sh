#!/usr/bin/env bash
# Usage: bash fetch_fonts.sh <folder-containing-carousel.html>
# Puts Cairo (Arabic + Latin) and Inter (Latin) variable fonts in <folder>/fonts/.
# Source: the google/fonts GitHub repo (works where fonts.googleapis.com is blocked).
set -euo pipefail
DEST="${1:-.}/fonts"
mkdir -p "$DEST"
BASE="https://raw.githubusercontent.com/google/fonts/main/ofl"
get() { # name url
  if [ -s "$DEST/$1" ]; then echo "ok   $1 (cached)"; return; fi
  if curl -fsSL --retry 2 -o "$DEST/$1" "$2"; then echo "ok   $1"; else echo "FAIL $1 — download it manually into $DEST"; rm -f "$DEST/$1"; fi
}
get Cairo.ttf "$BASE/cairo/Cairo%5Bslnt,wght%5D.ttf"
get Inter.ttf "$BASE/inter/Inter%5Bopsz,wght%5D.ttf"
# Optional Arabic alternatives (uncomment and change @font-face to use):
# get Tajawal-Black.ttf "$BASE/tajawal/Tajawal-Black.ttf"
# get IBMPlexSansArabic-Bold.ttf "$BASE/ibmplexsansarabic/IBMPlexSansArabic-Bold.ttf"
# get Almarai-ExtraBold.ttf "$BASE/almarai/Almarai-ExtraBold.ttf"
