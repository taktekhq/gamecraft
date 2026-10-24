---
name: web-game-studio
description: End-to-end route for making a small 2D casual web game (idle, clicker, puzzle, casual arcade) that can pass a portal's soft launch on CrazyGames or Poki - design check, stack, build, automated verification, art review, launch. Use when asked to "make a game", "build a web game", "HTML5 game", "browser game", "idle game", "clicker", "puzzle game", "game for CrazyGames/Poki", or to plan, review or fix such a game. Routes to game-art-direction (looks), game-assets (sprites, audio), portal-launch (submission). Not for Unity/Unreal/Godot projects or 3D games.
---

# Web game studio

A portal game lives or dies on three numbers measured in its first week: share of players still playing after 1 minute (CrazyGames top games 80%+), average session (10+ min), and next-day return (platform average about 6.7%, strong 10-15%). Every step below serves one of them.

## Rules

1. **Original only.** Own characters, names and art. No clones, no famous characters, no names confusable with other games. Portals reject clones and so do we.
2. **Land in gameplay.** No title screen, no login, no tutorial wall. The first input is the core verb.
3. **Logic is pure and tested.** All rules and numbers live in `src/core/` with no DOM or engine imports.
4. **Nothing ships unseen.** Every build gets screenshots at portal sizes and a visual review before anyone calls it done.

## Steps

1. **Design check (before code).** Write `DESIGN.md`: one-sentence pitch, core verb, the three loops (core 5-30 s, session 1-3 min, meta days), the first 60 seconds second by second, what unlocks when, and what brings a player back tomorrow. Run the checklist at the end of `references/retention-design.md`. Any "no" in its gate section: fix the design first.
2. **Pick the stack** from `references/tech-stack.md`: UI-heavy idle/clicker = Vite + TypeScript + DOM/CSS (no engine); grid puzzle or arcade = Phaser 4. Node 20+. Use its starter folder layout, `base: './'`, and a `platform.ts` adapter (local, crazygames, poki) so the game never calls a portal directly.
3. **Set the look before the build.** Load `game-art-direction` and write `ART.md` (art direction brief). Load `game-assets` for the asset plan. Approve one hero screen mock before producing everything.
4. **Build in thin slices.** Core loop first, playable in a browser within the first hour of work. Then juice (installed skill `game-feel` has the patterns), then progression, then save and offline, then polish.
5. **Verify with code, every slice:**
   - `npm test`: unit tests for `core/` (costs, rewards, save migration).
   - `npm run sim`: a headless pacing simulator that plays the game with a sensible strategy and prints time to every unlock and the longest stretch with nothing new. Targets: first reward under 10 s, new unlock every 30-90 s for the first 15 min, no dead stretch over 90 s.
   - Screenshots: `node ../game-art-direction/scripts/shots.mjs --url http://localhost:4173 --out shots/` (sizes 907x510, 1366x768, 1920x1080, 800x450, 390x844; fails on console errors).
   - Size: `node ../portal-launch/scripts/check-build.mjs dist`.
6. **Visual review.** Apply the screenshot checklist in `game-art-direction` to every PNG. Fix all blockers. Have a second agent review with fresh eyes when the game is close.
7. **Launch.** Load `portal-launch`: covers, preview video, listing, SDK calls, pre-submit check.

## Installed skills to lean on

`game-feel`, `game-ui-ux`, `create-game-assets`, `audio-design`, `save-systems`, `performance-optimization`, `phaser-core`, `pixijs-rendering`, `prototype-fast`, `puzzle` (the disciplines plugin, Apache 2.0). Read them for depth; this skill decides the order and the bar.

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| Players quit in the first minute | Menu or text before play, slow load, unclear goal | Start in play, one arrow hint, first reward under 10 s, build under 5 MB |
| Sessions short | Nothing new to want | Sim gap report; add an unlock or visible next goal in every gap over 90 s |
| Nobody returns | No saved progress or reason | Autosave, offline earnings, daily reward, an unfinished goal on exit |
| Looks amateur | Mixed styles, default fonts, flat buttons | `game-art-direction` checklist |
| Works locally, blank on portal | Absolute paths, external requests | `base: './'`, bundle everything, run check-build |
