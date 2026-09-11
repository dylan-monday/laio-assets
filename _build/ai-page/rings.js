  // ----- orbital rings: intro centerpiece, then live header backdrop -----
  (function () {
    const canvas = document.getElementById('rings');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const EASY = '#E385FE', ELEC = '#F629CB';
    let W = 0, H = 0, DPR = 1, t = 0, raf = 0, running = false;
    const mouse = { x: 0, y: 0, tx: 0, ty: 0 };

    const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
    const map = (v, a1, a2, b1, b2) => b1 + (v - a1) / (a2 - a1) * (b2 - b1);
    const rX = (p, a) => { const c = Math.cos(a), s = Math.sin(a); return [p[0], p[1]*c - p[2]*s, p[1]*s + p[2]*c]; };
    const rY = (p, a) => { const c = Math.cos(a), s = Math.sin(a); return [p[0]*c + p[2]*s, p[1], -p[0]*s + p[2]*c]; };
    const rZ = (p, a) => { const c = Math.cos(a), s = Math.sin(a); return [p[0]*c - p[1]*s, p[0]*s + p[1]*c, p[2]]; };
    const proj = (p, persp, cx, cy) => { const z = p[2] + persp; const f = persp / Math.max(z, 1); return [cx + p[0]*f, cy + p[1]*f, z]; };
    const vn = v => { const l = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0]/l, v[1]/l, v[2]/l]; };
    const mid = (a, b) => [(a[0]+b[0])/2, (a[1]+b[1])/2, (a[2]+b[2])/2];
    const rgba = (hex, a) => `rgba(${parseInt(hex.slice(1,3),16)},${parseInt(hex.slice(3,5),16)},${parseInt(hex.slice(5,7),16)},${a})`;

    function sphere(r, sub) {
      const T = (1 + Math.sqrt(5)) / 2;
      let v = [[-1,T,0],[1,T,0],[-1,-T,0],[1,-T,0],[0,-1,T],[0,1,T],[0,-1,-T],[0,1,-T],[T,0,-1],[T,0,1],[-T,0,-1],[-T,0,1]].map(p => { const n = vn(p); return [n[0]*r, n[1]*r, n[2]*r]; });
      let f = [[0,11,5],[0,5,1],[0,1,7],[0,7,10],[0,10,11],[1,5,9],[5,11,4],[11,10,2],[10,7,6],[7,1,8],[3,9,4],[3,4,2],[3,2,6],[3,6,8],[3,8,9],[4,9,5],[2,4,11],[6,2,10],[8,6,7],[9,8,1]];
      for (let s = 0; s < sub; s++) {
        const nf = [], cache = {};
        const gm = (i, j) => { const k = Math.min(i,j)+'_'+Math.max(i,j); if (cache[k] != null) return cache[k]; const m = vn(mid(v[i], v[j])); v.push([m[0]*r, m[1]*r, m[2]*r]); return cache[k] = v.length - 1; };
        for (const fc of f) { const a = gm(fc[0],fc[1]), b = gm(fc[1],fc[2]), c = gm(fc[2],fc[0]); nf.push([fc[0],a,c],[fc[1],b,a],[fc[2],c,b],[a,b,c]); }
        f = nf;
      }
      const es = {}, edges = [];
      for (const fc of f) for (let i = 0; i < 3; i++) { const a = fc[i], b = fc[(i+1)%3], k = Math.min(a,b)+'_'+Math.max(a,b); if (!es[k]) { es[k] = 1; edges.push([a,b]); } }
      return { v, edges };
    }

    // per-ring orientation + an independent slow spin (random speed & direction), generated once
    const N = 6, sign = () => (Math.random() < 0.5 ? -1 : 1);
    const ringMeta = [];
    for (let r = 0; r < N; r++) {
      ringMeta.push({
        rFactor: 0.55 + (r / N) * 1.5,
        tiltX: r * 0.5 + 0.2,
        tiltZ: r * 0.75,
        rateX: sign() * (0.3 + Math.random() * 0.7),
        rateZ: sign() * (0.3 + Math.random() * 0.7),
        every: 9 + r
      });
    }

    let rings = [], core = null, scale = 0;
    function build() {
      scale = Math.min(W, H) * 0.32;
      rings = ringMeta.map(m => {
        const radius = scale * m.rFactor, pts = [];
        for (let i = 0; i <= 70; i++) { const a = (i / 70) * Math.PI * 2; pts.push([radius * Math.cos(a), 0, radius * Math.sin(a)]); }
        return { pts, meta: m };
      });
      core = sphere(scale * 0.2, 1);
    }

    function draw() {
      ctx.clearRect(0, 0, W, H);
      mouse.x += (mouse.tx - mouse.x) * 0.05;
      mouse.y += (mouse.ty - mouse.y) * 0.05;
      const cx = W / 2, cy = H * 0.48, persp = 950, near = persp * 0.45, far = persp * 1.9;
      const ax = 0.5 + mouse.y * 0.45, ay = t + mouse.x * 0.55;
      const G = p => rY(rX(p, ax), ay);                       // whole-system spin + mouse parallax
      for (const ring of rings) {
        const m = ring.meta;
        const lx = m.tiltX + t * m.rateX, lz = m.tiltZ + t * m.rateZ;  // each ring's own slow spin
        const T = p => G(rZ(rX(p, lx), lz));
        ctx.lineWidth = 1;
        for (let i = 0; i < ring.pts.length - 1; i++) {
          const a = proj(T(ring.pts[i]), persp, cx, cy), b = proj(T(ring.pts[i+1]), persp, cx, cy);
          ctx.strokeStyle = rgba(EASY, clamp(map((a[2]+b[2])/2, near, far, 0.5, 0.05), 0.03, 0.5));
          ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
        }
        for (let i = 0; i < ring.pts.length; i += m.every) {
          const a = proj(T(ring.pts[i]), persp, cx, cy);
          ctx.fillStyle = rgba(ELEC, clamp(map(a[2], near, far, 0.85, 0.1), 0.05, 0.85));
          ctx.beginPath(); ctx.arc(a[0], a[1], clamp(map(a[2], near, far, 3, 0.8), 0.6, 3), 0, Math.PI * 2); ctx.fill();
        }
      }
      ctx.lineWidth = 1;
      for (const e of core.edges) {
        const a = proj(G(core.v[e[0]]), persp, cx, cy), b = proj(G(core.v[e[1]]), persp, cx, cy);
        ctx.strokeStyle = rgba(EASY, clamp(map((a[2]+b[2])/2, near, far, 0.55, 0.08), 0.05, 0.55));
        ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
      }
    }

    function resize() {
      DPR = Math.min(window.devicePixelRatio || 1, 2);
      W = window.innerWidth; H = window.innerHeight;
      canvas.width = W * DPR; canvas.height = H * DPR;
      canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      build();
    }
    const loop = () => { t += 0.0016; draw(); raf = requestAnimationFrame(loop); };
    const start = () => { if (!running) { running = true; loop(); } };
    const stop = () => { running = false; cancelAnimationFrame(raf); };

    resize();
    window.addEventListener('resize', () => { resize(); if (!running) draw(); });

    const motionOK = window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
    if (motionOK) {
      window.addEventListener('mousemove', e => { mouse.tx = e.clientX / W - 0.5; mouse.ty = e.clientY / H - 0.5; });
      start();
      const hero = document.querySelector('.hero');
      if (hero && 'IntersectionObserver' in window) {
        new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? start() : stop()), { threshold: 0 }).observe(hero);
      }
    } else {
      draw(); // single static frame
    }
  })();

  // ----- intro choreography + scroll reveals -----
  (function () {
    const root = document.documentElement;
    const intro = document.getElementById('intro');
    const introLogo = document.getElementById('intro-logo');

    ['.hero .laio-mark', '.hero .eyebrow', '.hero h1', '.hero .sub'].forEach((sel, i) => {
      const el = document.querySelector(sel);
      if (el) { el.classList.add('reveal-h'); el.style.setProperty('--i', i); }
    });
    const revealEls = document.querySelectorAll('.sec-eyebrow, .block h2, .lead, .door, .fam, .voice .col, .pillars, .tabs');
    revealEls.forEach(el => el.classList.add('reveal'));
    document.querySelectorAll('.doors .door').forEach((el, i) => el.style.setProperty('--i', i));
    document.querySelectorAll('.families .fam').forEach((el, i) => el.style.setProperty('--i', i));

    const motionOK = window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
    if (!motionOK) {
      root.classList.add('hero-in');
      if (intro) intro.remove();
      if (introLogo) introLogo.remove();
      return;
    }

    root.classList.add('anim', 'intro-active');
    document.body.style.overflow = 'hidden';

    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    revealEls.forEach(el => io.observe(el));

    const endIntro = () => { root.classList.remove('intro-active'); root.classList.add('hero-in'); document.body.style.overflow = ''; };
    const kill = () => { if (intro && intro.parentNode) intro.remove(); if (introLogo && introLogo.parentNode) introLogo.remove(); };
    const t1 = setTimeout(endIntro, 2600);
    const t2 = setTimeout(kill, 3200);
    const skip = () => {
      clearTimeout(t1); clearTimeout(t2);
      [intro, introLogo].forEach(n => { if (n) { n.style.animation = 'none'; n.style.transition = 'opacity .3s ease'; n.style.opacity = '0'; } });
      endIntro();
      setTimeout(kill, 320);
    };
    if (introLogo) introLogo.addEventListener('click', skip);
    if (intro) intro.addEventListener('click', skip);
  })();
