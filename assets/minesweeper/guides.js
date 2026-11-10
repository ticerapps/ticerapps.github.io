/* Minesweeper guides: the 1–2–1 quiz, Show solution buttons and the two practice lessons.
   Works locally: no network calls, storage or saved progress. Ported from minesweeperstraitofhormuz.com. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const showBoard = (board, show) => {
    board.classList.toggle('show-answer',show);
    board.querySelectorAll('[data-original-label]').forEach(cell => {
      cell.setAttribute('aria-label',show && cell.classList.contains('answer-safe') ? 'Proven safe' : show && cell.classList.contains('answer-mine') ? 'Proven mine' : cell.dataset.originalLabel);
    });
  };
  document.querySelectorAll('[data-answer]').forEach(button => {
    button.addEventListener('click',() => {
      const board=document.getElementById(button.dataset.answer);
      const show=button.getAttribute('aria-expanded') !== 'true';
      showBoard(board,show);
      if(!board.querySelector('.answer-marked'))board.closest('.pattern-card').querySelector('details').open=show;
      button.setAttribute('aria-expanded',String(show));
      button.textContent=show?'Hide solution':'Show solution';
    });
  });
  const quiz=document.getElementById('quiz-board');
  if (quiz) {
    const feedback=document.getElementById('quiz-feedback'), reset=document.querySelector('[data-quiz-reset]');
    quiz.querySelectorAll('button').forEach(button=>button.addEventListener('click',()=>{
      if (button.dataset.quizAnswer==='safe') {
        showBoard(quiz,true); feedback.textContent='Exactly. The 2 needs both outer tiles to be mines. The middle is safe.';
        quiz.querySelectorAll('button').forEach(b=>{b.disabled=true;});reset.hidden=false;
      } else feedback.textContent='That outer tile must be a mine. The two 1s limit the 2. Try another tile.';
    }));
    reset.addEventListener('click',()=>{ showBoard(quiz,false);quiz.querySelectorAll('button').forEach(b=>{b.disabled=false;});feedback.textContent='Tap one of the three hidden tiles.';reset.hidden=true;quiz.querySelector('button').focus(); });
  }
  const chord = document.getElementById('chord-practice');
  if (chord) {
    const tiles = [...chord.querySelectorAll('[data-flag]')];
    const trigger = chord.querySelector('[data-chord]');
    const reset = chord.querySelector('[data-chord-reset]');
    const feedback = chord.querySelector('[data-chord-feedback]');
    const count = chord.querySelector('[data-flag-count]');
    const flags = new Set();
    let finished = false;
    const updateFlags = () => {
      count.textContent = `${flags.size} / 2 flags`;
      tiles.forEach(tile => {
        const flagged = flags.has(tile.dataset.flag);
        tile.textContent = flagged ? '⚑' : '?';
        tile.classList.toggle('is-flagged', flagged);
        tile.setAttribute('aria-pressed', String(flagged));
        tile.setAttribute('aria-label', `${tile.dataset.position} ${flagged ? 'flagged' : 'hidden'} tile: toggle flag`);
      });
    };
    tiles.forEach(tile => {
      tile.disabled = false;
      tile.addEventListener('click', () => {
        if (finished) return;
        const id = tile.dataset.flag;
        if (flags.has(id)) flags.delete(id); else flags.add(id);
        updateFlags();
        feedback.textContent = flags.size === 2
          ? 'Two flags placed. Check the 1–2–1 clues, then tap the outlined 2.'
          : flags.size > 2 ? 'Too many flags for the 2. Tap a flag to remove it.'
          : 'Place flags on the two tiles you can prove are mines.';
      });
    });
    trigger.disabled = reset.disabled = false;
    trigger.addEventListener('click', () => {
      if (finished) return;
      if (flags.size !== 2) {
        feedback.textContent = `No chord yet: the 2 touches ${flags.size} flags. It needs exactly two. Prove their positions first.`;
        return;
      }
      finished = true;
      const correct = tiles.every(tile => flags.has(tile.dataset.flag) === (tile.dataset.mine === 'true'));
      tiles.forEach(tile => {
        tile.disabled = true;
        if (!flags.has(tile.dataset.flag)) {
          tile.classList.remove('covered');
          tile.classList.add(correct ? 'is-safe' : 'is-mine');
          tile.textContent = correct ? '2' : '✹';
          tile.setAttribute('aria-label', correct ? 'Middle tile revealed safely: 2 adjacent mines' : `${tile.dataset.position} tile: mine hit`);
        } else if (tile.dataset.mine !== 'true') {
          tile.classList.add('is-wrong');
          tile.textContent = '×';
          tile.setAttribute('aria-label', 'Middle tile: incorrect flag on a safe tile');
        }
      });
      feedback.textContent = correct
        ? 'Safe! The outer mines are flagged, so the chord opens the middle tile. Its 2 counts those same two mines.'
        : 'Mine hit. The count matched, but a flag was wrong. The two outer tiles are mines; the middle is safe. Reset and try those flags.';
    });
    reset.addEventListener('click', () => {
      flags.clear(); finished = false;
      tiles.forEach(tile => { tile.className = 'pattern-cell covered'; tile.disabled = false; });
      updateFlags();
      feedback.textContent = 'Place flags on the two tiles you can prove are mines.';
      tiles[0].focus();
    });
  }

  const reduction = document.getElementById('flag-reduction');
  if (reduction) {
    let step = 0;
    const next = reduction.querySelector('[data-reduction-next]');
    const reset = reduction.querySelector('[data-reduction-reset]');
    const messages = [
      'The bottom flag touches all three numbers. It already accounts for one mine in each.',
      'Subtract that one known mine: 2−1, 3−1, 2−1. These are remaining counts, not changed board numbers.',
      'The remaining counts are 1–2–1. Each outer 1 limits its pair to one mine; together with the 2, this forces the two outside tiles.',
      'Flag the left and right hidden tiles. The middle is safe. Original clues are shown again: 2–3–2.'
    ];
    const labels = ['Subtract the flag →', 'Read the pattern →', 'Show the safe move →', 'Replay example ↺'];
    const render = () => {
      reduction.querySelector('[data-reduction-count]').textContent = `Step ${step + 1} / 4`;
      reduction.querySelector('[data-reduction-feedback]').textContent = messages[step];
      reduction.querySelector('[data-reduction-caption]').textContent = step === 1 || step === 2
        ? 'Remaining mine counts · original clues stay 2–3–2'
        : step === 3 ? '⚑ Proven mine · ✓ Proven safe · original clues' : 'Original board clues';
      reduction.querySelectorAll('[data-clue]').forEach(cell => {
        const original = Number(cell.dataset.clue);
        const reduced = step === 1 || step === 2;
        const value = original - Number(reduced);
        cell.textContent = String(value);
        cell.className = `pattern-cell clue n${value}${reduced ? ' is-reduced' : ''}`;
        cell.setAttribute('aria-label', reduced ? `Original clue ${original}, remaining mines ${value}` : `${original} adjacent mines`);
      });
      reduction.querySelectorAll('[data-result]').forEach(cell => {
        const solved = step === 3;
        const safe = cell.dataset.result === 'safe';
        cell.className = `pattern-cell ${solved ? safe ? 'is-safe' : 'flag' : 'covered'}`;
        cell.textContent = solved ? safe ? '✓' : '⚑' : '?';
        cell.setAttribute('aria-label', solved ? safe ? 'Middle tile: proven safe' : `${cell.dataset.label}: proven mine` : cell.dataset.label);
      });
      reduction.querySelectorAll('.reduction-steps li').forEach((item, i) => {
        if (i === step) item.setAttribute('aria-current', 'step'); else item.removeAttribute('aria-current');
      });
      next.textContent = labels[step];
    };
    next.disabled = reset.disabled = false;
    next.addEventListener('click', () => { step = (step + 1) % messages.length; render(); });
    reset.addEventListener('click', () => { step = 0; render(); next.focus(); });
    render();
  }
})();
