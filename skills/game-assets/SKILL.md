---
name: game-assets
description: Produce game-ready 2D assets for a casual web game with an image model plus code - a locked style, sprite and prop families drawn as one sheet on a chroma background, automatic cutout and slicing, consistent sizes, code-drawn UI and particles, sound effects, fonts, licences, provenance and a size budget. Use for "make sprites", "game art", "generate game assets", "sprite sheet", "props", "icons for the game", "cut out the background", "game sound effects", "make the cover art". Not for deciding the look (use game-art-direction first) or for 3D models.
---

# Game assets

Verified pipeline (24 Oct 2026): one image-model call drew six matching props on a magenta sheet in about 2 minutes, and `scripts/cutout.py` turned it into six clean sprites in 4 seconds, with no halo on light or dark backgrounds.

## Rules

1. **Original art only.** Our own characters and designs. Never prompt for a well-known character, brand, logo or another game's style by name.
2. **Lock the style with references, not words alone.** Every prompt names 1-3 approved reference images and repeats the same style sentence verbatim (keep it in `art/style.txt`).
3. **Families, not singles.** Draw related assets together on one sheet (props, icons, characters' poses) so palette and line weight match. One image per prompt drifts.
4. **Never trust the requested hex.** Models miss it (asked #FF00FF, got #FC4FF9). The cutout script samples the real background.
5. **Text is set in code.** Ask the model for "no text, no letters". Titles, labels and numbers are fonts.
6. **Record provenance** for every shipped file in `ASSETS.md`: tool, date, prompt file, references, licence. Poki may ask for the process.

## Steps

1. **Plan.** List every asset in `ASSETS.md` grouped into families (characters, props, icons, backgrounds, UI, sfx, music) with target height in px and where it appears. Mark what is code-drawn: UI panels, buttons, icons with simple shapes, particles, gradients and most backgrounds are better in SVG/CSS/canvas (Rough.js for a hand-drawn line, with a fixed seed).
2. **Draw a family sheet.** Prompt pattern (`assets/sheet-prompt.txt` has the full template): "A sprite sheet of N separate [things] for a [genre] game, in a neat C by R grid with lots of empty space between them, same size, same [view] view: 1) ... N) .... [STYLE SENTENCE]. The background must be one perfectly flat solid [magenta or green] colour everywhere, no shadows, no floor, no texture, no text. Objects must not touch each other or the edges." Pick the chroma colour that appears in none of the objects (magenta for green characters, green otherwise). Run at most 2 image jobs at once.
3. **Cut out:** `python3 scripts/cutout.py sheet.png --out sprites/ --names a,b,c --height 256`. It prints the sampled background, writes one PNG per object in reading order, and `_check.png` on light and dark. Read `_check.png`. Fringe: raise `--tol`. Eaten outlines: lower it. Bits split off (steam, leaves): raise `--gap`. If the count is wrong, it warns.
4. **Review the family** at game scale with the game-art-direction checklist (consistency checks 11-15). Redraw the odd one out from the same references; never patch pixels.
5. **Characters that animate:** draw a pose sheet (idle, happy, surprised, working) as one family, then animate in code: squash and stretch, bob, blink, tilt. Frame-by-frame from image models stops matching after 4-6 frames.
6. **Audio.** Sound effects from ZzFX or jsfxr (generated in code, no licence issues, tiny). Music optional: CC0 packs, or a paid AI music plan with its terms saved. Normalise loudness; ship OGG plus MP3 or one MP3.
7. **Fonts.** One display font and one body font, both OFL (Google Fonts/Fontsource), bundled locally and subset to woff2.
8. **Pack and budget.** WebP for raster art (lossless for flat cartoon art), atlas at most 2048 px. `node ../portal-launch/scripts/check-build.mjs dist` fails over the budget.
9. **Covers** come from the same art: see portal-launch (`make-covers.py`).

Depth, library licences (Kenney CC0, game-icons CC BY, OpenGameArt traps), audio terms and portal AI rules: `references/asset-pipeline.md`.

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| Halo around sprites | Tolerance too low, or shadow on the background | `--tol 80`, and ask for "no shadows" |
| Outline eaten | Tolerance too high, or chroma colour close to the outline | Lower `--tol`, switch chroma colour |
| Character off-model | Model redrew from memory | Fewer words, name the reference file, describe shapes, not "a robot" |
| Two objects merged | Drawn touching | "lots of space between them", or lower `--gap` |
| Agent wrapper loops or times out | It inspects and refines its own output | Say "generate once and save it; do not inspect or refine" |
| Text in the art | Model added labels | "no text, no letters" and set text in code |
