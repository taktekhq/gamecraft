# gamecraft

Agent skills for making small 2D casual web games that can pass a portal's soft launch (CrazyGames, Poki): design for retention, a professional look, game-ready assets from an image model, and submission. Written for Claude Code, usable by any agent that reads `SKILL.md` files.

| Skill | Use it for |
|---|---|
| `web-game-studio` | The route from idea to submission: design check, stack, build in slices, automated verification |
| `game-art-direction` | Looking professional: art direction brief, palette roles, UI and juice rules, a 40-point screenshot review |
| `game-assets` | Sprites and props from an image model on a chroma sheet, automatic cutout, audio, fonts, licences, budget |
| `portal-launch` | CrazyGames and Poki rules, SDK calls, covers, preview videos, listing, pre-submit check |

Each skill has a short `SKILL.md` and a `references/` file with the research behind it (sources listed at the end of each).

## Scripts

| Script | What it does |
|---|---|
| `game-art-direction/scripts/shots.mjs` | Screenshots a served game at 5 portal sizes, before and after clicks; fails on console errors or external requests |
| `game-art-direction/scripts/review-sheet.py` | Original, grayscale, blurred, 200 px and 94 px thumbnails side by side, for visual review |
| `game-assets/scripts/cutout.py` | Samples a chroma background, keys it out with despill, splits a sheet into named sprites, writes a light/dark check sheet |
| `portal-launch/scripts/make-covers.py` | Makes 1920x1080, 800x1200 and 800x800 covers from one piece of art, with the title set in a font |
| `portal-launch/scripts/check-build.mjs` | Pre-submit check of a build folder: size budget, file count, absolute paths, external URLs, source maps |

Requirements: Node 18+ with `playwright` or `playwright-core` and a Chromium (`CHROMIUM_PATH` to point at one), Python 3 with Pillow and numpy (`uv run --with pillow --with numpy python3 ...` works).

## Install

```
git clone https://github.com/taktekhq/gamecraft.git
for s in gamecraft/skills/*/; do ln -s "$PWD/$s" ~/.claude/skills/; done
```

Or copy a single skill folder into a project's `.claude/skills/`. These skills pair well with the open-source discipline skills in awesome-gamedev-agent-skills (game feel, game UI/UX, Phaser), which they point to for depth.

## Test

```
bash tests/run.sh
```

Runs the scripts against a fixture game (`tests/fixture-game`) and a generated sprite sheet.

## Notes

- The image-model steps assume any model that accepts reference images; the prompt template is in `game-assets/assets/sheet-prompt.txt`.
- Portal rules change. The references record what each portal's docs said on 24 Oct 2026 with links; check the live docs before submitting.

## License

MIT, see LICENSE.
