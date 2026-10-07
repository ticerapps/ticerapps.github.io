# ticerapps.github.io

Ticer Apps' static GitHub Pages site. No build step, JavaScript, analytics,
third-party fonts, or trackers are added by this site.

- `/`: both games and support links.
- `/quilt-bee/`: Quilt Bee product information and support. The app is in testing;
  do not add internal testing links or imply public store availability.
- `/quilt-bee/privacy/`: Quilt Bee's app-specific privacy policy.
- `/privacy/`: existing Minesweeper: Strait of Hormuz privacy policy. Keep this
  published URL stable for existing app/store links.
- `/app-ads.txt`: authorized advertising seller declaration; retain the existing
  Google publisher ID `pub-9806107692884322`.

Quilt Bee's icon is the approved Google Play icon copied from the game repository
at `store/google-play/icon-512.png`. The website uses the local copy in
`quilt-bee/assets/` and makes no external image/font request.

Preview from this directory with `python3 -m http.server 8769 --bind 127.0.0.1`.
Review desktop and narrow mobile layouts and verify local links before publishing.
