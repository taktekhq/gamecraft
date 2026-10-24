# Portal playbook (CrazyGames first, then Poki)

Date: 2026-10-24. Research for the "launching a web game on portals" skill.

## Summary
1. CrazyGames needs 3 covers (1920x1080, 800x1200, 800x800), title-only art, plus two silent 15-20 s preview videos (16:9 and 2:3, 1080p, under 50 MB).
2. Size: 250 MB total, 1,500 files, initial 50 MB max (20 MB for mobile homepage); with SDK it is measured to the first `gameplayStart`.
3. Even Basic Launch needs `gameplayStart()` for size measurement; ads are disabled but the game must run clean with the Ads SDK on or off.
4. Data module: localStorage-like, 1 MB cap, 1 s debounce, must tick the Data Module toggle at submission.
5. Ads (Full Launch): midgame max 1 per 3 min by SDK, first one after tutorial or level 3-4; rewarded must be optional, equal-size skip, no reward on `adError`; banners menu-only.
6. Sitelock: CSP `frame-ancestors 'self' *.crazygames.com https://app.crazygames.com capacitor://app.crazygames.com` or iOS app goes white.
7. CG genre benchmarks: puzzle 21 min, D1 6.2%, conversion 68%; clicker 15 min, D1 6.6%; platform D1 average 6.7%. Puzzle is the biggest earner category.
8. Poki: application form, human review, closed beta. Player fit test (500 players, 3+ min, 25%+ over 3 min), web fit test (~7 d), soft release 2-3 wks, release 2-3 months after green light.
9. Poki targets: 65%+ conversion, 5+ min playtime. Deal: web exclusive default 5 years with rev share (50/50 on Poki traffic, 100% on your own), or flat one-time license with no share.
10. Poki thumbnail: 1:1 min 628x628, no text, avoid #83FFE7; `commercialBreak/rewardedBreak`, no IAP, no external requests, bundle everything.
11. Trends: idle/clicker/tycoon/merge/sim are crowded on /new; a themed twist on a one-verb loop with offline-earnings rewarded hooks fits both portals. Poki declines derivative games.
12. Second listings: GameMonetize 45% share, Y8 50% (non-exclusive, $100 PayPal min), itch.io (free, donations only), YouTube Playables (early access form), Telegram (Stars). Poki exclusivity blocks all of them, so Poki goes last.
13. Gaps: GameDistribution and Newgrounds terms not verified; no developer interviews or revenue figures found.
14. Checklist in section 5.
15. Sources at the bottom.


## 1. CrazyGames docs (beyond the basics)

### Quality (https://docs.crazygames.com/requirements/quality/)
- Onboarding: land new users straight in gameplay, teach inside play, skippable, visuals over text, show controls with a keyboard overlay or mouse gesture, label buttons clearly. Do not size buttons or delay them to push ads.
- Clear reachable goals, easy to learn, consistent controls, quick response to input, balanced pace, avoid repetitive tasks.
- If solo and multiplayer both exist, solo must be as prominent.
- Unique: make it easy to add levels/art later; do not change genre after submission; update often; avoid names/iconography confusable with other games; no generic names unless you own the IP ("Super Chess" ok, "Chess" not).
- Aesthetics: high-res consistent graphics, no compression artifacts, consistent audio levels, one art style, name and imagery must match gameplay (no misleading). Change name/imagery only after a major update.
- Restricted keys: adapt bindings to keyboard layout (AZERTY uses ZQSD, not WASD). Avoid keys with browser behaviour: Escape exits fullscreen, Ctrl/Cmd+W closes the tab (can be disabled in fullscreen).

### Game covers (https://docs.crazygames.com/requirements/game-covers/)
- Three covers required: landscape 16:9 1920x1080, portrait 2:3 800x1200, square 1:1 800x800. Same visuals across all three.
- Restrictions: no borders; only the game title as text (no "New", "Updated", "Play", "Play now"); no icons or store logos; no unlicensed art; no blur or pixelation.
- Good cover: not a plain screenshot; main character, big stylised title or an illustration; simple, readable on small screens; title on it; font that fits the style (no default Times New Roman). Study genre leaders and Steam/Epic. Refresh occasionally (new content, seasons) but not too often.
- Preview video (shown on hover): 15-20 s max (longer is cut at 20), 50 MB max, two mandatory versions: landscape 1080p 16:9 and portrait 1080p 2:3. No sound. No black screens/logo transitions, no black bars, no default mouse cursor, no "Play Now" text, no app/social icons. Do not fast-forward (platform speeds it slightly). Open with the static cover frame for a seamless transition. Show the most exciting moments (late levels, rare cosmetics, progression). Animated allowed if it represents gameplay.

### Technical (https://docs.crazygames.com/requirements/technical/)
- Total 250 MB max, 1,500 files max. Initial download 50 MB max, 20 MB for the mobile homepage. With SDK, initial size is measured up to the first `gameplayStart`; without SDK, total size is used. Externally loaded files: QA checks time to gameplay, 20 s or less.
- Relative paths only in the bundle.
- Must work on Chrome and Edge; poor Safari = disabled on Safari; disabled on Chromium OS if not smooth on 4 GB RAM.
- If mobile supported: must support mouse, keyboard and touch. Desktop landscape; vertical allowed with side bars. Set orientations in the submission form (site prompts rotation, no orientation lock code needed).
- Add `user-select: none` (and -webkit/-moz/-ms variants) on body to stop magnifier/selection menus.
- Unity disabled on iOS by default (memory crashes).
- iOS audio: AudioContext goes "interrupted" when backgrounded; call `resume()` inside a user gesture (touchend/click) when state is suspended; a visibilitychange listener is not enough. Howler and PlayCanvas flagged.
- SDK: Basic needs only `gameplayStart` (ads disabled even if integrated). Full: gameplayStart/Stop, Data module, User module; load start/stop optional.
- Sitelock: whitelist every crazygames.com origin plus iOS and Android app origins.
- If you collect personal data beyond SDK events, show a simple privacy notice (not a blocking pop-up).

### Ads requirements (https://docs.crazygames.com/requirements/ads/)
- Basic Launch: ads disabled, no revenue. If Ads SDK integrated, game must still run fine with ads off (no freezes, no dead rewarded buttons) or it is rejected.
- Only SDK ads. Types: midgame video, rewarded video (fallback banners), in-game banners.
- No ads in active play, no surprise, no chained ads, none before reasonable gameplay.
- Midgame: not on menu/settings/shop navigation buttons; pause game and block UI until `adFinished` or `adError`; handle `adError` and continue; mute only when the ad actually plays. SDK caps midroll at 1 per 3 minutes; early requests are ignored.
- Rewarded: occasional, never required to finish levels; hide button or show timer when unavailable; no chaining; never on an active gameplay screen; skip option must match the ad button in size/font/colour; skip not hidden or delayed; video icon; offer an alternative (coins); show clear reward on `adFinished`; NO reward on `adError`. Between two levels: midgame ad with restart OR rewarded to continue, not both.
- Banners: only on screens open 5 s+ on average, never block UI (also mobile), not in gameplay, max 2 per screen, may cost performance.
- Never block or punish adblock users; disable features with a notice; no popups.

### Getting to the first frame (https://docs.crazygames.com/resources/getting-to-the-first-frame/)
- Under 100 ms instant, 1 s fine, 10 s attention drifts. Measured up to `gameplayStart`. Platform has 50M+ monthly players.
- Load tutorial-critical assets first, start play when tutorial is playable, keep streaming during tutorial, loading screen only if still not done.
- Unity: Addressables, Brotli, ASTC, mono Vorbis, IL2CPP, light Awake/Start. Godot: external .pck, Brotli on wasm/js/pck (Content-Encoding: br), custom export template, lightweight _ready. (Less relevant for plain JS/canvas games, where the rules are: small bundle, lazy-load non-critical assets.)
- Perf bottlenecks: CPU-heavy JS/WASM, transparency overdraw, physics, GC allocations, audio latency.

### Ad monetization guide (https://docs.crazygames.com/resources/ad-monetization-guide/)
- Metric: revenue per 1000 plays. Conversion (plays 1+ min) drives impressions per play; playtime and impressions linked.
- Rewarded = highest eCPM; midgame = baseline revenue, request at every natural break (SDK paces it); banners = lowest eCPM, menus/shops/level-select only, keep buttons away from banners.
- Genre tips: Idle/merge: time skips, offline earnings multipliers. Puzzle: hints, extra moves; midgame between levels only if levels are long enough. Action: revives, power-ups. Word: fewer ads, strong via retention.
- Mobile landscape banner can eat 10-15% of screen; mobile sessions shorter, consider earlier first midgame and "watch to revive". Desktop: longer sessions, lean on deep-economy rewarded + midgame.

### Rewarded ads deep dive (https://docs.crazygames.com/resources/rewarded-ads-deep-dive/)
- Value exchange: urgency (revive, once per session), convenience (skip 1 h wait, instant finish), exclusivity (skins, daily chest).
- Scaling: reward = % of next upgrade cost or a few minutes of play; daily caps on premium currency (example 5/day); diminishing returns (100, 50, 25 gems); test smaller rewards (50 vs 100 coins) and keep if watch rate holds.
- High-converting spots: game over ("Watch to revive", "Double your coins"), shop free daily chest, main menu daily ad button that lights up, insufficient funds prompt (watch for missing 50 coins).
- UI: exact reward in button text ("+50 Gems"), video icon, test button position.
- Genres: puzzle "generally the best overall performers"; action and clicker show frequent rewarded ads.

### Midgame ads pacing (https://docs.crazygames.com/resources/midgame-ads-pacing/)
- Midgame often 40-60% of casual game earnings. SDK: max 1 per 3 min plus safeguards near game start and rewarded ads. No need for own cooldowns; request at every natural break.
- Best: between levels/rounds, after boss/milestone, rest screens (stage-clear summary), not as next level loads.
- Protect D1: first midgame after tutorial or 3-5 min of play, or after level 3 or 4. Track ads per active user, retention at the level of first ad, quits right after an ad. If retention drops, move the placement, do not cut request frequency.

### Genre monetization pages
**Puzzle** (https://docs.crazygames.com/resources/monetizing-puzzle/): puzzle is the largest category in the top 100 by earnings; avg playtime 21 min (32% above platform), D1 6.2%, conversion 68%, 8.9 impressions per play (4.2 rewarded, 4 midgame). Banners on level-complete/level-select/menu only, 320x50 mobile, 728x90 desktop, 15-20 px gap from buttons. Rewarded: hint (1-minute cooldown, video icon on HUD), 5 extra moves or undo when one step from losing, level skip (no coins/stars for skipped), exclusive daily puzzle. Midgame only between levels, even for 30 s levels. Track hints per session and level churn (put "watch to skip" on high-churn levels).
**Clicker** (https://docs.crazygames.com/resources/monetizing-clicker/): avg ~15 min playtime, D1 6.6%, top clickers 5.5 impressions per play, half rewarded. Best rewarded: welcome-back offline earnings x2/x3 (one of the highest-converting idle placements) and auto-clicker boost (e.g. 2x click damage for 10 min). Banners on upgrade tree, shop, stats. No natural level breaks: use shop open, milestone, leaving upgrade screen; never ad while tapping; show a 3-5 s "Ad starting in 3..." warning.
**Midcore/idle** (https://docs.crazygames.com/resources/monetizing-midcore-idle/): platform D1 average 6.7%. Strategy ~17 min, D1 7.5%, ~21 impressions per play (14 rewarded). Adventure ~17 min, D1 7.4%. Simulation ~14 min, D1 7.4%, 7.9 impressions per play. Cap free premium currency from ads (e.g. 5/day), scale rewards to level/upgrade cost, free gacha pull or chest once every few hours, ad to refill energy; forced midgame very sparingly (after quests only); prefer rewarded + menu banners; avoid inflation.

### HTML5 common fixes (https://docs.crazygames.com/resources/html5/common-fixes/)
- preventDefault on `wheel` (passive:false) to stop page scroll; on `keydown` for arrows and space; `contextmenu` preventDefault on document; Samsung app webview needs a visibilitychange hook (Unity-specific `publishEvent`).

### Sitelock (https://docs.crazygames.com/resources/html5/sitelock/)
- JS: allow only hostname `crazygames.com` or `*.crazygames.com`; else show "Available only on CrazyGames" or blank.
- iframe/CSP: `Content-Security-Policy: frame-ancestors 'self' *.crazygames.com https://app.crazygames.com capacitor://app.crazygames.com;` Wildcard host alone blocks the iOS app origin (white screen). Every ancestor is checked, so `games.crazygames.com` (video ads) must be allowed too. If sitelock reads referrer/ancestorOrigins, compare host only, do not require https.

### SDK intro (https://docs.crazygames.com/sdk/intro/)
- Modules: ad, banner, game, user, data (+ IAP). HTML5: add `<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js">` in head before game code, then `await window.CrazyGames.SDK.init()` (v3 needs manual init). Promise-based. Errors have `code` and `message`.
- Environments: `local` on localhost/127.0.0.1 (ads shown as overlay text, console logging), `crazygames` on their domains, `disabled` elsewhere (calls throw: check `window.CrazyGames.SDK.environment` first). Force local with `?useLocalSdk=true`.
- Unity builds must be Brotli/Gzip compressed. Construct: disable Worker mode. Most realistic QA: the Preview tool at crazygames.com/preview via https://developer.crazygames.com/.

### SDK game module (https://docs.crazygames.com/sdk/game/)
- `gameplayStart()` on start, resume, revive, next level; `gameplayStop()` on every break (menu, level end, pause); not on focus loss (platform handles it).
- `loadingStart()` / `loadingStop()` around loading.
- `happytime()` celebration: only for real achievements (boss, high score), never for level complete or pickups, sparingly.
- `reportGameCompletedPercentage(0..100)` HTML5 only; progress should move forward; 100 only at a meaningful end; endless games define a consistent point; re-report on load after adding content.
- `setGameContext({...})` at level start, `clearGameContext()` on exit; attaches state to player feedback.
- `game.settings.muteAudio` / `disableChat`: SDK mute takes priority over your in-game audio toggle. Test with `?muteAudio=true`.

### SDK data module (https://docs.crazygames.com/sdk/data/)
- localStorage-like: `getItem/setItem/removeItem/clear`, string values. Limit 1,048,576 bytes (1 MB) as JSON; saves debounced 1 s (up to 30 s in some cases); over 1 MB means no backup and error `dataLimitExcedeed`; `dataModuleDisabled` if the submission toggle "Yes, using the Data Module" was not selected.
- Rely fully on it for guests and logged-in users. Init preloads all saved data (do it on the loading screen). Logged-in data syncs across devices; guests use localStorage and it moves to the account on sign-in if the account is empty. Read before write. For an already-published game, migrate old localStorage keys.

### FAQ (https://docs.crazygames.com/faq/)
- Pipeline: A initial QA (fails for bugs, no English, clones, inappropriate content, PEGI-12, kid-aimed content), B Basic Launch (soft launch, collects retention/playtime/CTR/conversion), C Full Launch (second QA, wide release).
- Updates usually live the same working day; Basic Launch updates instant. Resubmit a rejected game after meaningful improvements. Result by email.
- Already live elsewhere is fine if you hold the rights; they will not iframe a game from a competing portal; your own domain is fine but hosting on CG is recommended; external games earn only with SDK. You keep ownership.
- Earning needs: no other portal branding, SDK, no external ads, original. Ad provider is theirs only. Payout monthly at EUR 100, wire or PayPal (the FAQ names PayPal, you noted Tipalti). Amount not stated.
- Ranking inputs: device, country, OS, play count, playtime, retention, conversion, feedback; new games may get an initial boost. Chrome and Edge required; Safari and Firefox recommended. No multiplayer servers provided. Chat needs profanity filter + moderation. Audience: strongest in US/UK/English markets; teens .io, older players puzzles.

## 2. Poki for Developers (2026)

Entry: https://developers.poki.com (guide at /guide). Closed beta / limited access per the official page; apply via https://developers.poki.com/guide/share.
- Submission form (/guide/share): name, email, studio; team size and location; prior releases; title and short pitch; engine; browser build with no login (or a gameplay video if none); 3 gameplay screenshots (static PNG/JPEG/WebP, 5 MiB max each); why Poki players would like it; already-released-elsewhere; accept the Content & Brand Guidelines. A human team reviews; no reply is a normal outcome.
- What they look for (/guide/what-we-look-for): quality (UX, feel, core loop), player fit, tech (fast load, stable fps, lean files). Extra signals: originality (clones of hits not promoted), depth and replayability, first impression (clear thumbnail, playable opening), cross-device feel (audience is "majority mobile", desktop-only is at a disadvantage), room to grow (roadmap at submission). No genre list or numeric thresholds.
- Testing (/guide/how-testing-works): player fit test: 500 players, ~5 hours, up to 2 per day, healthy = 3+ min average playtime and 25%+ of plays over 3 min (needs a thumbnail). Web fit test: game on real category pages, CTR/time/conversion vs category averages, ~7 days. Targets before asking for review: 65%+ conversion to play, 5+ min average playtime (10+ for management/sim). Poki average: ~70% conversion, 6+ min. Final review decision 1-2 weeks; release after green light roughly 2-3 months.
- Release (/guide/release-process): soft release slot 1-2 weeks to schedule, soft release itself 2-3 weeks (cannot be skipped); soft to global 2-3 weeks; new-game push about 2 weeks. Target at least 1 ad per daily active user with healthy midroll/rewarded mix. Animated thumbnail added during soft release, required before global.
- Deals (https://developers.poki.com/guide/revenue-deal-types): web exclusive preferred (only on Poki across open web, Discord and YouTube Playables; Steam, mobile stores, consoles excluded), default term 5 years, includes revenue share on Poki-brought players. Non-exclusive = one-time flat license fee, no revenue share (amounts not public, "set out in your agreement"). Official monetization page (via search): traffic you bring yourself keeps 100%, traffic from Poki.com 50/50. Payouts wire or PayPal (third-party).
- Requirements (https://developers.poki.com/guide/requirements-quality): 16:9 scaling to cover canvas (640x360, 836x470, 1031x580 reference); mobile fullscreen portrait/landscape; support desktop, mobile, tablet; leave if load over 10 s; `gameplayStart()` on first input (not on load), `gameplayStop()` on any interruption, never twice in a row, no SDK events during ads; `commercialBreak()` only when returning from pause; `rewardedBreak()`; mute during ads; no internal ad timers; one video per reward; standard continue button equal or larger and next to/above reward button; rewarded buttons not green with a video icon; no reward when adblock detected; no IAP, no third-party ads. External links via `PokiSDK.openExternalLink(url)`. Bundle everything (external requests blocked), no splash/branding (studio logo on loading screen ok), clean build, skippable cutscenes, ESC/space pause with SDK events, no parent-page scroll, save system or a notice, wrap localStorage in try/catch (incognito), profanity filter for usernames, hosted privacy policy URL (not a Google Doc) if linking out, multi-language recommended for text-heavy games. Third-party guides say initial download under 8 MB (unverified, check the Inspector).
- Thumbnail (/guide/game-thumbnail): static 1:1, min 628x628, full-bleed, no borders, no text, one clear foreground subject (main character), keep away from the background colour #83FFE7, test at small size. Animated hover preview needed before global release.
- Tool: Poki Inspector, free, checks a build against requirements. Other guide sections: Netlib, AUDS (user data store), User Accounts, playtesting, localization, engagement.

## 3. What performs (2025-2026)

Evidence is thin: neither portal publishes genre rankings, and WebSearch found no developer interviews or postmortems. What is solid:
- CrazyGames' own genre data (docs pages above): puzzle is the largest category in the top 100 by earnings (21 min average playtime, 6.2% D1, 68% conversion, 8.9 ad impressions per play). Clicker ~15 min, 6.6% D1. Strategy/adventure/sim 14-17 min, 7.4-7.5% D1. Platform D1 average 6.7%. Docs call puzzle "generally the best overall performers" for monetization and word games strong via retention.
- CrazyGames audience: strongest in US/UK/English markets; teens lean .io, older players lean puzzles (FAQ).
- Third-party (unverified, one Indonesian article, https://www.industry.co.id/read/150924/5-rekomendasi-game-seru-di-crazy-games-buat-nemenin-weekend-kamu): CrazyGames 93M visits in April 2026, ~30 min average session; hypercasual 78.8% and puzzle 20.6% of play time.
- Idle category page (https://www.crazygames.com/t/idle, checked 24 Oct 2026): Idle Mining Empire, Tiny Fishing, Idle Breakout, MineClicker, Clicker Heroes, Idle Blogger Simulator, Corn Tycoon, Leek Factory Tycoon, Mage Castle Idle Defense, Lumber Hero. Shared traits: one-verb mechanic, a familiar theme with a twist (Breakout, mining, farming, tycoon), numbers going up, reward loop, runs on low-end hardware, loads fast. Tiny Fishing is called "underrated" by the page itself.
- /new list (https://www.crazygames.com/new, 24 Oct 2026, titles from slugs): heavy on tycoon/simulator (Trash Tycoon, Asteroid Tycoon, Superhero Simulator, Robovac Satisfaction Co, Appraiser), Roblox-style "obby"/brainrot, idle defense, merge (Hero Merge), cozy/dress-up/ASMR (Dream Cake Designer, Makeover Cleaning ASMR, Blogger Dress Up), puzzle (Pixel Jam Bus Puzzle, Spot the Difference, Matching Moments), driving. Reading: tycoon, idle, merge and simulation dominate new releases, so those are crowded; a twist on theme matters.
- Poki (official): web sessions are short and return rate low, so design a ~3 minute loop and about an hour of content, make the first minutes brilliant, celebrate progress (confetti, sounds), start easy and ramp gently, keep gameplay continuous (no waiting), support touch + keyboard (WASD/arrows, space/return). Examples named: Puffy Cat, Stickman Hook (new character at the end of each level), Level Devil. Poki audience is majority mobile. On trends (https://sdk.poki.com/trends): trend-inspired games welcome only if they add something; derivative games and crowded genres can be declined. Poki average: ~70% conversion, 6+ min playtime.
- What top idle/clicker/puzzle share: instantly understood in under 10 s; one core loop; short levels or fast incremental feedback; visible progress and juice; rewarded-ad hooks built in (offline earnings x2/x3, hints, undo, revive); 10+ minute sessions through meta-progression; light assets that load fast and run on weak hardware.
- Gap: no named revenue figures for any title found. A GDevelop write-up (https://gdevelop.io/blog/powerline-guardians-jam-winners-web-success) says CrazyGames' team helped tune performance and mouse/keyboard/touch controls for a jam-winner game before launch (no numbers).

## 4. Other portals (one line each; verify before relying)

- GameDistribution (https://gamedistribution.com): distributes to a network (a 2026 article claims 4,000+ portals, 350M users a month, unverified); SDK required; official terms page did not load, revenue share not confirmed. Results reported as uneven by developers (2021 forum, anecdotal).
- GameMonetize (https://gamemonetize.com/developers): 45% revenue share, SDK ("5 minutes"), branding and links allowed, payment Net 30 within 25 days via PayPal or USDT, exclusivity not stated, no minimum or review time stated.
- Y8 (https://developer.y8.com): 50% of eligible in-game ad revenue (Y8 Managed Partnership, monthly; or AdSense for Platforms paid by Google); non-exclusive, game can be live elsewhere; need to own the rights and be tied to a studio (no company needed); no external links; SDK steps in the portal; payout minimum $100 PayPal or $500 wire; invoice processed in ~10 business days; payees 18+; resubmit cooldowns 0, 6 h, 12 h, 24 h, 2 d, 5 d.
- itch.io (https://itch.io/docs/creators/html5, /payments): zip with index.html, max 1,000 files, 500 MB extracted, 200 MB per file; HTML5 can only take donations (no paid HTML5); default itch cut 10%, adjustable 0-100%; good for a free playable page, press and jams, not for ad revenue.
- Newgrounds (https://www.newgrounds.com): upload page loads 403 to fetch tools; no verified revenue terms found. Treat as audience/feedback channel, check the Newgrounds wiki before relying.
- YouTube Playables (https://developers.google.com/youtube/gaming/playables): early access, interest form only; web APIs, WebGL/Canvas, Phaser/Unity/Godot/three.js; certification requirements and SDK on linked pages; Poki's web-exclusive deal also covers Playables and Discord.
- Telegram Mini Apps (https://core.telegram.org/bots/webapps): publish via @BotFather, no portal review; monetize with Telegram Stars, payment providers, subscriptions; no in-app ad network in the docs.
- Discord Activities: not researched (Poki exclusivity covers Discord).
- Rule of thumb: CrazyGames FAQ allows a game already live elsewhere if you hold the rights; but they will not iframe a game hosted on a competing portal. Poki's web exclusive (5 years default) blocks everything else on web, so Poki goes last or alone; GameMonetize/Y8/itch are non-exclusive and can run in parallel with CrazyGames Basic Launch (check each build has no other portal's branding).

## 5. Launch checklist

Build
- [ ] Initial download under 20 MB (mobile homepage), hard max 50 MB; total under 250 MB, under 1,500 files; relative paths only; loads to playable in under 10 s (target under 5).
- [ ] SDK script `https://sdk.crazygames.com/crazygames-sdk-v3.js` in head; `await SDK.init()` at load; call `gameplayStart()` on first real play; `gameplayStop()` on every break. Even for Basic Launch (needed for the size measurement).
- [ ] Test on localhost (env `local`), force `?useLocalSdk=true` elsewhere; then upload to the Developer Portal preview (https://developer.crazygames.com/, crazygames.com/preview) for realistic QA.
- [ ] Works in Chrome and Edge, decent on Safari/Firefox; mouse + keyboard + touch if mobile; set supported orientations in the form; no custom fullscreen button; no external links; no other portal branding.
- [ ] `user-select: none` on body; preventDefault on wheel, arrows/space, contextmenu; iOS audio resume on touchend/click; handle AZERTY (use `event.code` carefully or offer remap); avoid Escape and Ctrl/Cmd+W as controls.
- [ ] Saves: use SDK Data module (tick "using the Data Module" at submission), under 1 MB, wrapped in try/catch; wrap localStorage for Poki incognito; migrate on later updates.
- [ ] Sitelock (optional) with the exact CSP string above; if sitelock, whitelist all CG origins and app origins.
- [ ] Ads off must still work (Basic Launch). For Full: midgame at every natural break (SDK caps 1 per 3 min), first one after tutorial / 3-5 min / level 3-4; rewarded with clear reward text, video icon, equal-size skip, no reward on `adError`; banners only on menus. Mute only when the ad starts.
- [ ] No privacy-sensitive data collected beyond SDK, or add a simple notice. PEGI 12 content, English text, original name (no generic title like "Chess").
- [ ] Onboarding skippable, inside gameplay, visual not text; controls overlay; goals clear; consistent audio levels; one art style.

Assets
- [ ] Covers: 1920x1080 (16:9), 800x1200 (2:3), 800x800 (1:1), same art, title only, no borders/icons/"Play"/"New" text, readable small, custom font, not a raw screenshot.
- [ ] Preview video: 15-20 s, under 50 MB, two files (1080p 16:9 and 1080p 2:3), no sound, no cursor, no black bars, no promo text, starts on the cover frame, real footage not sped up.
- [ ] Poki later: 1:1 thumbnail min 628x628 no text, avoid #83FFE7, animated thumb before global release, 3 gameplay screenshots (5 MiB each) for the form.
- [ ] Description, controls text, tags/genre chosen after studying the category page; title that is distinct and matches gameplay; do not change genre after submission.

Metrics to hit before promotion
- [ ] Conversion (1+ min) top 80%+ (Poki wants 65%+, average 70%), average playtime 10+ min target (Poki 5+), D1 10-15% (platform average 6.7%), 500 plays in the first 7 days.
- [ ] Test the first 60 seconds with a stranger; remove any dead time; 3 minute loop.

After
- [ ] Watch Developer Portal stats and feedback (negative raters are asked why); update covers occasionally; ship content updates (updates go live same working day; Basic Launch instantly); report completion percentage; consider Full Launch SDK (ads) once promoted.
- [ ] Poki: apply only after CG data exists (conversion and playtime numbers help the pitch); weigh the 5-year web exclusivity before accepting.

## Sources
CrazyGames: https://docs.crazygames.com/requirements/quality/ , /requirements/game-covers/ , /requirements/technical/ , /requirements/ads/ , /resources/getting-to-the-first-frame/ , /resources/ad-monetization-guide/ , /resources/rewarded-ads-deep-dive/ , /resources/midgame-ads-pacing/ , /resources/monetizing-puzzle/ , /resources/monetizing-clicker/ , /resources/monetizing-midcore-idle/ , /resources/html5/common-fixes/ , /resources/html5/sitelock/ , /sdk/intro/ , /sdk/game/ , /sdk/data/ , /faq/ ; https://www.crazygames.com/t/idle ; https://www.crazygames.com/new
Poki: https://developers.poki.com , /guide , /guide/share , /guide/what-we-look-for , /guide/how-testing-works , /guide/release-process , /guide/revenue-deal-types , /guide/requirements-quality , /guide/game-thumbnail , /guide/engagement ; https://sdk.poki.com/trends ; https://app.cinevva.com/guides/publish-game-poki (third-party, promotional)
Portals: https://gamemonetize.com/developers ; https://developer.y8.com ; https://itch.io/docs/creators/html5 ; https://itch.io/docs/creators/payments ; https://developers.google.com/youtube/gaming/playables ; https://core.telegram.org/bots/webapps ; https://gdevelop.io/blog/powerline-guardians-jam-winners-web-success
Gaps: GameDistribution and Newgrounds terms unverified; Poki revenue percentages only via search summary of official page; no CG/Poki developer interview or postmortem found; Poki animated thumbnail spec not read (/guide/your-game-page).
