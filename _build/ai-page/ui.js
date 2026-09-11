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
