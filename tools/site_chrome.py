"""Write the shared Apps menu into every page's header and set the stylesheet version.

Run from anywhere:  python3 tools/site_chrome.py [extra site folder ...]
The Apportionment Calculator lives in its own repo but is served under this domain,
so pass its folder too:  python3 tools/site_chrome.py ~/Desktop/dev/apportionment-calculator
Re-running is safe: the menu sits between apps-menu markers and is replaced in place.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CSS_VERSION = 5

CHEVRON = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'

# Category heading (link or None), then the apps under it.
GROUPS = [
    ("Minesweeper", ("/minesweeper/", "Games &amp; guides →"), [
        ("/minesweeper-strait-of-hormuz/", "minesweeper", "Minesweeper: Strait of Hormuz", "iOS · Android · browser", False),
        ("/gem-sweeper/", "gem-sweeper", "Gem Sweeper", "iOS · Android", True),
    ]),
    ("Block puzzle", None, [
        ("/quilt-bee/", "quilt-bee", "Quilt Bee: Block Puzzle", "Android · iOS soon", False),
    ]),
    ("Tools", None, [
        ("/apportionment-calculator/", "apportionment", "Apportionment Calculator", "iPhone · iPad · Mac", False),
        ("/apportionment-calculator/#versions", "apportionment/icon-lite", "Apportionment Calculator Lite", "Android · Free", False),
        ("/apportionment-calculator/#versions", "apportionment", "Apportionment Calculator Pro", "Android · $4.99", False),
    ]),
]


def menu():
    # The panel is a sibling of the <details>, not its child: browsers keep a closed <details>
    # element's content hidden whatever the CSS says, so hover could never reveal it.
    parts = ['<!-- apps-menu:start --><div class="apps-menu"><details class="apps-toggle">',
             f'<summary aria-controls="apps-panel">Apps {CHEVRON}</summary></details>',
             '<div class="apps-panel" id="apps-panel">']
    for name, link, apps in GROUPS:
        parts.append('<div class="apps-group">')
        if link:
            parts.append(f'<a class="group-label" href="{link[0]}">{name} <span>{link[1]}</span></a>')
        else:
            parts.append(f'<p class="group-label" style="margin:0">{name}</p>')
        for href, icon, title, where, soon in apps:
            # "app" uses assets/apps/app/icon.webp; "app/name" names another file there.
            icon_path = icon if '/' in icon else icon + '/icon'
            pill = '<span class="pill pill-soon">SOON</span>' if soon else ''
            parts.append(f'<a class="apps-item" href="{href}"><img src="/assets/apps/{icon_path}.webp" alt="" width="40" height="40" loading="lazy"><span><strong>{title}</strong><small>{where}</small></span>{pill}</a>')
        parts.append('</div>')
    parts.append('<a class="apps-all" href="/#apps">All apps →</a></div></div><!-- apps-menu:end -->')
    return ''.join(parts)


def apply(path, html):
    if 'class="nav" aria-label="Main"' not in html:
        return html
    m = menu()
    if '<!-- apps-menu:start -->' in html:
        html = re.sub(r'<!-- apps-menu:start -->.*?<!-- apps-menu:end -->', lambda _: m, html, flags=re.S)
    else:
        html, n = re.subn(r'(<nav class="nav" aria-label="Main">\s*)<a href="/?#apps"(?: aria-current="page")?>Apps</a>',
                          lambda g: g[1] + m, html, count=1)
        if not n:
            raise SystemExit(f'{path}: no Apps link to replace')
    return re.sub(r'/assets/site\.css(?:\?v=\d+)?"', f'/assets/site.css?v={CSS_VERSION}"', html)


def run(roots):
    changed = 0
    for root in roots:
        for path in sorted(root.rglob('*.html')):
            if '.git' in path.parts:
                continue
            old = path.read_text()
            new = apply(path, old)
            if new != old:
                path.write_text(new)
                changed += 1
    print(f'Apps menu and site.css?v={CSS_VERSION} applied to {changed} page(s).')


if __name__ == '__main__':
    run([ROOT] + [Path(p).expanduser().resolve() for p in sys.argv[1:]])
