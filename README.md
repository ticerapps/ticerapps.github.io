# ticerapps.com

Ticerapps' static GitHub Pages site, served at https://ticerapps.com (custom domain set
on 2026-11-10; old `ticerapps.github.io/...` links redirect to the same path). No build
step, analytics, cookies, third-party fonts, or trackers are added by this site. Three scripts
exist: `assets/get.js` on the `/get/` download links below (reads the device type and the link's
campaign tags, stores nothing), `assets/minesweeper/guides.js` on the pattern guide (the
practice boards; no network calls or storage) and `assets/video.js` on app pages with a video
(see Videos). The header's Apps menu is HTML and CSS only.

## Videos

App pages show their YouTube videos click-to-play: a `.video[data-yt]` box holds a still image
hosted here (`assets/apps/<app>/video*.webp`) linked to the video on YouTube, and
`assets/video.js` swaps it for YouTube's no-cookie player only when the visitor presses play.
Nothing loads from YouTube before that, which keeps the no-trackers promise above; each app's
privacy policy says so in its website section. The iframe sends `strict-origin-when-cross-origin`
because YouTube's player refuses to load without a referrer, while the pages send none. Each
video has VideoObject JSON-LD in the page head. Use `.video.tall` for a vertical Short and
`.videos` for a row of them. Current videos (2026-11-11): Gem Sweeper `VK5VexWlyZ0`, Quilt Bee `YscjTCfR6WM`,
Minesweeper: Strait of Hormuz `b3fSf2jTIck`, and on the Apportionment Calculator page the
iOS `PwQH0BlwuKk`, Android Lite `UnJv9vU5REw` and Android Pro `B3Tlbm96bvs` Shorts.

## Pages

- `/`: home. Every public app with its stores, prices and ratings, Gem Sweeper as
  the featured new game, the browser Minesweeper band, guides, and social links.
- `/quilt-bee/`: Quilt Bee page and support (`#support`). Free on Google Play; the App
  Store is shown as coming soon until it is live there.
- `/minesweeper-strait-of-hormuz/`: the game's page here. Its full home, guides and
  browser demo are the separate site minesweeperstraitofhormuz.com
  (repo `ticerapps/minesweeperstraitofhormuz.com`). Google Play lists it as
  "Minesweeper: REDACTED".
- `/apportionment-calculator/`: **not in this repo.** It is the project site of
  `ticerapps/apportionment-calculator` (index.html is the app page and support URL,
  privacy.html the policy). It uses this repo's `/assets/` and `/favicon.svg`. Never
  add an `apportionment-calculator/` folder here: it would collide with that site.
- `/minesweeper/`: the Minesweeper hub, added 2026-11-10: both Minesweeper games, the guides,
  the pattern library and an FAQ (FAQPage structured data). The guides live under it:
  `/minesweeper/how-to-play/` (general rules), `/minesweeper/strategy/` (12 patterns and the
  practice lessons) and `/minesweeper/no-guess/`. The pattern and no-guess guides moved here from
  minesweeperstraitofhormuz.com, whose old URLs now redirect; that site keeps the browser game,
  the strait boards and a game-specific How to play page (controls, HUD, board sizes).
  Block puzzle and Tools have no hub yet: give each one only when it has a guide of its own,
  then make its Apps-menu heading a link in `tools/site_chrome.py`.
- `/gem-sweeper/`: Gem Sweeper page and support. Free on Google Play since 2026-11-10 (Play title
  "Gem Sweeper (Minesweeper)"); the App Store is shown as coming soon until it is live there
  (its App Store name is "Gem Sweeper: Mine Puzzle").
- `/support/`: privacy and support hub listing every app's policy.
- `/quilt-bee/privacy/`, `/privacy/` (Minesweeper: Strait of
  Hormuz), `/gem-sweeper/privacy/`: policies. Store listings and released apps link to
  these exact URLs; never move them. The 2026-11-10 redesign changed only their header,
  footer and stylesheet, not their text.
- `/quilt-bee/delete-data/` was removed on 2026-11-10 at the owner's request: current Quilt Bee
  creates no accounts of its own (Play Games / Game Center only). Play Console's Data safety form
  was updated the same day (no account creation; data-deletion link
  `/quilt-bee/privacy/#choices`), and the Quilt Bee policy now routes deletion requests,
  including earlier Firebase test-build records, to ticerapps@gmail.com.
- `/app-ads.txt`: authorized advertising seller declaration; retain the existing
  Google publisher ID `pub-9806107692884322`.
- `/sitemap.xml`, `/robots.txt`: add new pages to the sitemap.
- `google982a63541b8cf743.html`: Google site verification; keep.

## Download links for ads (`/get/`)

One link per app that sends each visitor to the right store, for TikTok, Instagram, Facebook,
YouTube, Snapchat, Reddit, X, QR codes, a bio link or anywhere else:

| Link | iPhone / iPad | Android | Mac | Other computers |
| --- | --- | --- | --- | --- |
| `ticerapps.com/get/quilt-bee/` | Quilt Bee page (not on the App Store yet) | Google Play | app page | app page |
| `ticerapps.com/get/minesweeper/` | App Store | Google Play | browser game | browser game |
| `ticerapps.com/get/apportionment/` | App Store | Play, Lite | Mac App Store | app page |
| `ticerapps.com/get/apportionment-pro/` | App Store | Play, Pro | Mac App Store | app page |
| `ticerapps.com/get/gem-sweeper/` | Gem Sweeper page (not on the App Store yet) | Google Play | app page | app page |

- Each page also shows both store badges, so a visitor whose in-app browser blocks the
  automatic redirect can still tap through. Crawlers (link previews, ad review) stay on the
  page and see the badges.
- Campaign tags: add `?src=tiktok&c=launch-week`, or let the ad platform append standard
  `utm_source` / `utm_medium` / `utm_campaign` / `utm_content`. Google Play receives them as
  the install referrer (Play Console acquisition reports). The App Store receives `ct=<source>-<campaign>`
  with the provider token `123947823` (`data-apple-pt` on each `/get/` page; App Store Connect
  > App Analytics > Acquisition > Campaigns). The token only names the developer account, so
  it is safe to publish; Apple puts it in every public campaign link.
- `?stay` shows the page without redirecting, to check where a device would go.
- When an app reaches a store, fill its `data-ios` / `data-android` attribute and swap the
  matching "Coming soon" block for the badge with `data-store="ios"` or `data-store="android"`.
- The pages are `noindex` and left out of the sitemap so they don't compete with the app pages.

## Tools

- `python3 tools/site_chrome.py ~/Desktop/dev/apportionment-calculator` writes the Apps menu into
  the header of every page in both repos and sets the `site.css?v=N` version (`CSS_VERSION`). Edit
  the menu's apps and categories there, never by hand in a page.
- `python3 tools/minesweeper/build_strategy.py` regenerates the pattern guide between its
  `patterns` markers. `patterns.py` holds the 12 examples; each one is proved against every
  possible mine placement before the page is written. `practice.py` holds the two lessons.
- `python3 tools/check_site.py ~/Desktop/dev/apportionment-calculator` checks every page: one h1,
  canonical URLs, links, #anchors, assets, JSON-LD, the Apps menu, the sitemap and the pattern
  proofs. Run it before every push.

## Assets

- `assets/site.css`: the only stylesheet, linked as `site.css?v=N`; bump N in every page when
  the CSS changes, because GitHub Pages lets browsers cache it for 10 minutes. Per-app accents come from body classes
  (`theme-quilt`, `theme-apportion`, `theme-gem`; Minesweeper uses the default mint).
- `assets/brand/`: the orange T Ticerapps logo (Google Play developer icon, from
  `~/Desktop/Ticerapps-branding-2026-10-21/selected-workshop/`); `favicon.png` and
  `apple-touch-icon.png` at the root are made from it.
- `assets/fonts/`: self-hosted Inter and Space Grotesk (latin subsets, SIL OFL; licences
  beside them).
- `assets/badges/`: official App Store and Google Play badges, copied from the
  minesweeperstraitofhormuz.com repo.
- `assets/apps/<app>/`: 384px WebP icons and 540px-wide WebP screenshots. Quilt Bee's icon
  is the one Google Play serves; screenshots come from each game's store listing assets.
  `quilt-bee/assets/icon-512.png` is the earlier plush-bee icon, kept for old links.

Ratings and prices on the home and app pages are typed in by hand (US store, 2026-11-10);
update them when they change.

Preview the whole domain locally by copying this repo and the calculator repo into one
folder (`apportionment-calculator/` inside it) and serving it with
`python3 -m http.server 8769 --bind 127.0.0.1`. Check desktop and 375px layouts before
publishing.
