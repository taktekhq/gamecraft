# Design for conversion, session length and retention (CrazyGames web games)

Written 24 Oct 2026 for the skill "designing casual games that hold players". Evidence tags: [DOC] read from a source this session, [MEM] from general industry knowledge, not re-verified here, treat as a heuristic.

## Summary (15 lines)

1. CrazyGames Basic Launch KPIs [DOC]: conversion = share who play 1+ minute (target 80%+, load under 10 s, build under 20 MB), avg session 10+ min, D1 retention 10-15%. Benchmarked against other platform games.
2. Each KPI has one lever: conversion = load + first screen; session = core loop, goal clarity, pacing; D1 = progression, daily hooks, saved progress.
3. The first minute is won or lost before gameplay: build size, first frame, zero menus, one obvious goal, controls shown by doing.
4. Land in play. Menu is a pause screen, not a gate. Skippable, wordless onboarding built into the first level.
5. Session length comes from a short core loop (5-30 s) nested in a medium loop (1-3 min) nested in a meta loop (unlocks over days).
6. Always have 2-3 goals within reach at once (an unfinished bar, a next unlock, a daily task). Goal gradient: show progress, start bars partly filled.
7. Variable reward is fine when fair: random drops with honest odds and pity timers, no rigging, no pay-to-spin.
8. D1 on a portal with no push: autosave from second one, offline progress, a visible "come back for" (daily reward, timed event, unfinished chain), collection and bests.
9. Idle maths: cost = base * r^owned, r between 1.07 and 1.15; next tier costs ~10-15x and produces ~5-8x per unit; prestige currency ~ sqrt or cbrt of lifetime earnings.
10. Offline earnings: cap at 2-8 h, show a "welcome back" screen, optionally double via rewarded ad.
11. Puzzle/arcade: ramp difficulty in waves (easy, easy, hard, rest), keep near-misses honest, add run variety (modifiers, seeds, upgrades).
12. Ads [DOC]: midgame only at natural breaks (SDK paces max 1 per 3 min), rewarded as a player choice at the moment of need, one revive offer per session, banners only on menus.
13. Poor ad timing hurts retention, which cuts revenue. Treat ads as a design surface, not a bolt-on.
14. Instrument the funnel: load, first input, 30 s, 60 s, first death, first unlock, session end. CrazyGames points to ByteBrew for drop-off tracking.
15. Checklist in section 7 is the gate before build.

## 1. First-time user experience

Platform guidance [DOC]: put new users straight into a simple onboarding phase, teach inside gameplay, cover core functionality only, make it skippable, prioritise visuals over text, show controls with a keyboard overlay or mouse gesture. Buttons must be clearly labelled, not sized to bait ad clicks, no delay timers on buttons.

What kills conversion (order of damage):
- Loading. Target under 10 s and under 20 MB [DOC]. Load the first level first, stream the rest. A third-party figure says up to 25% quit after a bad first experience such as slow load or a crash [secondary, web search snippet].
- Menus before play. Title, settings, "choose mode" and login walls cost players who came to try, not to configure. Default to mode 1 and start.
- Text tutorials. Players skip walls of text. One verb per screen, shown not told.
- Unclear goal. If a new player cannot say "I am trying to ___" after 10 s, they leave.
- Ads or sign-in before the first play.
- Input confusion: wrong key hints on touch devices, no focus on the canvas (first click needed), audio autoplay blocked and silent.

Timeline to design against [MEM, consistent with the 80% at 1 minute bar]:
- 0-3 s: first frame appears, game already moving or one big "tap to start" that is itself the first input. Sound on first input.
- 3-10 s: the first successful action. The player does the core verb once and gets feedback (sound, particles, number pop). No text beyond 3-5 words.
- 10-30 s: first small win and first small fail, both cheap. Fail restarts instantly (under 1 s).
- 30-60 s: reveal the second layer: first upgrade, first combo, first obstacle type, or first unlock bar nearly full. This is the "I want to see what is next" moment and is what keeps the 80% past the minute mark.
- 60 s+: first meaningful choice (pick one of 3 upgrades, spend currency on one of 2 things). Choices create ownership.

Teaching without text: constrain the first level so only the right action is possible (a single gap, a single button), use a ghost hand or arrow that disappears after the first success, let the environment show the goal (a flag, a full bar, a glowing target), and use affordances players know (swipe, drag, tap targets). Introduce one mechanic at a time, each in a safe spot where failure is impossible, then test it, then combine.

Loading and delivery tips: compress textures, use audio sprites, lazy-load anything not in level 1, show a progress bar only if it exceeds 2 s.

## 2. Session length: core loop, meta loop, hooks

Three nested loops:
- Core loop (5-30 s): act, feedback, reward. Must be satisfying alone (game feel: input response under 100 ms, squash, sound, number pops).
- Session loop (1-3 min per round or level): goal, risk, result screen, upgrade or unlock, next round. The result screen is where "one more go" lives: show what you almost got and what the next unlock costs.
- Meta loop (days): permanent upgrades, collection, characters, map regions, prestige.

Pacing unlocks: the first unlock should arrive within 60-90 s, the second within 3-4 min, then stretch (roughly a 1.5-2x gap each time) so every session of 10+ minutes contains 2-4 unlocks. Reveal future unlocks greyed out (a visible roadmap beats a surprise).

"One more go" hooks:
- Instant restart (no menu, no ad on the first retry).
- Near-goal bars: "2 more kills to level 5" at death. The goal gradient effect says effort rises as the goal nears; start progress bars at 10-20% (endowed progress) and show them often.
- Unfinished chains: a combo, a streak, a half-built item, a partly filled collection page.
- Short rounds with a fresh variable each time (new seed, modifier, enemy mix).
- Session goals that are bigger than one round: "reach 500 m across runs", "collect 3 gems today".
- Soft stopping cues: avoid hard ends. End a round at a high, with a tease of the next.

Variable rewards, ethically: randomise what, not whether. Fair rules: publish drop odds in game, add a pity timer (guaranteed rare after N misses), never adjust difficulty or odds secretly to push spending or ad views, no fake near-misses. Keep the average reward predictable, let the spread give the excitement. No timers designed to shame, no loss-aversion threats on streaks (let a missed day pause, not wipe).

Reward cadence: tiny reward every 2-5 s (coin, score tick), small every 20-30 s (level, combo), medium every 2-3 min (unlock), large every 10 min (new area, boss, prestige).

## 3. D1 retention without push notifications

The platform asks for [DOC]: meaningful progression, daily hooks (login bonus, daily quests), saved progress, polish. For a no-push portal the reason to return must be remembered by the player or visible on the portal return.

- Save from the first second. Autosave on every meaningful change (localStorage fallback plus the portal's save data module so progress follows the account). A returning player who finds nothing is a lost D1. Check the CrazyGames SDK data module docs before build.
- Offline progress: idle and builder games grow while away, shown as a "welcome back" screen with the amount. Pull factor: the player pictures the pile of coins waiting.
- Daily reward: 7-day cycle with a final bigger prize. A missed day should not reset to zero (forgive: drop back one step or keep a "grace day"). Day 1 gift should be useful immediately but not a full reward, to leave something to want.
- Unfinished goals: end session 1 with 2-3 open goals (a bar at 80%, a locked item at a near cost, a daily quest).
- Collection: characters, skins, trophies, a codex that records discoveries. Show empty slots.
- Leaderboards and bests: personal best first (always on), then daily and weekly boards, ghost or name of the next rival to beat ("beat Alex by 120"). Portal leaderboards are weaker than in-game ones unless the SDK offers them, so show personal best strongly.
- Timed events or daily seeded challenge: same level for everyone today (Wordle effect), shareable result.
- Return trigger copy: on exit/pause screens, state when the next reward is ready ("daily chest in 6 h").
- D1 measurement rule: D1 shows a day later in the dashboard [DOC], so ship with events logged on your side too.

What works on portals specifically [MEM, heuristic]: players browse "next game" tiles, so D1 return mostly comes from the game being easy to find again (name recall, portal "recently played" lists, favourites). Ask the player to favourite or bookmark after a win, not at the start. Never cross-promote other games or platforms inside the game [DOC].

## 4. Idle and incremental maths

Sources: Anthony Pecorella, "The Math of Idle Games", Kongregate Developer Blog, parts I-III (republished on Game Developer). Summarised in my own words.

### 4.1 Part I: generators and cost growth
- Each generator has base cost b, base production p and count owned k. Next purchase costs b * r^k, where r is the growth rate. Production is p * k * multipliers. Adventure Capitalist's Lemonade Stand uses r = 1.07; across the game's generators r sits in the 1.07 to 1.15 range, and Cookie Clicker uses 1.15 [rates other than 1.07: MEM].
- Why exponential cost: production grows linearly (or polynomially) with count, so cost must grow faster for the game to slow down and keep decisions meaningful.
- Cost of buying n at once: b * r^k * (r^n - 1) / (r - 1). Max affordable with currency c: floor(log_r(c * (r - 1) / (b * r^k) + 1)). Use these for "buy x10 / x100 / max" buttons without loops.
- Payback time of the next unit = cost_next / p. It rises by factor r per unit, so it doubles every ln2/ln r units: about 10 units at 1.07, about 5 at 1.15. Use that to choose r: low r (1.07) for the cheap early generator that players mass-buy, high r (1.12-1.15) for later ones so they self-limit.
- Tier ratios [AdCap-style, MEM]: each next generator costs about 10-15x the one before and produces about 5-9x more per unit, so higher tiers are worse per coin early but better late. A buy-decision metric players use is income per cost; keep it from making the newest tier always best by varying multiplier milestones per generator.
- Multiplier milestones: x2 at counts like 25, 50, 100 (AdCap's stand doubles at 25 and 50) [DOC]. They create bursts of purchasing and visible goals ("12 more to double").
- Pecorella's caution: per-second income models over-favour slow high-tier generators, so test with a spreadsheet and real player play.

### 4.2 Part II: derivative-based growth and relevancy
- Alternative to pure exponential: tier N produces tier N-1 (a chain). With four tiers, output follows x^n / n!, which is polynomial early and approaches e^x (exponential) as tiers are added. Growth stays sub-exponential while costs still rise exponentially, so costs eventually win. Example cost 5 * 1.1^n [DOC, Derivative Clicker].
- Keep earlier generators relevant: a bonus per purchased unit that boosts the whole tier, such as +0.05% production per purchased Tier 1 unit, so buying low tiers stays worth it [DOC]. Cost depends on number purchased, not number owned (including produced units).
- Two currencies that depend on each other's production make players balance, not just buy the last tier.

### 4.3 Part III: prestige
Let L = lifetime earnings, M = max earnings in one run, R = earnings this run. Formulas [DOC]:
- Realm Grinder (on M): p = (sqrt(1 + 8M / 1e12) - 1) / 2. Needs about 4x earnings to double p. Resetting at the same point gives nothing extra.
- Adventure Capitalist (on L): p = 150 * sqrt(L / 1e15). About 3-4x to double.
- Cookie Clicker (on L): p = cbrt(L / 1e12). About 8x to double.
- Egg, Inc. (on R, this run): gain = (R / 1e6)^0.14. About 128x to double, so a flat curve that rewards active runs and does not depend on idle time. Its offline gain is limited to 2 hours [DOC].
- Rule of thumb [MEM]: each prestige point gives +1% or +2% to all production, so growth feels like multiplicative steps. Offer the first prestige 30-60 min of play in, and make each next one possible at 2-4x the earlier run length, with a clear "you would gain N" readout.
- Check multiplier thresholds: a large multiplier (x16 at 500 units in the Pecorella sheet) can cut a planned long run short, so model the bursts [DOC].
- Light model only: Pecorella warns the spreadsheet is for rough feel, not a simulator [DOC].

### 4.4 Offline earnings
- Cap offline accrual at 2-8 h (Egg, Inc. uses 2 h [DOC]); credit at 50-100% of the active rate. Longer caps reduce the pull to return and flatten D1.
- Welcome-back screen with the sum and a rewarded-ad "x2" button (player choice).
- Compute with elapsed time from saved timestamp, clamp negatives (clock tampering) and clamp to cap. Store a version in the save for later rebalancing.

### 4.5 Number formatting and engine hygiene
- Exceeding float range: use a big-number library (break_infinity.js, decimal.js, or BigInt with a mantissa and exponent) when numbers exceed 1e15 [MEM].
- Show 3 significant digits and a suffix: 1.23K, 4.56M, 7.89B, then T, Qa, Qi or aa, ab; switch to scientific (1.23e45) past a configured limit. Show the rate per second next to the total. Round down costs, round to the player's favour on rewards.
- Fix a tick: use delta time, never a fixed counter per frame, so tab throttling does not slow the economy.

## 5. Puzzle and casual arcade

- Difficulty curve in waves: new idea, easy, easy, harder, rest, new idea (sawtooth rising). First 5 levels should be nearly unlosable; first real fail around level 6-10 [MEM].
- Level pacing: puzzle levels must be long enough to justify an ad break [DOC], ideally 30-90 s each.
- Near-miss: honest near-misses (you missed by a pixel) motivate retry; do not fake them. Show the closest point on the result screen.
- Run-based variety: seeded levels, random modifiers, choose-1-of-3 upgrades, enemy mixes, daily seeds. Roguelite loops (Vampire Survivors style) keep runs at 10-30 min with a meta shop for permanent upgrades.
- Merge, sort and block puzzles: infinite or endless modes with escalating score give session length with no level authoring.
- .io and shooters: death screen with kill count, rank movement and "play again" under one second; platform advises ads at the death or respawn screen after a moment to breathe [DOC].
- What portal hits tend to share [MEM, heuristic, not checked against live rankings]: a single-line pitch, a core loop readable in 5 s, a visible progress meter, soft failure, a long tail of unlocks, and mobile-friendly one-hand controls. Genres that stay on top: idle/tycoon, io games, physics/drift/driving, merge and block puzzle, and shooters. Verify against the current CrazyGames top lists before copying.
- Difficulty adapts without telling: lightly ease after 3 straight fails (extra time, fewer enemies) and never advertise it; do not tie it to payment or ad views.

## 6. Ads that do not hurt retention

From the CrazyGames ad guide [DOC]:
- Midgame ads only at natural breaks: between levels, after death, on the summary screen. The SDK paces them, max 1 every 3 minutes. Never during active play.
- Rewarded ads are opt-in. Put the offer at the moment of need: revive on game over, "double coins" at level end. One revive offer per session. Make the reward meaningful, not too generous or too weak.
- Banners on menus, shop, lobby, level select only; keep buttons and joysticks away from them.
- Desktop sessions run longer, so lean on rewarded and midgame at breaks; on mobile the first midgame may need to come earlier.
- Poor timing lowers retention, which lowers revenue [DOC].

Design rules that follow:
- No ad before the first win and no ad before the second run starts.
- Game logic calls gameplayStart/Stop correctly so the portal can time ads [MEM, verify in the SDK docs].
- Rewarded value must be useful but not required to progress; never gate a level behind an ad.
- Offer rewarded ads in the context of progress (offline x2, revive near a goal, extra spin of the same fair odds) and display the reward before the click.
- Measure per-session ad count against session length and D1; drop the frequency if D1 falls.

## 7. Design checklist before build (apply to a game design doc)

Pass each item or write a reason. Fail any of the first block and do not start building.

A. Conversion (first minute)
1. One-sentence pitch and one visible goal readable in 5 s.
2. Build under 20 MB, first level loads under 10 s, rest streamed.
3. No menu, login, ad or text wall before the first input; start is one tap.
4. First verb achieved within 10 s; a win within 30 s; a second layer revealed by 60 s.
5. Onboarding is inside level 1, wordless, skippable; controls shown by overlay for keyboard and touch.
6. Retry costs under 1 s.

B. Session length (10+ min)
7. Core loop (5-30 s), round loop (1-3 min), meta loop (days) each written down in one line.
8. At least 2 goals in reach at all times; progress bars everywhere; first unlock within 90 s.
9. 2-4 unlocks inside a 10-minute session, gaps growing 1.5-2x.
10. Reward cadence table (tiny, small, medium, large) filled in.
11. Variable rewards use disclosed odds and pity timers; no hidden difficulty or odds tuning tied to money or ads.
12. Result screen shows the near-miss and the next unlock.

C. Retention (D1 10-15%)
13. Autosave from second one, plus portal save data; load tested.
14. Reason to return stated: offline progress, daily reward with grace, daily quest, unfinished chain, collection slots, personal best.
15. Exit/pause screen tells when the next reward is ready.
16. No streak that wipes on a missed day; no shame copy.

D. Economy (if idle or upgrade-driven)
17. Cost = base * r^owned with r in 1.07-1.15; tier cost ratio about 10-15x; per-unit production ratio about 5-9x.
18. Payback times charted per tier, first purchase under 10 s, first tier up under 2 min.
19. Milestone multipliers (25, 50, 100...) listed; prestige formula chosen (sqrt or cbrt of lifetime earnings) with first prestige at 30-60 min.
20. Offline cap 2-8 h; big-number library; formatting rule (3 significant digits plus suffix).

E. Difficulty (puzzle and arcade)
21. Sawtooth difficulty plan; levels 1-5 near-unlosable; run variety source (seed, modifier, upgrade pick).
22. Levels long enough (30-90 s) to justify an ad break.

F. Ads and compliance
23. Midgame ads only at death, level end, summary; rewarded as a choice at point of need; one revive offer per session; banners only on menus.
24. No fullscreen custom button, no cross-promotion, no button delays or oversized ad-bait buttons [DOC].

G. Measurement
25. Events logged: loaded, first input, 30 s, 60 s, first fail, first unlock, session end, D1 return. Compare against the targets: 80% reach 1 min, 10+ min average, D1 10-15% [DOC].

## Sources

- CrazyGames, Basic Launch metrics: https://docs.crazygames.com/resources/basic-launch-metrics/
- CrazyGames, Quality requirements (onboarding): https://docs.crazygames.com/requirements/quality/
- CrazyGames, Ad monetization guide: https://docs.crazygames.com/resources/ad-monetization-guide/
- Anthony Pecorella, The Math of Idle Games, Part I: https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i
- Part II: https://www.gamedeveloper.com/disciplines/the-math-of-idle-games-part-ii
- Part III: https://www.gamedeveloper.com/design/the-math-of-idle-games-part-iii
- Original GDC talk "Quest for Progress" (Pecorella, GDC Europe 2016) listed at https://www.slideshare.net/slideshow/quest-for-progress-gdc-europe-2016/65405507 (not opened)
- Tagged [MEM] items (tier ratios, pacing numbers, portal hit traits, SDK call names, number-library names) come from general industry knowledge, not fetched this session. Verify before treating as rules.
