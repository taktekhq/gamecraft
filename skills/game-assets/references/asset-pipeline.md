# Asset pipeline for small 2D web games (Taktek arcade), research of 24 Oct 2026

Status: written in one pass under a time cap. Policy facts (section 7) and portal size limits were fetched from official pages on 24 Oct 2026. Tool-behaviour claims in sections 1-5 mix verified pages with working knowledge; items marked (check) should be tested once before being written into the skill.

## Summary (15 lines)
1. Portals do not ban AI assets. Poki says AI is fine if it adds value, wants the process on request (tools, prompts, iterations), and rejects raw or generic output. CrazyGames docs say nothing about AI. Steam (Jan 2026 rules) wants disclosure of AI content that ships and players see; coding helpers are exempt.
2. Keep a provenance file per game (tool, date, prompt, plan, licence) so Poki's "show your process" ask takes five minutes.
3. Size limits that matter: CrazyGames initial download 50 MB (20 MB for the mobile homepage), total 250 MB, 1500 files. Poki wants fast first load. Our own budget: under 5 MB initial, under 20 MB total.
4. Our edge is an original cartoon cast with a hand-inked cream-paper look. Lock it with 2-4 reference images plus a short style paragraph reused verbatim in every prompt. Never rely on the model's memory of the style.
5. Transparency: generate on flat chroma green (#00FF00) or magenta, key out with ImageMagick or sharp, then clean edges. For hard cases use rembg or BiRefNet on the XPS/Toshiba (CPU is fine for one-off sprites).
6. Generate in sheets (character sheet, item grid of 3x3 or 4x4) in one prompt, then slice. One image per prompt drifts; a grid keeps palette and line weight consistent.
7. Animate by cutting parts out (body, head, arms, eyes, mouth) and tweening in code: squash/stretch, bob, blink, wobble. Frame-by-frame from image models drifts too much beyond 4-6 frames.
8. Code art (SVG, canvas, CSS) beats raster for UI, icons, particles, backgrounds with gradients, and anything that must scale or recolour. Raster wins for the hand-inked characters.
9. Libraries: Kenney (CC0) is the safe default; game-icons.net needs CC BY 3.0 credit; OpenGameArt must be checked per asset (CC-BY-SA and GPL are traps); fonts from Google Fonts/Fontsource are OFL.
10. Audio: ZzFX/jsfxr for sfx (no licence worries, tiny), ElevenLabs paid plan for richer sfx, Suno paid plan for music only with eyes open about ownership; CC0 music (Kenney, OpenGameArt CC0, Pixabay-style licences need reading) as the safe fallback.
11. Ship WebP for raster (lossless for flat cartoon art, quality 80-90 lossy for backgrounds), OGG or MP3 for audio via Howler, one atlas per scene at 2048 max.
12. Subset fonts to the glyphs used (pyftsubset to woff2), 1 or 2 fonts max.
13. Sprite sheets: free-tex-packer or the Python PIL packer below; no paid TexturePacker needed.
14. Review gate before upload: no watermark, no prompt text, consistent style, thumbnail matches in-game art (Poki rule).
15. Disclose AI use plainly in the credits screen and in Steam if we ever go there; it costs nothing and Poki encourages it.

## 1. Consistent 2D sprites with image models

### Model chooser (for our case)
- Gemini image ("nano banana" family) via agy: our default. Strong at following reference images, editing ("keep this character, change the pose"), and multi-image input, and good at flat backgrounds. Use for characters, props, backgrounds, thumbnails. Free on our Ultra plan, but agy image jobs time out when run in parallel, so run 1-2 at a time.
- gpt-image: strong text rendering and precise edits; only if we have API budget. Not needed.
- Flux (Kontext for edit-with-reference): best open option for consistent edits; needs a GPU, so only through a hosted API. Skip unless Gemini fails.
- Ideogram: best for text inside images (logos, title cards, button labels). Use for thumbnails with lettering, or draw text in code instead.
- Recraft: native vector (SVG) output and icon sets in one style. Good for UI icon families; output SVGs are often heavy, so run through svgo. Paid, so optional.
- Retro Diffusion / PixelLab: only if we ever do true pixel art. Gemini cannot make grid-true pixel art; it fakes it and the pixels are inconsistent. For pixel art use those, or write pixel arrays by hand/code.
- Scenario / Layer.ai: train a custom style model on our cast and generate consistent families at scale. Worth it only if we ship many games with identical style; for now reference-image prompting on Gemini is enough. (check pricing before recommending)

### Step by step (Gemini via agy)
1. Style bible: one folder `style/` with 3-5 approved images: two cast portraits, one prop, one background, one UI element. These are the permanent reference images attached to every generation.
2. Style lock paragraph (copy verbatim into every prompt). Example: "Hand-inked cartoon, uneven black ink outline about 3 px at 512 px, flat gouache fills, slight paper grain, cream paper tone, no gradients, no 3D, no shadows beyond one flat offset shade, warm limited palette of 6 colours." Add the palette hex list; models follow hex codes loosely but better than adjectives.
3. Character sheet first: ask for the character in a 3x2 grid: front, 3/4, side, back (if needed), plus 4 expressions, all same scale, on flat #00FF00 background, with equal space between cells. Pick the best one and store it as `char/<name>/sheet.png`. Every later pose prompt attaches the sheet plus a style reference.
4. Per-asset prompts always: "Match the attached style reference exactly. Same line weight and palette. Orthographic side view / front view [pick one for the whole game]. Subject centred, fully inside frame, margin 10 percent, background solid #00FF00 with no shadow, no ground, no gradient."
5. Families (items, icons, tiles): request a grid in one image ("a 4x4 grid of 16 distinct fruit icons, each in its own equal cell, same size and view, no overlap"). Slice with ImageMagick `convert in.png -crop 4x4@ +repage +adjoin cell_%02d.png`. Grid generation is the best consistency trick; batches of separate prompts drift in line weight and saturation.
6. Scale and view: decide once per game (for example, camera front-on, characters 256 px tall, items 96 px, UI 64 px). State it in the prompt, then normalise after generation (trim, scale to the target height, pad to a common cell). Never trust the model's scale.
7. Backgrounds: generate wide (16:9 or 21:9) with no characters, "empty centre, details at edges"; parallax layers: ask separately for far, mid and near layers with the same palette and keyed transparent where needed. Keep text-free.
8. Iterate with edit prompts, not new prompts: "same image, change X only". Edit mode preserves identity better than regeneration.
9. Reject early: if the 3rd regeneration still drifts, fix by compositing in code (swap a hand, reuse a head) rather than more prompting.

### Clean transparency
- Method A (default): flat chroma. Prompt for #00FF00 (green) when the art has no green; use #FF00FF when it does. Then key and de-spill:
  - ImageMagick: `magick in.png -fuzz 12% -transparent "#00FF00" -channel A -morphology Erode Diamond:1 +channel out.png` then a de-spill step: `magick out.png -fill none -channel RGB -fx "..."` (simpler: do green despill in PIL, set G = min(G, max(R,B)) on edge pixels).
  - Edge halo fix: erode alpha 1 px, then blur alpha 0.5 px: `magick out.png \( +clone -alpha extract -morphology Erode Diamond:1 -blur 0x0.6 \) -alpha off -compose copy_opacity -composite clean.png`.
- Method B: background-removal model. rembg (U2Net, isnet-anime) is easy: `pip install "rembg[cpu]"` then `rembg i in.png out.png -m isnet-anime`. BiRefNet gives the best edges on fine hair and thin lines but is slower on CPU (fine for a few dozen sprites, run on the XPS). Cartoon outlines on a cream background are hard for models (they eat thin outlines); chroma wins for ink-line art.
- Method C: generate on white and on black with identical prompts, difference-matte; fragile, skip.
- Never ask for "transparent background" directly: many models paint a checkerboard into the pixels. This is the single most common failure.
- Always check: zoom 400 percent over a dark and a light backdrop before accepting.

### Upscale / downscale
- Generate big (1024+), downscale with Lanczos to the target: `magick in.png -filter Lanczos -resize 256x256 out.png` (or sharp `.resize({kernel:'lanczos3'})`). Downscaling hides small model errors; design for it.
- Upscale only when needed: Real-ESRGAN (anime model) on the XPS CPU for single images; it sharpens ink lines well. Avoid upscaling to fix a soft generation, regenerate instead.
- Retina: ship 2x only for characters and key UI; backgrounds can ship at 1x and be stretched since they are soft.

### Known failure modes and fixes
- Style drift between generations: use the same references every time, add the style paragraph, use grids, edit-mode instead of regenerate.
- Fake transparency (checkerboard baked in): chroma method.
- Extra fingers, odd limbs, face off-model: crop and regenerate only that region in edit mode; or composite parts from another take.
- Inconsistent scale and viewpoint: normalise in code; ask for orthographic views; separate prompts for top-down vs side.
- Text garbled: draw text in code with an OFL font.
- Outlines lost on key-out: use a darker, thicker outline in the prompt, key at lower fuzz, never go below 10 percent fuzz without checking.
- Glow/shadow on the chroma background (contaminates key): say "no shadow, no glow, no ground plane".
- Colour shift between batches: after generation, quantise to the palette with `magick in.png -remap palette.png` for flat art (see palette step in pipeline).
- Watermarks / sparkle logos on some outputs (Gemini adds an invisible SynthID; visible stars on some tools): inspect and crop. Poki asks for no visible AI watermarks.

## 2. Animation for small web games

### Frame-by-frame from image models
- Works for short loops (idle 4 frames, blink 2 frames, a 6-frame walk) only if you feed the previous frame plus the character sheet and ask for "the same character, next frame, only the legs moved". Even then, line wobble and detail drift appear. With hand-inked art, a little wobble looks intentional (boiling line), which helps us.
- Veo/Flow video to sprite frames: extract with `ffmpeg -i clip.mp4 -vf "fps=12,scale=256:-1" f_%03d.png`, key the background (generate against flat chroma), then pick 8-12 frames. Good for one-off effects (explosion, poof), poor for long consistent loops. Loop point needs hand trimming.
- Practical limit: do not plan any asset that needs more than ~12 unique frames per animation from image models.

### Cut-out animation in code (our default for characters)
1. Ask Gemini for a "disassembled" character: body, head, each arm, each leg, eyes open/closed, mouth shapes, on chroma, in an exploded layout. Slice to parts.
2. Define pivots (shoulder, hip, neck) in a small JSON: `{ "head": {"x":..,"y":..,"pivot":[..]} }`.
3. Animate with tweens: idle = body scaleY sin(t*2) 2 percent, head rotate 1-2 degrees, blink every 3-5 s for 120 ms by swapping the eye part, mouth swaps for speech, arms swing for walk.
4. Libraries: GSAP (now free including plugins), Phaser tweens, PixiJS + @pixi/spine only if using Spine. Plain `requestAnimationFrame` with ease functions is enough for small games.

### Tools
- Spine: best skeletal runtime but paid licence for editor (Essential about 70 USD one-off; check) and runtime licence terms; overkill for our scale.
- DragonBones: free, but unmaintained; avoid for new work.
- Rive: free editor tier and a small WASM runtime (~150-300 KB), great for UI, state machines and character rigs; check the portal rule about external requests (bundle the runtime locally). Good option if we want a designer-style tool.
- Lottie: JSON, suited to UI/celebration effects exported from After Effects; the lottie-web player is heavy (~150 KB min). dotLottie/thorvg builds are smaller. For games, prefer code tweens.
- Procedural: squash and stretch on land/jump (scale 1.2/0.8 for 80 ms then spring back), bob (sin), blink timers, anticipation (move 5 percent back before action), hit flash (white tint 60 ms), screen shake, particle puffs. This "juice" gives more feel per kilobyte than extra frames. See the disciplines:game-feel skill.

### Sprite sheets and atlases (free)
- free-tex-packer (web/CLI/npm `free-tex-packer-core`) outputs Phaser/Pixi JSON atlases.
- ShoeBox (free, Adobe Air; old), Aseprite exports (paid or compile free), Leshy SpriteSheet Tool (web, free).
- Our own: a 40-line PIL shelf packer is enough; or `sharp` composite with a JSON map (see pipeline).
- Rules: power of two not required in WebGL2 but 2048x2048 max for old mobile; 2 px padding with edge extrusion to prevent bleeding; trim transparent borders and store offsets.

## 3. Code-drawn art
- SVG (hand-written by Claude): icons, UI frames, buttons, logos, simple props. Tiny files (0.3-3 KB), scalable, recolourable via CSS variables, animatable. Run `npx svgo`.
- Rough.js: gives a hand-drawn wobbly stroke and hachure fill to shapes drawn in canvas or SVG; matches a hand-inked identity. Roughly 9 KB gzip. Seed it (`seed` option) so shapes do not jitter every frame unless you want boiling lines.
- Canvas 2D: procedural backgrounds (gradients, noise, paper grain via a single small tiled texture), particles, trails, grids, board games, tilemaps that are just coloured rectangles.
- CSS: UI, buttons, transitions, text with `text-shadow` outlines, layout. Cheap to ship; free scaling to all screens.
- Choose vector/code when: asset is geometric, needs recolouring (tile colours, skins), must scale across mobile and desktop, or you need dozens of variants (generate by function). Choose raster when: asset is characters with the hand-inked texture, painterly backgrounds, or anything with organic variation.
- Hybrid: raster characters over code-drawn backgrounds and UI; paper-grain overlay in canvas ties both together.

## 4. Free and licensed asset libraries (commercial portals)
| Source | Licence | Rule |
|---|---|---|
| Kenney.nl | CC0 | No credit needed; best default for UI, shapes, sfx, some music. Safe on portals. |
| game-icons.net | CC BY 3.0 | Commercial use OK but attribution required: credit the artist (author names are on each icon) in a credits screen and in the portal description. |
| OpenGameArt | Per asset: CC0, CC-BY, CC-BY-SA, GPL, OGA-BY | Allow CC0 and CC-BY only. Avoid CC-BY-SA and GPL for shipped art because share-alike can reach the game. Check that the uploader is the creator (reuploads of ripped assets occur). |
| Google Fonts / Fontsource | OFL (mostly) | Free to embed and ship; keep the licence text; do not sell the font alone; renaming rules apply if modified (Reserved Font Name). |
| itch.io packs | Per pack (read the page / EULA) | Many allow commercial use, forbid redistributing the raw pack; some ban AI training or use in games for sale. Screenshot the licence at purchase. |
| Freesound | CC0 / CC-BY / CC-BY-NC | Only CC0 or CC-BY; NC is not allowed on ad-supported portals. |
| Pixabay / Mixkit audio | Own licences | Generally commercial-friendly, but not CC0 and some restrict standalone redistribution; read and save the page. |

### Provenance record
- One `ASSETS.md` (or `assets.json`) per game, one row per asset group: file or folder, source (URL or "generated"), author, licence, date, tool and model name for AI, the prompt file path, plan/tier at the time, attribution text required.
- Save the licence page as PDF or text in `provenance/` the day you take the asset (licences change).
- Keep every AI prompt and the chosen/rejected outputs list in `provenance/prompts/`. That is exactly what Poki asks for on request.
- Credits screen text generated from the same file at build time so they never drift.
- AI output copyright: pure AI output may not be copyrightable in the US; our human edits (hand-inked cast, compositing, tweening code) are what we own. Do not claim exclusive rights on raw output.

## 5. Audio
### SFX
- ZzFX (about 1 KB, code-generated, array of numbers per sound), jsfxr/sfxr (web editor `sfxr.me`, exports WAV or a param string), ChipTone (web, exports WAV). Output is yours; no licence issue. Best for blips, coins, clicks, jumps. Pre-render to OGG for Howler or play ZzFX live with no file at all.
- AI SFX: ElevenLabs sound effects. Free plan is non-commercial (needs a paid plan for commercial use and attribution rules on free); generate the final files while a paid plan is active and keep the invoice/plan record. Reports say rights stay with you once generated on paid. Check the current terms page for SFX specifically before relying on it. Alternatives (Stable Audio, Gemini/Lyria for sound) have different terms; read each.
- Foley by recording and ffmpeg pitch/time tricks is free and original.

### Music
- Suno / Udio: paid plans grant commercial use per their terms, but terms changed in 2025-26 (label deals); ownership language is murky, free tier is non-commercial, and output cannot be used to train competing models. Safe stance: generate on a paid plan, keep dated screenshots of the plan and the terms, treat tracks as licensed rather than owned, avoid prompts naming artists. Some portals/distributors scan for matches, so keep tracks short and original.
- CC0 music: Kenney audio, OpenGameArt CC0 tracks, Incompetech (CC BY, credit required).
- Procedural music: Tone.js or a small WebAudio sequencer: a pentatonic arpeggio over a drone loops forever at near-zero size. Good for idle/clicker backgrounds. Add layers with game state (extra stem when score grows).
- Gemini TTS for voice lines: check terms; keep voices short, and no real-person likeness.

### Loudness and formats
- Target about -16 LUFS for music, -14 to -12 LUFS for short sfx peaks, true peak -1 dBTP. Normalise with ffmpeg: `ffmpeg -i in.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 out.wav`.
- Format: OGG Vorbis (smallest) plus MP3 fallback (Safari handles OGG on modern versions; check target browsers). Howler.js accepts `src: ['a.webm','a.mp3']`. Music mono or 96 kbps stereo; sfx mono 22-44 kHz. Typical size: 60 s music ~ 700 KB at 96 kbps.
- `ffmpeg -i in.wav -c:a libvorbis -q:a 3 out.ogg` and `ffmpeg -i in.wav -c:a libmp3lame -b:a 96k out.mp3`.
- Howler.js: audio sprites (one file, many sounds): `audiosprite` npm tool or ffmpeg concat, then `new Howl({src, sprite:{coin:[0,300]}})`. Unlock audio on first user tap; resume AudioContext after iOS interruption (CrazyGames doc calls this out). Mute on tab hidden and expose mute buttons (portals expect them).

## 6. Optimisation for web portals
- Verified limits (CrazyGames docs, 24 Oct 2026): initial download at most 50 MB (20 MB for mobile homepage eligibility), total at most 250 MB, at most 1500 files, and externally loaded files should reach gameplay in 20 s or less. Use relative paths. Our internal budget: initial under 5 MB, total under 20 MB, under 100 files.
- Raster formats: WebP is universally supported and our default (lossless for flat cartoon art; lossy q80-85 for backgrounds). AVIF is smaller but slower to decode and fussy on old mobiles; use only for big static backgrounds if we need the bytes. PNG only for sources and tiny assets. Commands: `cwebp -q 85 in.png -o out.webp`, `cwebp -lossless -z 9 in.png`, sharp: `sharp(i).webp({quality:82})`.
- Palette-quantised PNG (pngquant 64 colours) is often smaller than WebP for flat 6-colour art: test both per asset.
- Atlas sizes: one atlas per scene, 2048x2048 max (1024 for low-end mobile); keep atlas under 1.5 MB each after WebP.
- Lazy loading: load the menu and first level only, stream later levels and music after gameplay starts; the portals' initial-size clock stops at gameplay start.
- Fonts: subset with `pyftsubset Font.ttf --unicodes=U+0020-007E --flavor=woff2 --output-file=font.woff2`; one display and one body font max; or draw numbers from a bitmap font atlas.
- Audio: see section 5; music is usually the biggest item, so use mono 64-96 kbps and short loops.
- Code: esbuild/vite with minify, tree shake; no heavy frameworks for small games; gzip/brotli served by portals.
- Count your files: 1500 file cap means atlases and audio sprites, not hundreds of loose files.

## 7. Policy: AI-generated assets (checked 24 Oct 2026)
- Poki (developers.poki.com guide "Content & player safety", AI section): allowed. Principle: "AI should empower, not shortcut." Prototype with AI freely; before player testing the game must show your own perspective. Heavy reliance on non-original material raises rejection risk after the web-fit test. Games made solely with AI can raise IP ownership issues for Poki, so keep process, prompts, iterations and be ready to hand them over. Pre-submit: consistent visuals, no AI watermarks or leftover prompt text, review all dialogue, playtest all generated content, thumbnail must match the in-game art. Do not use prompts that imitate other franchises. Disclosure is encouraged, not mandated.
- CrazyGames: the requirements pages I fetched (intro and technical) say nothing about AI content. A third-party summary (Playgama) says there is no AI-specific rule or disclosure and that any game must pass QA and the Basic Launch performance test. Treat as unverified: check the CrazyGames developer portal (Terms) before submission; I could not find an official AI statement.
- Steam (Valve, rewritten 16 Jan 2026): disclosure required for pre-generated AI content (art, code, sound) that ships in the game, with confirmation of rights; live-generated AI content needs described guardrails; AI used only as a behind-the-scenes dev tool (such as a coding assistant) is exempt. Players can flag content; non-compliance risks removal. Source is trade press; verify in Steamworks docs if we ever go there.
- Other: itch.io has an AI-generated tag (no mandate). Panic Playdate Catalog bans generative AI for creative assets (not relevant). Epic, GOG, consoles: no clear public rule. Apple/Google stores: no blanket AI-asset rule I verified; Google Play has an AI-generated content policy aimed at apps that generate content for users (not pre-baked art). (check before mobile packaging)
- Our stance: ship AI-assisted art that is substantially edited into our own cast and style, keep the provenance folder, add a short credits line "Art: Taktek with AI assistance", and never ship raw model output.

## Recommended pipeline for us (exact steps)
Folder layout per game: `game/assets/src/` (raw generations, git-ignored large), `game/assets/art/` (cleaned PNG), `game/public/` (built WebP + atlas + audio), `game/provenance/` (ASSETS.md, prompts/, licences/).

1. Style bible (once, shared across games): `arcade/style/` with 4 approved reference images, the style paragraph in `style.txt`, and `palette.txt` (6-8 hex). Add `viewpoint.txt` (side view, 3/4, top-down) per game.
2. Generate on agy, one or two jobs at a time, always with references and the style paragraph. Output into `assets/src/<name>_<n>.png`, prompt saved next to it as `.txt`.
   - Characters: sheet first (grid of poses/expressions on #00FF00), then exploded parts for rig.
   - Items/icons: 4x4 grid per family, slice.
   - Backgrounds: wide, empty centre, 3 parallax layers if needed.
3. Slice and clean (run on the XPS if more than a few files):
   ```
   magick sheet.png -crop 4x4@ +repage +adjoin cell_%02d.png
   magick cell_00.png -fuzz 14% -transparent "#00FF00" -trim +repage out_00.png
   ```
   De-spill with a PIL script: for pixels with alpha above 0, set G = min(G, max(R, B)). Erode alpha 1 px and blur 0.5 px. For ink-line problems fall back to `rembg i -m isnet-anime`.
4. Normalise: trim, scale to the per-class target height with Lanczos, pad to a uniform cell; optionally remap to the palette (`magick in.png -remap palette.png`) for flat art.
5. Review gate: view each on a dark and a light checker; reject halos, off-model faces, stray text, visible watermarks. Record keepers in ASSETS.md.
6. Code art for UI, icons, particles: Claude writes SVG/canvas/CSS; `npx svgo`; Rough.js for hand-inked panels with a fixed seed.
7. Rig and animate in code: parts atlas plus pivots JSON, tweens for idle/blink/squash; juice (hit flash, screen shake, puffs) per the game-feel skill.
8. Pack: `npx free-tex-packer-cli --project pack.ftpp` (or the PIL packer) to a 2048 max atlas with 2 px padding and extrusion; convert to WebP: `cwebp -q 85 atlas.png -o atlas.webp` (lossless if flat colours).
9. Audio: ZzFX/jsfxr for sfx; if AI sfx, ElevenLabs on a paid month, log the plan. Music: Suno paid (log plan and terms screenshot), or CC0/procedural. Normalise (`loudnorm`), export OGG + MP3, pack sfx into an audio sprite.
10. Fonts: choose OFL font, subset to woff2 (`pyftsubset`), keep licence file.
11. Budget check script in CI: sum `public/` bytes of what loads before gameplay; fail over 5 MB; fail total over 20 MB; fail over 100 files.
12. Provenance: update `ASSETS.md`; generate the in-game credits from it; save licence pages for CC BY items (game-icons.net authors) in `provenance/licences/`.
13. Portal submission: thumbnails drawn from in-game art style (Poki), no prompt text or watermarks, have the prompts folder ready; mention "AI-assisted art, edited by hand" in notes.
14. Close the loop: after launch, note in the arcade memory which prompts and tricks worked (grid trick, chroma colour, failures).

## Sources
- Poki, content and player safety (AI section; the old sdk.poki.com/working-with-ai redirects here): https://developers.poki.com/guide/content-player-safety
- CrazyGames technical requirements: https://docs.crazygames.com/requirements/technical/
- CrazyGames requirements intro: https://docs.crazygames.com/requirements/intro/
- Playgama on CrazyGames AI policy (third-party): https://playgama.com/blog/business-faqs/what-is-the-crazygames-policy-on-publishing-ai-generated-gam/
- Steam AI disclosure, Jan 2026 rewrite (trade press): https://tbreak.com/steam-ai-disclosure-policy-update-developers/ and https://www.techradar.com/gaming/steam-softens-its-stance-on-ai-generated-content-opening-the-floodgates-to-the-vast-majority-of-games-that-use-it
- Steam disclosure overview: https://www.videogameschronicle.com/news/steam-pages-will-now-disclose-which-games-use-ai-generated-content/
- ElevenLabs terms summary: https://terms.law/ai-output-rights/elevenlabs/
- AI music licensing (Suno, ElevenLabs): https://licenseorg.com/blog/ai-music-licensing-suno-elevenlabs
- Panic Playdate AI ban: https://letsdatascience.com/news/playdate-maker-bans-generative-ai-in-catalog-38fa3bf0
