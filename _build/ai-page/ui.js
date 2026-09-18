  // Tabs
  const tabs = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.panel');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const name = tab.dataset.tab;
      tabs.forEach(t => t.setAttribute('aria-selected', t === tab ? 'true' : 'false'));
      panels.forEach(p => p.setAttribute('data-active', p.dataset.tab === name ? 'true' : 'false'));
    });
  });

  // Copy buttons
  document.querySelectorAll('.copy').forEach(btn => {
    btn.addEventListener('click', async () => {
      const pre = btn.parentElement.querySelector('pre');
      try {
        await navigator.clipboard.writeText(pre.innerText);
        const label = btn.textContent;
        btn.textContent = 'Copied';
        btn.classList.add('done');
        setTimeout(() => { btn.textContent = label; btn.classList.remove('done'); }, 1600);
      } catch (e) {
        const r = document.createRange(); r.selectNodeContents(pre);
        const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      }
    });
  });

  // The three acts. One on screen at a time, and the hash points at one.
  (function () {
    const acts = document.querySelectorAll('.act');
    const actpanels = document.querySelectorAll('.actpanel');
    if (!acts.length) return;

    function show(name, push) {
      if (![...actpanels].some(p => p.dataset.act === name)) return false;
      acts.forEach(a => a.setAttribute('aria-selected', a.dataset.act === name ? 'true' : 'false'));
      actpanels.forEach(p => p.setAttribute('data-active', p.dataset.act === name ? 'true' : 'false'));
      if (push && history.replaceState) history.replaceState(null, '', '#' + name);
      return true;
    }

    acts.forEach(a => a.addEventListener('click', () => show(a.dataset.act, true)));

    // A hash can name an act, or a tool tab inside act one.
    function fromHash() {
      const h = (location.hash || '').replace('#', '');
      if (!h) return;
      if (show(h, false)) { document.getElementById(h)?.scrollIntoView({ block: 'start' }); return; }
      const tab = document.querySelector('.tab[data-tab="' + CSS.escape(h) + '"]');
      if (tab) { show('connect', false); tab.click(); }
    }
    fromHash();
    window.addEventListener('hashchange', fromHash);
  })();
