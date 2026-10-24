# Tech stack and engineering practice for small HTML5 portal games (Oct 2026)

Research for the Taktek "building HTML5 games" skill. Items marked (measured) were fetched on 24 Oct 2026 from jsDelivr/npm. Items marked (portal doc) come from CrazyGames/Poki docs. Items marked (judgment) are our recommendations, not facts. Items marked (memory) are from prior knowledge and not re-verified today.

## Summary (default stack)

1. Default language and tooling: TypeScript + Vite, Node 20+ (Node 18 is end-of-life; install Node 22 LTS via nvm or uv-style tool on the box). Vitest for logic, Playwright for the browser.
2. Default engine for most games: Phaser 4 (stable since 10 Apr 2026, v4.2.1 on 9 Jul 2026). Largest LLM training coverage, scenes/tweens/audio/input/scale manager built in, ships skills files for AI agents, Poki has a Phaser SDK guide.
3. Cost of Phaser 4: 1.38 MB minified, 356 KB gzip (measured). Fine for the 20 MB mobile cap, but eats ~10 percent of a tight 3 MB budget.
4. UI-heavy idle/clicker: plain DOM + CSS + a tiny canvas or CSS particles layer, no engine at all (or Pixi v8 only if you need many animated sprites). Smallest bundle, best text, a11y and layout, fastest load, easiest for agents to test with Playwright selectors.
5. Grid puzzle: Phaser 4 (or Kaplay when the game is under ~1500 lines). Tile tweens, input, scale manager come free.
6. Physics/arcade: Phaser 4 with Arcade physics (Matter only if truly needed). Kaplay is a fine lighter alternative for jam-sized games (70 KB gzip, measured).
7. Do not pick Godot/Unity/Cocos/Defold for the default: heavier downloads, editor-driven scenes that agents cannot easily author, thin LLM coverage (Defold, Cocos).
8. Portal SDKs are plain script tags (CrazyGames `crazygames-sdk-v3.js`, Poki `poki-sdk.js`). Wrap both behind one `platform.ts` adapter so the game never imports a portal directly.
9. Budgets (judgment): first interactive frame under 3 s on throttled 4G, initial download under 3 MB gzip target, hard cap 8 MB; portal caps are looser (CrazyGames 50 MB initial, 20 MB for mobile homepage).
10. Game loop: fixed 60 Hz logic step with accumulator, render every rAF, delta clamp, pause on `visibilitychange`. Idle games compute offline progress from timestamps, not ticks.
11. Save system: single JSON blob in localStorage wrapped in try/catch (Poki incognito rule), `version` field and an ordered migration array, export/import string, mirror to CrazyGames Data module when present.
12. Audio: unlock AudioContext on first pointer/touch gesture and again on `touchend`/`click` after iOS interruption (CrazyGames doc). Howler (9.7 KB gzip, measured) or raw WebAudio + ZzFX for synth SFX.
13. Juice: GSAP is free including all plugins under its standard license (28 KB gzip core, measured), but engines already have tweens; prefer built-ins, add GSAP only for DOM-heavy UIs.
14. Verification an agent can run: Vitest on pure logic, a headless Node balance simulator (greedy buyer, time-to-milestone table), Playwright with `page.clock` to fast-forward idle time, screenshots at 8 viewports, console-error gate, bundle-size gate, scripted playthrough through a `window.__test` hook.
15. No mainstream autonomous web-game playtesting tool exists; build a thin Playwright bot per game and gate on invariants (no errors, progress reachable, score changes, no soft-lock).

---

## 1. Engine choice in 2026

### Measured sizes (jsDelivr, minified, gzip as served)

| Library | Version | Raw min | Gzip | Note |
|---|---|---|---|---|
| Phaser | 4.2.1 (latest) | 1.38 MB | 356 KB | full build, no tree-shaking; custom build can trim |
| Phaser | 3.90.0 (last v3) | 1.20 MB | 318 KB | |
| PixiJS | 8.22.0 | 841 KB | 238 KB | full pixi.min.js; ESM tree-shaken app is smaller (memory: roughly 100-170 KB gzip for sprites+text+ticker) |
| Kaplay | 3001.0.19 | 189 KB | 70 KB | v4000 exists as a "next" preview, not stable |
| Excalibur | 0.32.0 | 574 KB | 148 KB | |
| LittleJS | 1.28.0 | 500 KB | 155 KB | file measured was `dist/littlejs.min.js`; may include extras, check the leaner build |
| Howler | latest | 36 KB | 9.7 KB | |
| GSAP core | latest | 73 KB | 28 KB | |

### Per engine

**Phaser 3 / 4.** Phaser 4 "Caladan" released 10 Apr 2026; 4.1.0 on 30 Apr; 4.2.1 "Giedi" on 9 Jul 2026 (stability and ESM fixes). New renderer, unified filter system (bloom, blur, glow etc.), GPU gradient and noise objects, one-line lighting. Public API is described as "almost identical" to v3, so v3 tutorials mostly still apply. It ships skills files for AI coding agents. TypeScript types included. Mobile performance is good in v3; v4 claims large batching gains (vendor claim, not verified). Risk: v4 is 6 months old, so some LLM answers will be v3-era (usually still valid) and some plugins lag. Pin to `phaser@4` exact version in package.json. Portals: Poki has an official Phaser 3 SDK guide (portal doc); CrazyGames' SDK intro page lists plugins for Unity, GameMaker, Construct, Godot, Cocos, Defold but not Phaser, so use the plain script SDK. Rule: either portal works with any engine through the plain JS SDK.

**PixiJS v8.** Renderer only: sprites, text, graphics, filters, ticker, WebGL + WebGPU. You supply scenes, audio (`@pixi/sound`), tweens, input mapping, layout (`@pixi/ui`, `@pixi/layout`). v8 init is async (`await app.init({...})`), a common agent mistake is writing v7 code (`new Application({...})`, `app.view`). Great TypeScript, stable docs. Good when you want a custom thin framework and the smallest render footprint. Poki lists it as a low-level control option (Poki blog). No official portal plugins; use plain SDK.

**Kaplay (Kaboom successor).** Stable line is 3001.x (70 KB gzip, measured). "Strong TypeScript support" per site. Component API: `add([sprite(), pos(), area(), body()])`, `onClick`, `tween`, `setGravity`. Very compact code, easy for LLMs to write, but LLM training data is split between Kaboom 2000-3000 and Kaplay names, so agents sometimes emit removed Kaboom APIs. Weaker for UI-heavy games (no layout system), mobile scaling needs care (letterbox mode option). Best for jam-style arcade and simple puzzles.

**Excalibur.** TypeScript-first, 148 KB gzip, good scene/actor/physics model, smaller community and less training data than Phaser. Viable, not default.

**LittleJS.** Tiny, fast, built-in physics and sound (ZzFX style), for very small arcade games with a single-file mindset. Small docs, so agents do fine, but limited UI and fewer examples.

**Plain DOM + CSS + canvas.** Zero engine bytes. CSS transitions/animations, `requestAnimationFrame`, one `<canvas>` for effects. Best for idle/clicker, card, word, quiz and menu-heavy games. Agents write it fluently and Playwright can click real buttons by role/text. Weak for large numbers of moving sprites (use canvas 2D, or Pixi).

**Godot 4 web export.** Real editor, GDScript. Default web template is roughly 8-10 MB wasm uncompressed (memory), downloads ~4-6 MB compressed, single-threaded export (4.3+) avoids COOP/COEP header issues. CrazyGames has a Godot 3/4 addon, Poki has a Godot guide (both portal docs). Poki's 2026 blog notes lazy-loading is still being built. Poor fit for our flow: scenes are `.tscn` text but editor-centric, agents can write them yet iteration is slower, loads heavier than any JS option.

**Defold.** Very small runtime (~1-2 MB, memory), Lua, both portals list Defold extensions (portal docs). Weak LLM coverage and API stability for agents. Skip unless a game needs native-feeling performance.

**Cocos Creator.** Editor-driven, scene files edited in GUI, CrazyGames and Poki have Cocos integrations (portal docs). Poor for agents. Skip.

### Recommendation by game type

| Type | Default | Why | Fallback |
|---|---|---|---|
| UI-heavy idle/clicker | DOM + CSS + tiny canvas, Vite + TS, no engine | Smallest, text and layout native, easy Playwright asserts, offline progress is pure state | Pixi v8 if many animated sprites |
| Grid puzzle (match-3, 2048, sokoban, word) | Phaser 4 (or DOM for pure text/board games) | Tweens, input, scale manager, atlases; board logic stays in a pure TS module | Kaplay under ~1500 lines |
| Physics/arcade (runner, shooter, breakout, flappy) | Phaser 4 + Arcade physics | Collision, groups, cameras, particles, audio all built in | Kaplay or LittleJS for the tiniest |

Keep game logic engine-independent in every case (`src/core/`), so a rewrite of the view layer never touches rules or balance.

---

## 2. Project template (Vite + TypeScript)

### Starter folder layout

```
my-game/
  package.json            # scripts: dev, build, test, sim, e2e, size, check
  vite.config.ts          # base: './' (CrazyGames needs relative paths), build.target es2020
  tsconfig.json           # strict true
  index.html              # one canvas/div#app, viewport meta, user-select none
  public/
    sdk/                  # optional vendored poki-sdk.js (external requests blocked on Poki)
  src/
    main.ts               # boot: platform.init -> load -> start
    platform/
      platform.ts         # interface: gameplayStart/Stop, midgameAd, rewardedAd, save/load, isMobile
      crazygames.ts  poki.ts  local.ts   # picked at runtime, local = no-op
    core/                 # PURE TS, no DOM, no engine, fully unit-tested
      state.ts            # State type, initialState()
      rules.ts            # step(state, dt) / applyAction(state, action)
      balance.ts          # constants and cost formulas (single source of truth)
      rng.ts              # seeded PRNG (mulberry32)
      save.ts             # serialize, migrate, validate
    engine/               # engine-specific view layer
      scenes/ Boot.ts Menu.ts Game.ts Pause.ts
      loop.ts  scale.ts  audio.ts  input.ts  juice.ts
    ui/                   # DOM overlay (menus, settings, HUD text)
    assets/               # source art/audio, packed by script
  tools/
    pack-atlas.mjs        # free-tex-packer-core or similar -> public/atlas/*.json+png
    sim.ts                # balance simulator (runs in Node/tsx using core/)
    size-check.mjs        # gzip dist, fail over budget
  tests/
    unit/*.test.ts        # vitest
    e2e/*.spec.ts         # playwright: smoke, viewports, playthrough
  dist/                   # build output, zip root = index.html
```

### Practices

- **Assets and atlases.** Pack sprites into 1-3 atlases (max 2048x2048, one texture per draw batch), prefer WebP for images (Chrome/Edge/Safari all support), OGG/MP3 pair or just MP3/AAC for audio (single format AAC/MP3 is safe everywhere now). Preload only what the first scene needs; load later levels in the background. Poki blog: each extra MB before play costs a couple percent of players.
- **Scene management.** Phaser: Boot -> Menu -> Game -> UI overlay scene. Plain: a tiny state machine `setScene('menu'|'game'|'pause')`. Scenes only render and forward input; rules live in `core/`.
- **Game loop.** Fixed timestep logic, variable render:
  ```ts
  const STEP = 1000 / 60; let acc = 0, last = performance.now();
  function frame(now: number) {
    acc += Math.min(now - last, 250); last = now;      // clamp after tab sleep
    while (acc >= STEP) { update(STEP); acc -= STEP; }
    render(acc / STEP);                                 // interpolate
    requestAnimationFrame(frame);
  }
  ```
  This is refresh-rate independent (120/144 Hz screens run the same logic). Phaser already uses a fixed-ish delta; for physics set `fps: { target: 60, smoothStep }` or use `physics.arcade.fps`. Idle games: tick with real elapsed seconds, not frame counts, and on load compute offline progress from `Date.now() - lastSaved` (cap it, e.g. 8 h, and show a "welcome back" summary).
- **Resize and letterbox.** Design resolution 1280x720 (16:9, matches Poki 640x360, 836x470, 1031x580 reference sizes). Scale to fit with preserved aspect ratio (Phaser `Scale.FIT` + `CENTER_BOTH`), fill the bars with a themed background rather than black where possible. Portrait: a second layout (e.g. 720x1280) chosen by `matchMedia('(orientation: portrait)')` or aspect < 1; do not just scale the landscape one. Poki says cover the full canvas on mobile in portrait or landscape; CrazyGames allows black bars/background images for portrait and shows its own rotate prompt, so do not lock orientation. Respect safe-area insets (`env(safe-area-inset-*)`) because CrazyGames app fullscreen requires it, and keep important UI away from the Poki pill (use `movePill` if needed).
- **devicePixelRatio.** Render at `min(devicePixelRatio, 2)` (cap at 2, even 1.5 on weak phones). CrazyGames uses DPR 1 on iOS and low-memory Android for Unity, an example of why capping matters. Provide a quality fallback: if the 60-frame moving average stays above 24 ms, drop DPR to 1.
- **Audio unlock.** Create/resume the `AudioContext` on the first `pointerdown`/`touchend`. On iOS the context can go `interrupted`/`suspended` after backgrounding; CrazyGames says to call `resume()` inside a user gesture (`touchend`/`click`) and that a visibility listener alone is not enough. Keep a mute toggle that persists, and mute automatically around ads (Poki rule).
- **Save system.** Shape: `{ v: 3, savedAt, data }`. Keep `migrations: Array<(d:any)=>any>` where index n upgrades v n to n+1; on load run all migrations from the stored version, then validate with a schema (zod or hand-rolled) and fall back to defaults on failure. Write on a 5-10 s debounce and on `visibilitychange`/`pagehide`. Wrap every `localStorage` call in try/catch (Poki requires playability in incognito). Offer export/import string. Poki syncs localStorage for logged-in users automatically; CrazyGames has a `data` module (cross-device) to mirror into when `SDK.environment !== 'disabled'`. Unit-test: v1 fixtures migrate to current, corrupted JSON recovers.
- **Pause on visibility.** On `document.visibilitychange` hidden: pause logic and music, call `gameplayStop()`; on visible: show a tap-to-resume, then `gameplayStart()`. Poki wants `gameplayStart()` on first input (not on load) and never two identical events in a row; ESC or space toggles pause on desktop; `commercialBreak()` only when leaving pause into gameplay; no custom ad timers. For idle games, the game keeps accruing offline-style on resume rather than running hidden.
- **Portal adapter.** One interface, three implementations. SDK init: CrazyGames `await window.CrazyGames.SDK.init()` (script `https://sdk.crazygames.com/crazygames-sdk-v3.js`, works on localhost in a `local` environment, disabled elsewhere so guard calls); Poki `PokiSDK.init()` then start the game in both `then` and `catch`, `gameLoadingFinished()` after load. Bundle fonts/libs: external requests are blocked on Poki; external links must use `PokiSDK.openExternalLink`.
- **Misc.** CSS `user-select: none` on body (CrazyGames), prevent page scroll on arrows/space/wheel, no right-click menu, relative asset paths only, must run in Chrome and Edge and ideally Safari, test with 4 GB RAM Chromebook in mind.

---

## 3. Testing and verification an agent can run alone

### Layers

1. **Unit tests (Vitest) on `core/`.** Pure functions with a seeded RNG: rule transitions, scoring, win/lose, save migration fixtures, cost formulas monotonic, no NaN/Infinity (idle games break with big numbers; test the number-format and big-number path at 1e3, 1e15, 1e100).
2. **Headless balance simulator (`tools/sim.ts`).** Runs the real `core/` in Node with a policy, prints a table, asserts targets. Idle model (the standard one):
   - Cost of the n-th unit: `cost = base * r^n`, r typically 1.07 (AdVenture Capitalist worked example) to 1.15 (common tutorial value). Production usually linear or polynomial in units owned, so costs outgrow income and force the player to the next generator or prestige.
   - Payback time of a purchase: `cost / delta_income_per_sec`. Greedy policy: always buy the item with the lowest payback. A rule of thumb from one calculator: a buy is strong if payback is under 25 percent of the play horizon, skip if past the horizon.
   - Time-to-milestone: simulate with a policy at three skill/attention levels (active clicker every 1 s, casual checking every 5 min, offline 8 h). Output first-purchase time, each tier unlock time, first prestige time, session 1 (10 min) and session 2 targets.
   - Sanity targets (judgment): first upgrade under 10 s; first meaningful unlock within 60 s; a new thing to buy every 15-45 s in the first 5 min; no stretch above 3 min with nothing affordable unless a prestige is on screen; first prestige or ending of content in 20-40 min for a portal session; offline cap matches the narrative. Fail CI if a milestone drifts more than 25 percent from target.
   - For puzzle/arcade: simulate 10k seeded runs with a random bot and a greedy bot; check solvability rate, average game length, score distribution percentiles, difficulty ramp per level (bot win rate monotonic decreasing), no dead boards.
3. **Playwright (headless Chromium) browser tests.**
   - Smoke: page loads, zero `console.error`, zero `pageerror`, zero failed requests (404s), canvas non-blank.
   - Viewports: 1920x1080, 1366x768, 1280x720, 1024x576 (16:9 sizes), 844x390 and 390x844 (phone landscape/portrait), 768x1024 (tablet), 360x640 (small Android). For each: screenshot, assert canvas fits viewport, no horizontal scroll, key button bounding boxes are within the viewport and at least 44x44 CSS px for touch. Compare to committed baselines with `expect(page).toHaveScreenshot()` (a masked/threshold diff); the agent reviews new screenshots by eye for the first run.
   - Idle fast-forward: `page.clock.install()` then `page.clock.fastForward('08:00:00')` or `runFor` to test offline progress and long-session behavior without waiting. The game must read time via `Date.now()`/`performance.now()` that the fake clock controls.
   - Scripted playthrough: expose `window.__test = { state(), act(name,...args), seed(n), skipTo(milestone) }` only when `?test=1`. The bot clicks real UI for a golden path (menu -> play -> first win/first 10 purchases), then asserts invariants (score increased, currency never negative, no soft-lock: some action always available).
   - Input: both mouse and touch (`hasTouch: true`, `page.touchscreen.tap`), keyboard for desktop.
   - Reload test: play, reload, state restored; localStorage disabled (incognito simulation) still plays.
4. **Perf budgets.**
   - Headless Chromium uses software GL (SwiftShader), so FPS numbers are pessimistic and not comparable to devices; use them as relative regression signals only. Measure with `requestAnimationFrame` sampling over 10 s via `page.evaluate`, or Chrome DevTools Protocol `Performance.getMetrics`. Emulate a slow phone with CDP `Emulation.setCPUThrottlingRate` (4x or 6x) and network throttling (`Network.emulateNetworkConditions`, Fast 3G/4G profile).
   - Budgets (judgment): median frame under 16.7 ms at 4x CPU throttle on a typical scene, p95 under 33 ms; JS heap under ~150 MB after 5 min; no growth in heap over a 5-minute soak (leak check, count DOM nodes and listeners too). Lighthouse can run from the XPS for load metrics.
   - Remember offload rule: headless browsing and Playwright run on the XPS, not the Mac.
5. **Bundle checks.** `size-check.mjs` walks `dist/`, sums raw and gzip bytes of JS, assets by type, total file count, and fails over budget (also fail if any single asset over 1 MB or any file over 5 MB). Add `rollup-plugin-visualizer` for a treemap when it fails. Tools: `size-limit`, `vite-bundle-visualizer`. Assert file count under 1500 and relative paths in built `index.html`.
6. **Static gates.** `tsc --noEmit`, eslint, a grep gate for `console.log` leftovers, `localStorage` outside the save module, absolute URLs (external requests blocked on Poki).

### Automated playtesting tools

No widely used off-the-shelf tool for autonomous playtesting of small web games. Options: (a) our own Playwright bot + `__test` hook (recommended, deterministic); (b) a Claude agent driving the page through screenshots (slow and costly; use once for "does it look and feel right", not in CI); (c) Poki Play Testing, which returns 10 to 20 recordings of real players within minutes of upload (Poki blog), the only real human signal and worth using once the build passes our gates; (d) commercial QA-bot vendors (e.g. modl.ai) and RL frameworks (Unity ML-Agents) exist but target Unity/native and are overkill here (memory, unverified for 2026).

---

## 4. Juice libraries and helpers

- **Tweening.** Use the engine's: Phaser `tweens.add` / `tweens.chain`, Kaplay `tween()`, Pixi has none built in. For DOM/Pixi/plain, GSAP: Webflow acquired GSAP and made it free for everyone, including formerly paid Club plugins (SplitText, MorphSVG etc.), commercial use allowed under the standard license. Caveat: the license forbids using it to build a product that competes with Webflow's visual animation tools; the license text defines permitted use as any website, web app or digital interface and does not name games, which is the normal case but unverified word-for-word. Core is 28 KB gzip (measured). Alternatives: a 50-line custom tween with easing functions (easings.net formulas), or `@tweenjs/tween.js` (small, MIT; memory). For tiny idle UIs, CSS transitions/Web Animations API need no library.
- **Easing set to use.** easeOutBack (pops, buttons), easeOutElastic (rewards), easeOutQuad/Cubic (movement), easeInOutSine (idle bobbing), spring for drag-release. Rule of thumb: UI feedback 80-200 ms, big rewards 400-800 ms.
- **Particles.** Phaser 4 particle emitters (built in); Pixi `particle-container` / `@pixi/particle-emitter` (memory); Kaplay `particles()`. For DOM idle games: 8-20 absolutely-positioned spans animated with Web Animations API, pooled; canvas confetti on a dedicated overlay canvas. Always pool objects and cap live particles (e.g. 200) for mobile.
- **Screen shake.** Camera offset with decaying trauma: `offset = maxOffset * trauma^2 * noise(t)`, trauma += hit, decays ~1.5/s. Phaser `cameras.main.shake(duration, intensity)`. Respect a "reduce motion" setting (also `prefers-reduced-motion`).
- **Other cheap juice.** Squash and stretch on click, number pop-ups that float up, count-up tweens on big numbers, hit-stop (30-60 ms freeze), color flash, a combo meter, pitch-randomized SFX, haptics via `navigator.vibrate` (Android only).
- **Audio.** Howler.js 2.x (9.7 KB gzip, measured): sprites, pooling, fades, auto-unlock; note CrazyGames reported Howler (and PlayCanvas) have shown audio issues on iOS interruption, so add your own `resume()` on gesture. ZzFX (~1 KB, MIT, memory) generates retro SFX from a parameter array at runtime: zero audio files, great for the byte budget. Music: one short loopable MP3/AAC (64-96 kbps), lazy-loaded after first frame.

---

## 5. Size and speed budgets for portals

| Source | Rule |
|---|---|
| CrazyGames (portal doc) | Total 250 MB max, 1,500 files max. Initial download up to 50 MB, and up to 20 MB to be eligible for the mobile homepage. With SDK, measured from load start to first `Gameplay start` event (menus excluded). Externally hosted: QA expects gameplay within 20 s. Must work on Chrome and Edge, smooth on a 4 GB RAM Chromebook, mouse + keyboard, touch if mobile, relative paths. |
| Poki (portal doc) | No numeric size cap on the requirements page: "small file size", progressive loading. Players tend to leave if loading takes over 10 s. Min 30 FPS, target 60 FPS on 3G+ (deals page). Third-party guide says 8 MB initial (unverified); a Defold guide suggests under 20 MB total; Poki talk shows conversion drops notably already at 10 MB initial in the US. Must run in incognito, 16:9 scaling, mobile full-screen. |

Taktek budgets (judgment, tighter than the portals because conversion to play falls with size):

- **First frame / interactive:** under 3 s on Fast 4G with 4x CPU throttle; a visible loading bar by 500 ms.
- **Initial download (to gameplay start):** target 3 MB gzip, hard cap 8 MB. Idle/DOM games should land under 1 MB. Phaser games: ~360 KB engine + under 2 MB assets.
- **Total:** under 20 MB so the same build qualifies for mobile homepage lists.
- **Per asset:** images WebP under 300 KB each, atlas under 1 MB each, music under 1.5 MB, SFX under 30 KB each (or ZzFX).
- **Runtime:** 60 FPS target, 30 FPS floor on a mid phone; heap under 150 MB.
- **Loading strategy:** engine + menu + first level first; everything else lazy; call the portal's "loading finished"/`gameplayStart` accordingly so the measured window is small.
- WebGPU: about 68 percent of Poki players had WebGPU-capable devices in June 2026; treat it as an enhancement, keep WebGL baseline (Poki blog).

---

## Open items worth verifying before the skill is finalized

- Phaser 4 gzip with a custom build and its Arcade physics only; Pixi v8 tree-shaken size for a typical sprite+text app (measure with a Vite build on the XPS).
- Whether CrazyGames now offers a Phaser plugin page (SDK intro did not list it).
- Exact Poki numeric requirements if any exist in the developer dashboard (public pages give none).
- GSAP license wording for games (low risk; ask GSAP licensing only if we ever ship a game-authoring tool).

## Sources

- Phaser stable release page, v4.2.1 "Giedi", 9 Jul 2026: https://phaser.io/download/stable
- Phaser 4 feature page: https://phaser.io/phaser4
- Wikipedia, Phaser (game framework): https://en.wikipedia.org/wiki/Phaser_(game_framework)
- CrazyGames technical requirements: https://docs.crazygames.com/requirements/technical/
- CrazyGames SDK intro (v3): https://docs.crazygames.com/sdk/intro/
- Poki HTML5 SDK guide: https://developers.poki.com/guide/sdk-html5
- Poki requirements and quality: https://developers.poki.com/guide/requirements-quality
- Poki deals page (FPS minimums): https://sdk.poki.com/deals
- Poki blog, building web browser games in 2026: https://poki.com/blog/building-web-browser-games-2026
- Defold Poki SDK best practices: https://defold.com/extension-poki-sdk/best-practices
- KAPLAY site: https://kaplayjs.com/
- GSAP standard license: https://gsap.com/community/standard-license/
- Webflow, GSAP becomes free: https://webflow.com/blog/gsap-becomes-free
- Game Developer, The Math of Idle Games part I: https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i
- Idle game payback calculator: https://west-games.com/idle-game-payback-calculator/
- Library sizes: jsDelivr CDN and npm registry, measured 24 Oct 2026 (phaser, pixi.js, kaplay, excalibur, littlejsengine, howler, gsap)
