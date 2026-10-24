---
name: game-art-direction
description: Make a 2D casual web game look professional and review whether it does - art direction brief, palette roles, outline and shading rules, chunky UI, typography, juice timings, portal cover and thumbnail look, and a 40-point screenshot review with scripts that capture the game at portal sizes and build grayscale and thumbnail-size test sheets. Use for "make the game look good", "art direction", "game UI looks amateur", "review these game screenshots", "polish", "juice", "game cover", "thumbnail". Not for producing the sprite files themselves (use game-assets) or for non-game websites.
---

# Game art direction

Professional casual games look finished because of consistency, not detail: one shape language, one outline rule, one light direction, one type scale, one spacing unit, everywhere. Amateur tells are mixed art sources, default fonts, flat rectangle buttons, low contrast and empty space.

## Rules

1. **Write the brief before any art.** No asset is produced until `ART.md` exists.
2. **Palette by role, not by taste:** background family, one action colour, one reward colour (gold, used only for value), one danger colour, two tinted darks for text and outlines. No pure #000 or #FFF.
3. **Pick one outline and shading system** and never mix: (a) thick dark outline + flat fill + one highlight and one shadow, (b) no outline + soft shading + rim light, (c) flat vector, no shading. Light from the top left on everything.
4. **Every input answers within one frame** in at least three channels (motion, sound, particles or flash). Timings in `references/visual-quality.md` section 2.3.
5. **The cover shouts even if the game whispers.** On portal grids, winners use a saturated background, one big character or object, and a chunky outlined title readable at 200 px. See `references/portal-thumbnails.md`.

## Steps

1. **Brief.** Copy the template below into the game's `ART.md` and fill every line with concrete values (hex codes, px, font names).
2. **Hero screen mock.** Build one screen (the main gameplay view) at 1366x768 with real art for the main character and placeholder rectangles for the rest. Review it (step 4) before producing other assets.
3. **Capture.** Serve the build (`npx vite preview --port 4173`), then:
   `node scripts/shots.mjs --url http://localhost:4173 --out shots/` captures 907x510, 1366x768, 1920x1080, 800x450 and 390x844 after load and after 40 clicks at the centre of the scene; it exits 1 if the page logs console errors. Options: `--clicks N`, `--selector CSS` (what to click), `--wait MS`.
4. **Review.** `python3 scripts/review-sheet.py shots/1366x768-play.png` writes `-review.png`: the frame, a grayscale copy, a blurred copy and 200 px and 94 px thumbnails side by side. Read it and answer the 40 checks at the end of `references/visual-quality.md`. Checks 1-12 are blockers. Write the answers into `REVIEW.md` with the fix for every "no".
5. **Fix and repeat** until no blockers remain. Then ask a fresh reviewer agent to do step 4 without seeing your answers.
6. **Cover.** Follow `portal-launch` for sizes; judge the cover with `review-sheet.py` too. The 94 px thumbnail must still show what the game is.

## ART.md template

```
Pitch in one line:
Shape language (round/square/spiky) and why:
Outline and shading system (a/b/c), outline px at 1080 high:
Light direction:
Palette (hex): background ___ ___ | action ___ | reward ___ | danger ___ | text dark ___ | text light ___
Fonts (max 2, licence): display ___ (titles, numbers, with outline ___ px) | body ___
Spacing unit: 8 px. Corner radii: ___ ___ ___ (and pill).
Button style: fill, lip px, outline, press animation:
Hero object and its idle animation:
Reward tiers (tap / buy / milestone) and their effects:
Thumbnail idea: background colour, subject, title treatment:
References (our own art files, not other games' assets):
```

## Common problems

| Problem | Fix |
|---|---|
| Shapes vanish in the grayscale copy | Raise value contrast between play objects and background |
| Thumbnail unreadable at 94 px | Fewer elements, bigger subject, 1-3 word title with thick outline |
| UI feels flat | Lip and gradient on buttons, panel shadows, display font with outline |
| Scene feels dead in screenshots | Idle loops, floating numbers, ambient particles |
| Mismatched art | Regenerate the odd one out from the approved references (game-assets) |
