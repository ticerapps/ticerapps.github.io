"""Render the pattern library into minesweeper/strategy/index.html.

Run:  python3 tools/minesweeper/build_strategy.py
Every example in patterns.py is checked against all possible mine placements first, so a
diagram can never show a move that isn't forced. Only the part between the patterns markers
is generated; the rest of the page is ordinary HTML.
"""
from pathlib import Path
import html
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from patterns import PATTERNS, verify
from practice import render_practice

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'minesweeper/strategy/index.html'
PLAY = 'https://minesweeperstraitofhormuz.com/#play'


def board(p, quiz=False):
    width = len(p['board'][0]); out = []
    for i, c in enumerate(''.join(p['board'])):
        cls = 'pattern-cell '; label = ''; inside = html.escape(c)
        if c == '#': cls += 'outside'; inside = ''; label = 'Outside this example'
        elif c == 'F': cls += 'flag'; inside = '⚑'; label = 'Proven mine'
        elif c.isdigit(): cls += 'clue n' + c; label = f'{c} adjacent mines'
        else:
            cls += 'covered'; label = f'Hidden tile {i + 1}'; answer = ''
            if i in p['mines']: cls += ' answer-marked answer-mine'; answer = '⚑'
            if i in p['safe']: cls += ' answer-marked answer-safe'; answer = '✓'
            inside = f'<span class="hidden-symbol" aria-hidden="true">?</span><span class="answer-symbol" aria-hidden="true">{answer}</span>'
        if quiz and c == '?':
            pos = ('left', 'middle', 'right')[i]
            out.append(f'<button type="button" class="{cls}" data-quiz-answer="{"safe" if i in p["safe"] else "mine"}" data-original-label="Try {pos} tile" aria-label="Try {pos} tile">{inside}</button>')
        else:
            out.append(f'<span role="img" class="{cls}" aria-label="{label}" data-original-label="{label}">{inside}</span>')
    bid = 'quiz-board' if quiz else 'board-' + p['id']
    return f'<div class="pattern-board" id="{bid}" style="--cols:{width}" role="group" aria-label="{html.escape(p["title"])} example">' + ''.join(out) + '</div>'


def article():
    cards = []
    for n, p in enumerate(PATTERNS, 1):
        note = '1 mine in this whole example' if 'total' in p else 'Rotate or mirror the same layout'
        cards.append(f'''<section class="pattern-card" id="{p['id']}"><p class="pattern-group">{n:02d} / {p['group']}</p><h2>{p['title']}</h2><div class="pattern-stage">{board(p)}</div><div class="pattern-answer"><button type="button" data-answer="board-{p['id']}" aria-controls="board-{p['id']}" aria-expanded="false">Show solution</button><small>{note}</small></div><details><summary>Why it works</summary><p>{p['text']}</p></details></section>''')
    one_two_one = next(p for p in PATTERNS if p['id'] == 'one-two-one')
    return f'''<div class="guide-intro"><div><p class="eyebrow">Strategy guide / 12 visual reads</p><h1>Minesweeper patterns. See the next move.</h1><p class="lead">Read the numbers. Spot the pattern. Open a tile you can prove is safe.</p><p><a href="/minesweeper/how-to-play/">New to Minesweeper? Start with the rules.</a></p></div><section class="quiz" aria-label="Interactive 1–2–1 exercise"><h2>Which tile is safe?</h2>{board(one_two_one, True)}<p class="quiz-feedback" id="quiz-feedback" role="status" aria-live="polite">Tap one of the three hidden tiles.</p><button type="button" class="text-button" data-quiz-reset hidden>Try again</button><noscript><p>The middle tile is safe. The outer two must be mines.</p></noscript></section></div>
<div class="pattern-legend"><span>? Unresolved</span><span class="legend-safe">✓ Proven safe</span><span class="legend-mine">⚑ Proven mine</span></div>
<p class="pattern-note">These are cropped examples: all hidden neighbours of the numbered clues are shown. Hatched cells are outside the example. Flags stand for proven mines. A matching string of numbers is not enough if extra hidden neighbours change the clues.</p>
<nav class="guide-jump" aria-label="Pattern groups"><a href="#chord-practice">Practice chording</a><a href="#flag-reduction">Worked example</a><a href="#all-mines">Basic patterns</a><a href="#one-one">Edge patterns</a><a href="#one-one-plus">Holes &amp; corners</a><a href="#counting">Endgame</a></nav>
{render_practice()}
<h2 class="pattern-library-heading" id="library">The pattern library</h2>
<div class="pattern-cards">{''.join(cards)}</div>
<div class="guide-end"><section><h2>Chord once the flags are proven.</h2><p>When the adjacent flags match a number, tap that number to open its remaining neighbours. Chording trusts your flags; it does not check whether they are correct.</p></section><section><h2>Mind the edges of odd shapes.</h2><p>Boards that are not rectangles, like the coastline boards in Minesweeper: Strait of Hormuz, use the same eight-neighbour rule, diagonals included. Land removes neighbours, so count the actual tiles before applying an edge pattern.</p></section><section><h2>A zero counter is not proof.</h2><p>The mine counter subtracts placed flags, including wrong ones. Only treat the remaining tiles as safe when every flag is justified and every mine is accounted for.</p></section><section><h2>Keep learning.</h2><p>Try these reads on the <a href="{PLAY}">free browser boards</a>, or learn them one at a time in <a href="/gem-sweeper/">Gem Sweeper</a>’s 50 teaching puzzles. For more community terminology, see <a href="https://minesweeper.online/help/patterns">Minesweeper Online’s pattern reference</a>. Diagrams on this page are our own.</p></section></div>'''


def main():
    count = verify()
    page = PAGE.read_text()
    new = re.sub(r'<!-- patterns:start -->.*?<!-- patterns:end -->',
                 lambda _: '<!-- patterns:start -->' + article() + '<!-- patterns:end -->', page, flags=re.S)
    if new == page and '<!-- patterns:start -->' not in page:
        raise SystemExit('patterns markers missing')
    PAGE.write_text(new)
    print(f'Verified {count} patterns and rendered the strategy guide.')


if __name__ == '__main__':
    main()
