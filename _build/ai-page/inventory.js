
  // Copy buttons on asset rows and cards. The URL lives in data-copy.
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-copy]');
    if (!btn) return;
    try { await navigator.clipboard.writeText(btn.dataset.copy); } catch (err) { return; }
    const label = btn.querySelector('.uci');
    if (!label) return;
    const text = label.textContent;
    label.textContent = 'Copied';
    btn.classList.add('done');
    setTimeout(() => { label.textContent = text; btn.classList.remove('done'); }, 1400);
  });
