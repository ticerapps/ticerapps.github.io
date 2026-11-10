# ticerapps.com

Ticerapps' static GitHub Pages site, served at https://ticerapps.com (custom domain set
on 2026-11-10; old `ticerapps.github.io/...` links redirect to the same path). No build
step, analytics, cookies, third-party fonts, or trackers are added by this site. The only
JavaScript is `assets/get.js` on the `/get/` download links below; it reads the device type and
the link's campaign tags and stores nothing.

## Pages

- `/`: home. Every public app with its stores, prices and ratings, Gem Sweeper as
  coming soon, the browser Minesweeper band, guides, and social links.
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
- `/gem-sweeper/`: Gem Sweeper page and support, marked coming soon. When it launches,
  swap the two dashed "Coming soon" store blocks for the official badges.
- `/support/`: privacy and support hub listing every app's policy.
- `/quilt-bee/privacy/`, `/quilt-bee/delete-data/`, `/privacy/` (Minesweeper: Strait of
  Hormuz), `/gem-sweeper/privacy/`: policies. Store listings and released apps link to
  these exact URLs; never move them. The 2026-11-10 redesign changed only their header,
  footer and stylesheet, not their text.
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
| `ticerapps.com/get/gem-sweeper/` | Gem Sweeper page until launch | same | same | same |

- Each page also shows both store badges, so a visitor whose in-app browser blocks the
  automatic redirect can still tap through. Crawlers (link previews, ad review) stay on the
  page and see the badges.
- Campaign tags: add `?src=tiktok&c=launch-week`, or let the ad platform append standard
  `utm_source` / `utm_medium` / `utm_campaign` / `utm_content`. Google Play receives them as
  the install referrer (Play Console acquisition reports). The App Store only receives a
  campaign once `data-apple-pt` on each `/get/` page holds the provider token from App Store
  Connect's campaign link generator; it is empty for now.
- `?stay` shows the page without redirecting, to check where a device would go.
- When an app reaches a store, fill its `data-ios` / `data-android` attribute and swap the
  matching "Coming soon" block for the badge with `data-store="ios"` or `data-store="android"`.
- The pages are `noindex` and left out of the sitemap so they don't compete with the app pages.

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
