# Visual quality and polish for small 2D casual web games

Status: written 24 Oct 2026 for the Taktek arcade skill. Evidence labels: [F] fetched/searched this session, [K] from the researcher's background knowledge of the sources (talks, public game UIs); verify [K] numbers before treating them as law. Timings are starting points to tune by feel, not standards.

## Summary (15 lines)

1. Pro casual games look finished because of consistency, not detail: one shape language, one outline rule, one light direction, one type scale, one spacing unit, used everywhere.
2. Limit the palette to roles: 1 background family, 1 primary action color, 1 reward/currency color (gold), 1 danger/alert color, 2 neutral UI darks. Everything else is a tint of those.
3. Value contrast carries readability. The play object must differ from its background by a large lightness gap; check by blurring or desaturating the screenshot. If shapes vanish in grayscale, the art fails.
4. Silhouette first: each game object must be identifiable as a flat black shape at 48 px. Bold, simple, rounded shapes with a 2-4 px dark outline (or a darker same-hue edge) read best on portal thumbnails.
5. UI is chunky: buttons are large (min 44 px tall, ideal 56-72 px on a 1080-wide canvas), rounded, with a bottom "lip" (darker 4-8 px edge) and a top highlight. Flat unstyled rectangles and default browser fonts are the number one amateur tell.
6. One bold display font for headings and numbers (with outline or shadow), one plain sans for body. Never more than two families. Numbers use tabular figures and abbreviations (1.2K, 3.4M, 5.6B) past 4 digits.
7. Layout on a grid: one base unit (8 px), consistent margins, thumb-reachable primary action in the lower half, nothing important in the outer 5% (safe area), portals overlay their own chrome.
8. Juice rule: every input gets feedback within one frame (16 ms), in at least 3 channels (motion, sound, particles or flash). Silent, motionless state changes feel dead.
9. Motion uses easing, never linear: ease-out for things arriving (150-300 ms), ease-in for leaving (100-200 ms), overshoot (easeOutBack) for pop-ins and rewards (250-400 ms), spring/elastic sparingly.
10. Squash and stretch preserves volume (scaleX 1.2 / scaleY 0.8 style), lasts 80-200 ms, and is always paired with anticipation or follow-through on important actions.
11. Screen shake and hit-stop are seasoning: shake 2-8 px decaying in 100-250 ms; hit-stop 30-80 ms; ban constant shake; always provide a reduced-motion/shake toggle.
12. Reward moments escalate: small tap = small pop; big milestone = full-screen celebration of 1-2 s with burst particles, number count-up, a skippable "tap to continue". Never block play for more than ~2 s.
13. Idle screens are never static: breathing scale 1.00 to 1.03 over 1.5-2.5 s, gentle float, glints on currency. Motion draws the eye to the next action.
14. Top portal games (Block Blast style) win on thumbnail clarity: one focal subject, saturated gradient background, big bright title/logo or a clear mid-play board, no tiny text.
15. The first screenshot decides the click: it must show the core loop, a big readable number or board, a clear focal point, and a clean HUD. Review every PNG against the checklist at the bottom before shipping.

---

## 1. What separates professional from amateur at a glance

### 1.1 Art direction

Shape language [K]: pick one family and apply to characters, props, buttons and panels. Rounded squares and circles read friendly (casual default); angular reads aggressive or serious. Mixing sharp-cornered panels with round characters is a classic mismatch. Use one corner radius system for UI (for example 8, 16, 24 px; pill for buttons), not arbitrary values.

Silhouette [K]: test every sprite filled solid black on a plain background at 48 px and at 32 px. Distinct characters need distinct silhouettes (tall vs round vs spiky). Collectibles and hazards must not share silhouette.

Palette roles [K]:
- Background: low-to-mid saturation, mid value, often a vertical gradient (darker at edges, lighter behind play area).
- Play objects: highest saturation and clearly lighter or darker than background.
- Action color: one hue for every primary button (green or orange are common "go" colors); secondary buttons blue or grey; destructive red.
- Reward color: warm yellow/gold for coins, stars, XP; used only for value so it keeps its meaning.
- Text: near-white on dark fills with dark outline; near-black on light panels. Avoid pure #000 and #FFF; use tinted darks (e.g. deep navy or purple) and warm off-whites.
- Rule of thumb: 60 percent background family, 30 percent panels and objects, 10 percent accent.

Value contrast [K]: squint test. Convert the screenshot to grayscale; the three layers (background, play objects, UI/text) must each separate by a visible lightness step. Typical target: text vs fill contrast at least 4.5:1 (WCAG AA), large display numbers at least 3:1. Same-value colors (e.g. mid green on mid red) vibrate and read badly.

Outline and shading [K]: choose one of these and do not mix:
1. Thick dark outline (2-4 px at 1080 px canvas) plus flat fill plus one highlight and one shadow tone (sticker/cartoon look; most readable at thumbnail size).
2. No outline, soft gradient shading, rim light (glossy 3D-ish look, Royal Match, Supercell-like).
3. Flat vector with no shading (clean, minimal, needs strong palette).
Light direction is fixed (usually top-left): highlights on top/left, shadows bottom/right, on every object and every UI element including text shadows (drop shadow goes down, not randomly).

Consistency [K]: same outline weight, same corner radius, same shadow offset, same gradient angle, same icon stroke width across the whole game. Mixed asset sources (stock icons with hand-drawn characters) are visible instantly.

### 1.2 Readability at small sizes

[K] Portals show thumbnails around 200-300 px wide (Poki's own list shows 204x204 and 94x94 px squares, [F]). Design the key art and in-game hero at that size:
- Main subject fills 50-70 percent of the thumbnail height.
- No text under roughly 14 percent of the thumbnail height; title text 2-3 words max.
- 3 to 4 dominant colors.
- In game, minimum text size 16 px on a 1080-tall canvas for secondary info, 24+ px for primary info; on mobile landscape iframes the game may render at ~360-420 px height, so scale-test at 360x640 and 640x360.
- Minimum tap target 44x44 CSS px (Apple HIG) / 48 dp (Material); keep 8 px gaps between targets.

### 1.3 UI polish

Buttons [K]: pill or rounded-rectangle, vertical gradient (lighter top), 4-8 px darker bottom lip that compresses to 0-2 px on press, 2-4 px dark outline or inner stroke, a thin top gloss. Pressed state: translateY 2-4 px plus scale 0.95-0.97 over 60-100 ms. Hover (desktop): scale 1.04-1.06 and brightness +8 percent. Disabled: desaturate and lower value, not just lower opacity. Label centered, bold, with outline or shadow.

Panels [K]: rounded, a header strip or title tab, inner padding at least 16 px (24 px preferred), a dark translucent backdrop (black at 40-60 percent) behind modals to isolate them, drop shadow below. Avoid thin 1 px borders and default gray.

Typography [K]: one rounded or chunky display font (examples in the licensing-safe set: Lilita One, Baloo 2, Fredoka, Luckiest Guy, Titan One, all on Google Fonts under OFL) for titles and numbers; one clean sans (Nunito, Poppins, Inter) for descriptions. Display text gets 3-6 px dark outline plus 2-4 px offset shadow, optionally a gradient fill. Letter-spacing slightly positive on all-caps. Line height 1.2-1.4. Do not use more than 3 sizes per screen plus the hero number.

Number display [K]: right-align or center numbers, use tabular figures or a monospace-width display font so digits do not jitter while counting up. Abbreviate with K, M, B, T then aa, ab or scientific for idle games; show at most 3 significant digits after the abbreviation (e.g. 12.3K). Keep a permanent icon next to every currency. Count up over 300-800 ms with ease-out rather than snapping. Bump (scale 1.0 to 1.2 to 1.0 over 150 ms) when the value rises.

Icons [K]: one stroke weight, one corner style, same size grid (24, 32, 48, 64 px), same palette; icons sit in a consistent container (circle or rounded square). Prefer pictorial icons for core stats (coin, gem, heart, star) and avoid text-only buttons for repeating actions.

Spacing and grid [K]: base unit 8 px; common steps 8/16/24/32/48. Group related things closer (8-16) than unrelated (32+). Align left edges and centers to a few shared axes. Equal margins to screen edges (16-24 px).

Safe areas [K]: keep HUD elements at least 5 percent (about 48 px at 1080) in from edges; CrazyGames and Poki overlay their own loading screens, ad frames, and on mobile the notch and rounded corners. Keep the primary action reachable in the bottom 40 percent in portrait. Support both 16:9 landscape and 9:16 portrait with a responsive layout (anchor to edges, scale to fit, never letterbox ugly bars; fill extra space with background art).

### 1.4 The first-screenshot impression

[K] A reviewer or player decides from one frame. The strong first frame has: a clear focal point (center or golden-third), a large readable hero number or board, saturated background that is calmer than the foreground, 3-5 UI elements visible at most, a primary button with highest contrast, and visible "stuff happening" (floating coins, particles, a character mid-motion). It does not have: empty gray areas, debug text, placeholder art, tiny paragraphs, or a menu wall.

---

## 2. Juice and motion

### 2.1 The "Juice it or lose it" idea (Jonasson and Purho, GDC Europe 2012) [K, search could not confirm details, see Sources]

Summary in my words: take a bare-bones breakout clone and add, step by step, small effects: tween the bricks in, wobble the paddle, add squash and stretch to the ball, spawn particles on every hit, flash and shake on impact, play layered sounds with pitch variation, add a trail and a background pulse. Each step alone is minor; together the same rules feel alive. Lesson: feedback should be proportional to importance, and everything that responds to input should visibly react.

### 2.2 The "Art of screenshake" idea (Jan Willem Nijman, Vlambeer, 2013) [F partial, K]

Verified detail from a write-up [F]: one pistol shot kicks the camera back about 6 pixels opposite the aim direction and adds about 4 to a screenshake value that decays quickly. The rest of the talk (from memory [K]) stacks a few dozen tweaks on a simple shooter: more bullets, bigger muzzle flash, bullet casings that persist, enemy knockback and a short hit pause, camera lerp toward aim, permanent leftover debris, weapon recoil, sound with variation, and slightly more screen shake only on strong events. Lesson: layer small effects, tune each by feel, and do not overdo shake.

### 2.3 Timing and easing cheat sheet [K, tune by feel]

| Effect | Duration | Easing |
|---|---|---|
| Button press down | 60-100 ms | ease-out |
| Button release | 100-160 ms | easeOutBack (overshoot ~1.1) |
| Element appears (modal, popup) | 200-300 ms | easeOutBack, scale 0.8 to 1.0 plus fade |
| Element disappears | 120-200 ms | ease-in, scale to 0.9 plus fade |
| Screen transition | 250-400 ms | ease-in-out, slide or wipe |
| Number count-up | 300-800 ms | ease-out |
| Coin fly to HUD | 500-800 ms | ease-in-out with arc, staggered 30-60 ms per coin |
| Squash on land/hit | 80-150 ms in, 150-250 ms recover | squash then spring back with 1 overshoot |
| Hit-stop (freeze) | 30-80 ms (up to 120 ms for big hits) | n/a |
| Screen shake | 100-250 ms | decaying amplitude (exponential) |
| Idle breathe | 1.5-2.5 s loop | sine |
| Tooltip / small feedback | 150-200 ms | ease-out |
| Level-complete celebration | 1.0-2.0 s | staged |

General rules [K]:
- Never linear for UI or character motion (except spinners and scrolling marquees).
- Ease-out (fast start, slow end) for things entering; ease-in for exits; ease-in-out for position moves across the screen.
- Anything under ~100 ms reads as instant; over ~500 ms for routine UI feels sluggish. Material Design guidance puts most UI transitions in the 150-300 ms range [K].
- Stagger lists and grids by 30-60 ms per item rather than animating all at once.
- Overshoot values: easeOutBack with constant about 1.70158 is the standard Penner value; use 1.2-1.7 for subtle.
- Use springs (stiffness about 170-300, damping about 12-26) for draggable and scalable elements.

### 2.4 Squash, stretch, anticipation, follow-through [K]

From the animation principles (Disney's twelve, as applied to games): preserve volume (if scaleY drops to 0.8, scaleX rises to about 1.2); stretch along the direction of travel at speed (1.2 to 1.4 along motion), squash on impact; anticipation is a small opposite move before the main action (scale to 0.9 for 60-100 ms before a jump or reward pop); follow-through means parts keep moving after the main stops (overshoot then settle in 2-3 oscillations of decaying amplitude); secondary motion (hair, tails, UI sparkle) lags the main body.

### 2.5 Particles [K]

- Burst on action: 8-20 particles, lifespan 300-700 ms, random speed in a cone, gravity, scale from 1.0 to 0 and alpha fade.
- Use 2-3 shapes (circle, star, small square) in palette colors, plus additive glow for rewards.
- Always include a brief flash or ring (100-150 ms) at the origin.
- Keep total live particles under about 300 on mobile browsers; pool objects; avoid allocating per frame.
- Ambient particles (dust, sparkles, bokeh) at low alpha, slow drift, give the background life.

### 2.6 Number popups and floating text [K]

Spawn at the source, rise 40-80 px over 600-900 ms, ease-out, fade out over the last third, start at scale 0.6 and pop to 1.2 then 1.0 in about 150 ms. Colors by meaning (white normal, yellow critical, green heal/gain). Randomize x by plus or minus 10-20 px to avoid stacking. Make crits bigger (1.3 to 1.6x) with a different outline color. In clickers, cap simultaneous popups (30-50) and merge when rapid.

### 2.7 Reward celebrations [K]

Tier them. Tier 1 (every tap): pop plus tiny particles plus sound. Tier 2 (purchase/upgrade): button flash, icon bounce, ring burst. Tier 3 (milestone/level up): dim background to 60 percent, rays or glow rotating behind a centered reward icon, confetti burst, count-up numbers, title banner dropping in with overshoot, then a bright "Continue" button after a 0.6-1.0 s delay so it cannot be mis-tapped. Total under about 2 s of forced animation. Rewards fly into the HUD counter and the counter bumps.

### 2.8 Idle animation and transitions [K]

Every on-screen character or primary object should have a loop: breathe (scale Y 1.00 to 1.03), blink at random 2-5 s intervals, bob (plus or minus 4-8 px, 2 s). Buttons that should be pressed (a ready upgrade, "claim") pulse (scale 1.0 to 1.08, 0.8-1.2 s) or shine (a diagonal light streak sweeping every 3-4 s). Transitions: avoid hard cuts between screens; use fade/slide 250-400 ms or a shape wipe; keep the previous screen visible under the transition so the player keeps context.

### 2.9 Restraint [K]

Juice is relative: if everything shakes and flashes, nothing is emphasised. Reserve the biggest effects for the rarest events. Provide settings for sound and shake/flash reduction (accessibility; photosensitivity: avoid flashes above 3 per second).

---

## 3. Teardowns (patterns only, no assets copied)

Portal pages: crazygames.com/c/idle returned HTTP 404 to a plain fetch [F]; crazygames.com/t/idle listed as most popular idle games: Mage Castle Idle Defense, Evil Tower, Leek Factory Tycoon, Claw Master, Meeland.io, Lumber Hero: Idle Defense, The MachinEGG, Firestone Idle Clicker Online RPG, Forest Nothing, Steal Eggs [F] (titles skew to defense, factory, food and RPG themes with a mascot or hero, not abstract clickers); Poki's clicker page listed Spacebar Clicker, Duck Merge, Kiwi Clicker, Idle Ants, Idle Success, Cat Clicker RE, Smash It, Home Builder Clicker, Quest Clicker, Idle Construction 3D, plus popular Subway Surfers, Aquapark.io, Paper.io 2 [F]. Thumbnails are square logo-style images, 204 px in featured rows and 94 px in dense lists [F], so key art must work at about 94 px. Fetch could not show the artwork itself. TODO for a follow-up: screenshot these pages with headless Chrome on the XPS (not the Mac) and describe thumbnails.

### 3.1 Block Blast style puzzle [K]
Dark blue/purple background with a clearly lighter grid board; blocks are glossy, saturated, bevelled squares in 6-8 distinct hues that never touch the background hue family; a bold score at the top with a gold crown/best-score; pieces tray at the bottom within thumb reach. Clearing lines triggers a sweep flash, blocks shatter into square particles, a combo word ("Great!", "Excellent!") scales in with overshoot, and screen micro-shake; score counts up. Everything is high contrast so the board state reads at a glance. Thumbnail: the board mid-play with a colorful cluster and a big combo word.

### 3.2 Royal Match / King-style match-3 [K]
Rich saturated environments, cartoon characters with expressive faces, chunky 3D-rendered pieces with soft shading and rim light, ornate but clean gold-bordered panels, big rounded buttons with strong lips and gloss, bright cartoon fonts with thick outlines. Heavy but short celebrations (pieces burst, lightning, confetti), clear tutorial hands and glows. Pattern to borrow: gold-framed panels, one hero character, very consistent bevel/highlight logic. Pattern not to copy at small-studio scale: 3D-rendered asset volume.

### 3.3 Supercell (Clash Royale, Clash of Clans, Brawl Stars) [K]
Strong unified UI language: thick dark-blue outlines on everything, chunky pill buttons with bottom lips, bold italic display font with heavy outline and drop shadow, saturated single-hue panels (blue for neutral, green for go, red/orange for danger/attack, purple for rare), gold and gem as the only metallic accents. Characters have exaggerated proportions (big head, big hands) and instantly distinct silhouettes. Animation: every element has idle motion, chests wobble before opening, rewards pop with squash/stretch, numbers bump. Key lesson: a style guide of outline weight, shadow offset and color-by-meaning applied rigidly.

### 3.4 Cookie Clicker and modern idle games [K]
Cookie Clicker (web classic): the hero object is big, centered, and responds to every click (shrinks to about 0.95 on press, pops back) with falling cookie particles and a "+N" floater; the big number is the top header; side panels list buildings with small icons and counts. The look is deliberately informal; it succeeds on function and constant feedback, and loses polish via mismatched asset sources, which is a thing to avoid. Modern idle games (Egg Inc style, AdVenture Capitalist, Idle Miner-type) add: a consistent character set, chunky buy buttons showing cost in a colored pill (green when affordable, grey when not), progress bars with shine, milestone celebrations, floating currency, prestige screens with dramatic dimmed overlays, and a bottom tab bar of 4-5 icons with a red notification dot. Pattern: a vertical list of upgrade cards (icon left, name and level center, buy button right) with affordability state shown by color, not text alone.

### 3.5 Top portal titles [F partial, K]
Names from Poki's clicker list [F] suggest: animal mascots (Duck, Cat, Kiwi, Ants), themed .io-style simplicity (Aquapark.io, Paper.io 2), and merge/builder variants. Common thumbnail pattern [K]: single mascot or object, face visible, bright saturated gradient, thick outline, 1-3 word logo with outline, a hint of the mechanic (arrow, merge sparkle, big number). Portal best practice [K]: upload thumbnails in the required sizes (CrazyGames asks for multiple ratios such as 16:9 and 1:1; check each portal's current spec in its developer docs), no portal logos, no misleading text, no screenshot with UI clutter.

---

## 4. Common amateur mistakes (and how to spot them in a PNG)

See checklist below. Typical causes: default fonts, mixed art sources, flat unstyled rectangles, low value contrast, text over busy art, uneven spacing, huge empty areas, tiny tap targets, too many colors, inconsistent outlines, no hero focus, numbers without abbreviation, no shadows, misaligned items, stretched images (wrong aspect), blurry upscaled sprites mixed with crisp ones, cut-off text, visible placeholder text or debug overlay, HUD colliding with portal chrome.

---

## 5. Talks and articles worth citing (in my words)

- "Juice it or lose it", Martin Jonasson and Petri Purho, GDC Europe 2012: incremental juice on a breakout clone; proves the same rules can feel dead or alive. [K]
- "The Art of Screenshake", Jan Willem Nijman, Vlambeer, 2013: stacks many small feel tweaks on a shooter; shake is one of many; documented example 6 px camera kick plus 4 shake added per shot [F]. [K]
- "Game Feel" by Steve Swink (book): input, response, context; response should feel physical. [K]
- Disney's twelve principles of animation (Thomas and Johnston, "The Illusion of Life"): squash and stretch, anticipation, follow-through, slow in slow out, arcs, secondary action, timing, exaggeration, appeal. [K]
- Robert Penner's easing equations (2001-2002): standard easing function set (quad, cubic, back, elastic, bounce); easings.net visualises them. [K]
- Material Design motion guidelines: durations around 100-300 ms for UI, asymmetric easing. [K]
- Apple Human Interface Guidelines: 44 pt minimum touch targets, safe areas. [K]
- Supercell and King public art talks and interviews on UI consistency and readability; Supercell's "make fewer, better" philosophy. [K]
- WCAG 2.2 contrast ratios: 4.5:1 normal text, 3:1 large text and UI components. [K]

---

## Screenshot review checklist (yes/no; any "no" on 1-12 is a blocker)

Focus and composition
1. Is there one obvious focal point (hero object, board or big number) within 1 second of looking?
2. Does the main subject occupy at least 40 percent of the play area height?
3. Is the scene free of large empty or flat grey areas (more than about 25 percent of screen)?
4. Are at most 5 UI elements competing for attention?

Color and contrast
5. In a grayscale/blurred copy, do play objects separate clearly from the background?
6. Does text meet roughly 4.5:1 contrast against its fill (3:1 for large display text)?
7. Are there 6 or fewer distinct hues in total, with one hue clearly the primary action color?
8. Is gold/yellow used only for rewards and currency?
9. Is the background calmer (lower saturation or contrast) than the foreground?
10. Are there no pure #000 or #FFF blocks, and no neon-on-neon vibrating pairs?

Consistency
11. Is outline weight the same across characters, buttons and icons (or consistently absent)?
12. Do all corner radii come from a small set, with no sharp boxes mixed with pills?
13. Does light come from one direction (highlights top, shadows bottom) everywhere?
14. Do all icons share stroke weight, size grid and style?
15. Are there no mixed art sources (stock vs hand-drawn, pixel vs vector, different resolutions)?

Typography and numbers
16. Are there at most 2 font families?
17. Do headings and numbers have outline or shadow and a bold display face?
18. Is the smallest text at least 16 px at a 1080-px canvas height (and readable at 360 px height)?
19. Are large numbers abbreviated (K, M, B) and aligned, with a currency icon beside them?
20. Is no text clipped, overlapping other elements, or running edge to edge?

UI polish
21. Do buttons have depth (gradient, lip or shadow) and a clear label, not flat rectangles?
22. Is the primary action the highest-contrast element and in the lower half (portrait) or a reachable corner?
23. Are tap targets at least 44 px with 8 px gaps?
24. Is spacing on a consistent 8 px grid, with equal screen margins of at least 16 px?
25. Are modals dimmed backdrops with shadow, and panels padded at least 16 px?
26. Are affordable vs unaffordable states visibly different (color, not just text)?

Safe area and layout
27. Is all essential UI at least 5 percent from every edge?
28. Does nothing important sit where portal chrome or ads overlay (top bar, bottom banner)?
29. Does the layout fill both 16:9 and 9:16 without black bars or stretched art?

Polish and life
30. Is there visible life in the still frame (particles, floaters, glow, character pose mid-action)?
31. Do sprites share the same resolution crispness (no blurry upscaled assets)?
32. Is there a shadow or ground contact under objects so they do not float?

Hygiene
33. Is there no placeholder text, debug overlay, FPS counter, or lorem ipsum?
34. Are there no browser default elements (default buttons, scrollbars, blue links, focus rings)?
35. Is the game title or core mechanic clear from the frame alone?

Thumbnail (separate PNG)
36. At 94 px square, can you still tell what the subject is?
37. Is there 3 words or fewer of text, with outline, and no tiny text?
38. Does it have a face, character or iconic object rather than a UI screenshot?
39. Is the background saturated with a gradient, and the subject lighter or darker than it?
40. Does it avoid portal logos, borders, and misleading claims?

---

## Sources

Fetched or searched this session [F]:
- https://poki.com/en/clicker (title list and thumbnail sizes)
- https://infovore.org/?p=5275 (Making Game "Feel", Nuclear Throne shot example: 6 px kick, +4 screenshake)
- https://kenney.nl/learn/must-see-videos-for-indie-developers (links to both talks)
- https://en.wikipedia.org/wiki/Vlambeer
- https://www.crazygames.com/t/idle (popular idle titles; /c/idle was 404)
- https://m3.material.io/styles/motion/easing-and-duration/tokens-specs (fetch returned no values, so Material numbers stay [K])
- https://www.gamedeveloper.com/design/game-feel-the-secret-ingredient (qualitative only, no numbers)

Background knowledge to verify [K]:
- Juice it or lose it (GDC Europe 2012): search GDC Vault / YouTube "Juice it or lose it Jonasson Purho"
- The Art of Screenshake (Nijman, 2013): YouTube, "The Art of Screenshake Jan Willem Nijman"
- https://easings.net (Penner equations)
- https://m3.material.io/styles/motion/overview (motion durations)
- https://developer.apple.com/design/human-interface-guidelines/ (touch targets, safe areas)
- https://www.w3.org/TR/WCAG22/ (contrast)
- Swink, Game Feel (2008); Thomas and Johnston, The Illusion of Life (1981)
