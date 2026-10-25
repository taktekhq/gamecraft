---
name: portal-launch
description: Get a finished HTML5 game onto CrazyGames (and later Poki) - build rules, SDK calls, saves, ad rules, the three covers and preview videos, listing text, a pre-submit check script, the soft-launch metrics and what to do after. Use for "submit to CrazyGames", "publish on Poki", "portal requirements", "make the game covers", "game thumbnail", "CrazyGames SDK", "Basic Launch", "Full Launch", "is the build ready to submit". Not for designing or drawing the game (web-game-studio, game-art-direction, game-assets).
---

# Portal launch

CrazyGames first: free Basic Launch (7-21 days, ends at 7 days and 500 plays), then Full Launch with ads only if conversion, playtime and day-1 retention beat their benchmarks. Poki last: its default deal is 5 years web-exclusive, which blocks other portals.

## Rules

1. **Accepting a portal's terms is the owner's call.** Summarise the terms (exclusivity, ownership, jurisdiction) and get an explicit yes before ticking any terms box.
2. **Bundle everything.** No external requests, no CDNs, no analytics, relative paths only (`base: './'`). The only allowed script from outside is the portal's own SDK.
3. **No ads or SDK ad calls in Basic Launch**, but call `gameplayStart()` (CrazyGames measures initial size up to it). The game must run cleanly with ads off.
4. **Title text only on covers.** No "Play", "New", borders, icons or store logos.

## Steps

1. **Pre-submit check:** `node scripts/check-build.mjs dist --budget-mb 5` checks total size, file count (1,500 max), absolute paths, external URLs in code, and a missing `index.html`. Fix everything it reports.
2. **SDK wiring** (CrazyGames v3) through the game's `platform.ts`: load `https://sdk.crazygames.com/crazygames-sdk-v3.js` in the head, `await window.CrazyGames.SDK.init()`, `game.loadingStart()` before boot work and `game.loadingStop()` when the first frame is ready, then `game.gameplayStart()` as soon as play is possible (the QA tool times "load" up to the first gameplayStart: a game that waited for the first click showed a 63 s load; calling it when ready showed 1.4 s), again on every resume, `game.gameplayStop()` on every break, `game.happytime()` only for real achievements, and the Data module for saves (under 1 MB). Tick "using the Data Module" in the form. Test on localhost (the SDK runs in `local` mode), then in the portal's Preview tool.
3. **Browser hygiene:** `user-select: none` on body; preventDefault on wheel, arrow keys, space and contextmenu; resume AudioContext on touchend/click; never use Escape or Ctrl/Cmd+W as controls; support mouse, keyboard and touch if mobile is on.
4. **Covers:** `python3 scripts/make-covers.py art.png "Title" --font Display.ttf --focus 0.7,0.5 --out covers/` makes 1920x1080, 800x1200 and 800x800 from one piece of art with the title set in code. Art: one big character or object, saturated background, an empty side for the title, no text. Check each with `game-art-direction/scripts/review-sheet.py`: the 94 px thumbnail must still read.
5. **Preview videos:** two silent 15-20 s clips (1080p 16:9 and 1080p 2:3, under 50 MB), real gameplay at normal speed, opening on the cover frame, no cursor, no black bars, no text. Record with Playwright's video capture or ffmpeg from scripted play.
6. **Listing:** a distinct title that matches the gameplay, a 2-3 sentence description, controls, tags chosen after reading the category page. No em dashes, no hype.
7. **Submit** at developer.crazygames.com. The HTML5 upload takes a folder, not a zip: unzip `dist` and drop the folder on the upload zone (from an agent: CDP `Input.dispatchDragEvent` with `data.files: [folderPath]`; `DOM.setFileInputFiles` with a folder sets 0 files). The QA step asks you to self-certify checks, including a real phone test: open the preview's QR link on an iPhone and an Android phone first. Then then watch the Developer Portal stats daily during Basic Launch. Targets: 1-minute conversion 80%+, average playtime 10+ min, D1 10-15% (genre averages: puzzle 21 min and D1 6.2%; clicker 15 min and D1 6.6%).
8. **After the verdict:** promoted means integrate ads per `references/portal-playbook.md` (midgame only at natural breaks, at most 1 per 3 min; rewarded as an optional offer, no reward on adError). Not promoted means a new game, or a significantly improved resubmission.

Full rules, numbers and sources: `references/portal-playbook.md` (CrazyGames docs, Poki process, other portals, the full launch checklist).

## Common problems

| Problem | Fix |
|---|---|
| White screen in the CrazyGames iOS app | Sitelock CSP must allow `https://app.crazygames.com` and `capacitor://app.crazygames.com` |
| Page scrolls while playing | preventDefault on wheel (passive: false) and arrow/space keys |
| No sound on iPhone after switching apps | Resume AudioContext inside a touchend/click handler |
| Save lost in incognito | Wrap storage in try/catch; use the SDK Data module |
| Rejected as unoriginal | New name and art; never derivative of an existing hit |
