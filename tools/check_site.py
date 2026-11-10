"""Check every page before publishing:  python3 tools/check_site.py [calculator repo folder]

One h1, a canonical URL that matches the page, unique ids, valid JSON-LD, local links,
#anchors and /assets/ files that exist, the Apps menu in every main header, and a sitemap
that lists only real pages. Pass the apportionment-calculator folder to check the links
into that site too; without it, links under /apportionment-calculator/ are skipped.
No third-party dependencies.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ticerapps.com/'
CALC = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else None
sys.path.insert(0, str(ROOT / 'tools' / 'minesweeper'))
from patterns import verify


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids = []; self.links = []; self.h1 = 0; self.canonical = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a.get('href'))


def local_file(path):
    """Map a URL path on ticerapps.com to the file that serves it, or None to skip."""
    path = unquote(path)
    if path.startswith('/apportionment-calculator'):
        if not CALC: return None
        rest = path[len('/apportionment-calculator'):].strip('/')
        f = CALC / (rest or 'index.html')
        return f / 'index.html' if f.is_dir() else (f if f.suffix else f.with_suffix('.html'))
    f = ROOT / path.lstrip('/')
    return f / 'index.html' if f.is_dir() else f


def url_for(f):
    if CALC and CALC in f.parents:
        rel = f.relative_to(CALC).as_posix()
        return BASE + 'apportionment-calculator/' + ('' if rel == 'index.html' else rel.removesuffix('.html'))
    rel = f.relative_to(ROOT).as_posix()
    return BASE + rel.removesuffix('index.html')


files = [f for f in ROOT.rglob('*.html') if '.git' not in f.parts and f.name != 'google982a63541b8cf743.html']
if CALC: files += [f for f in CALC.glob('*.html')]
pages = {f: Page(f.read_text()) for f in files}
errors = []
for f, page in pages.items():
    text = f.read_text(); rel = f.as_posix().replace(str(ROOT) + '/', ''); url = url_for(f)
    redirect = 'http-equiv="refresh"' in text
    if len(page.ids) != len(set(page.ids)): errors.append(f'{rel}: duplicate id')
    if not redirect and page.h1 != 1: errors.append(f'{rel}: {page.h1} h1 elements')
    if not redirect and '/get/' not in url and page.canonical != [url]: errors.append(f'{rel}: canonical {page.canonical} != {url}')
    if 'class="nav" aria-label="Main"' in text and 'apps-menu:start' not in text: errors.append(f'{rel}: no Apps menu (run tools/site_chrome.py)')
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try: json.loads(block)
        except ValueError as e: errors.append(f'{rel}: bad JSON-LD {e}')
    for link in page.links:
        target = urlparse(urljoin(url, link))
        if target.scheme not in ('http', 'https') or target.netloc != 'ticerapps.com': continue
        lf = local_file(target.path)
        if lf is None: continue
        if not lf.exists(): errors.append(f'{rel}: missing page {link}')
        elif target.fragment and lf in pages and target.fragment not in pages[lf].ids: errors.append(f'{rel}: missing anchor {link}')
    for src in re.findall(r'(?:src|href)="(/assets/[^"?#]+)', text):
        if not (ROOT / src.lstrip('/')).exists(): errors.append(f'{rel}: missing asset {src}')
for loc in re.findall(r'<loc>([^<]+)</loc>', (ROOT / 'sitemap.xml').read_text()):
    lf = local_file(urlparse(loc).path)
    if lf is not None and not lf.exists(): errors.append(f'sitemap: {loc} has no page')
count = verify()
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(pages)} pages, links, anchors, assets, JSON-LD, Apps menu, sitemap, {count} pattern proofs')
