#!/bin/bash
# Smoke tests for the scripts. Needs node with playwright or playwright-core, python3 with pillow and numpy.
set -u
here=$(cd "$(dirname "$0")" && pwd); root=$(dirname "$here"); fail=0
echo "1. check-build should FAIL on the fixture (it references an external URL)"
if node "$root/skills/portal-launch/scripts/check-build.mjs" "$here/fixture-game" >/dev/null 2>&1; then echo "  FAIL: passed"; fail=1; else echo "  ok"; fi
echo "2. check-build should PASS with that host allowed"
node "$root/skills/portal-launch/scripts/check-build.mjs" "$here/fixture-game" --allow example.com >/dev/null || { echo "  FAIL"; fail=1; } && echo "  ok"
echo "3. shots.mjs captures 10 screenshots of the fixture"
out=$(mktemp -d); (cd "$here/fixture-game" && python3 -m http.server 4199 >/dev/null 2>&1 & echo $! > "$out/pid")
sleep 1
node "$root/skills/game-art-direction/scripts/shots.mjs" --url http://localhost:4199/ --out "$out/shots" --clicks 5 --wait 300 && [ "$(ls "$out/shots" | wc -l)" -eq 10 ] && echo "  ok" || { echo "  FAIL"; fail=1; }
kill "$(cat "$out/pid")" 2>/dev/null
echo "4. review-sheet.py builds a sheet"
python3 "$root/skills/game-art-direction/scripts/review-sheet.py" "$out/shots/1366x768-play.png" >/dev/null && [ -f "$out/shots/1366x768-play-review.png" ] && echo "  ok" || { echo "  FAIL"; fail=1; }
echo "5. cutout.py splits a generated 3-object sheet"
python3 - "$out/sheet.png" <<'PY'
import sys
from PIL import Image, ImageDraw
im = Image.new("RGB", (600, 220), (252, 79, 249)); d = ImageDraw.Draw(im)
for i, c in enumerate([(240, 200, 80), (120, 200, 160), (200, 120, 90)]):
    d.ellipse([30 + i * 200, 40, 170 + i * 200, 180], fill=c, outline=(60, 40, 30), width=6)
im.save(sys.argv[1])
PY
python3 "$root/skills/game-assets/scripts/cutout.py" "$out/sheet.png" --out "$out/sprites" --names a,b,c | grep -q "_check.png" && [ -f "$out/sprites/c.png" ] && echo "  ok" || { echo "  FAIL"; fail=1; }
rm -rf "$out"; exit $fail
