document.addEventListener('DOMContentLoaded', function () {

  /* ===== Animation preference ===== */
  const body = document.body;
  const animationMode = body.dataset.animationMode || 'device';
  const deviceReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const motionEnabled = animationMode === 'full' || (animationMode === 'device' && !deviceReduced);
  body.classList.add(motionEnabled ? 'motion-on' : 'motion-off');

  /* ===== Mobile nav toggle ===== */
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.querySelector('.nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const open = navLinks.style.display === 'flex';
      navToggle.setAttribute('aria-expanded', String(!open));
      navLinks.style.display = open ? 'none' : 'flex';
      navLinks.style.flexDirection = 'column';
      navLinks.style.position = 'absolute';
      navLinks.style.top = '74px';
      navLinks.style.right = '0';
      navLinks.style.left = '0';
      navLinks.style.background = 'var(--paper)';
      navLinks.style.padding = '20px 32px';
      navLinks.style.borderBottom = '1px solid var(--line-light)';
      navLinks.style.gap = '18px';
    });
  }

  /* ===== Scroll reveal choreography ===== */
  const revealEls = document.querySelectorAll('.reveal');
  revealEls.forEach((el, index) => {
    const parent = el.parentElement;
    const siblings = parent ? Array.from(parent.children).filter(child => child.classList.contains('reveal')) : [];
    const siblingIndex = Math.max(0, siblings.indexOf(el));
    el.style.setProperty('--reveal-delay', `${Math.min(siblingIndex * 85, 340)}ms`);
    if (el.classList.contains('tl-item')) el.classList.add('from-right');
    if (el.classList.contains('proj-card') || el.classList.contains('edu-card')) el.classList.add('scale-in');
  });
  if (motionEnabled && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -5% 0px' });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('in'));
  }

  /* ===== Statistics counters ===== */
  const counters = document.querySelectorAll('[data-count]');
  function animateCounter(el) {
    if (el.dataset.counted === 'true') return;
    el.dataset.counted = 'true';
    const label = el.dataset.count || el.textContent.trim();
    const match = label.match(/([0-9]+(?:\.[0-9]+)?)(.*)/);
    if (!match || !motionEnabled) { el.textContent = label; return; }
    const target = Number(match[1]);
    const suffix = match[2];
    const start = performance.now();
    const duration = 1100;
    function frame(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = `${Math.round(target * eased)}${suffix}`;
      if (progress < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  if (motionEnabled && 'IntersectionObserver' in window) {
    const counterObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { animateCounter(entry.target); counterObserver.unobserve(entry.target); }
      });
    }, { threshold: .65 });
    counters.forEach(counter => counterObserver.observe(counter));
  } else counters.forEach(animateCounter);

  /* ===== Generic rotating-card carousel (used for hero ledger + testimonials) ===== */
  function setupCarousel(viewportSelector, dotsSelector, cardClass, intervalMs) {
    const viewport = document.getElementById(viewportSelector);
    const dotsWrap = document.getElementById(dotsSelector);
    if (!viewport || !dotsWrap) return;
    const cards = () => viewport.querySelectorAll('.' + cardClass);
    const dots = () => dotsWrap.querySelectorAll('button');
    let idx = 0;
    let timer = null;

    function show(i) {
      cards().forEach(c => c.classList.remove('active'));
      dots().forEach(d => d.classList.remove('active'));
      if (cards()[i]) cards()[i].classList.add('active');
      if (dots()[i]) dots()[i].classList.add('active');
      idx = i;
    }

    dots().forEach((dot, i) => dot.addEventListener('click', () => { show(i); resetTimer(); }));

    function resetTimer() {
      if (timer) clearInterval(timer);
      const total = cards().length;
      if (total > 1) {
        timer = setInterval(() => show((idx + 1) % total), intervalMs);
      }
    }
    resetTimer();

    const parentToWatch = viewport.closest('.ledger') || viewport;
    parentToWatch.addEventListener('mouseenter', () => { if (timer) clearInterval(timer); });
    parentToWatch.addEventListener('mouseleave', resetTimer);
  }

  setupCarousel('ledgerViewport', 'ledgerDots', 'ledger-card', 4200);
  setupCarousel('testiViewport', 'testiDots', 'testi-card', 5200);

  /* ===== Skills hover/click tabs ===== */
  const skillTabs = document.querySelectorAll('.skill-tab');
  const skillPanes = document.querySelectorAll('.skill-pane');
  function activateTab(tab) {
    skillTabs.forEach(t => t.classList.remove('active'));
    skillPanes.forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    const pane = document.getElementById('pane-' + tab.dataset.pane);
    if (pane) pane.classList.add('active');
  }
  skillTabs.forEach(tab => {
    tab.addEventListener('mouseenter', () => activateTab(tab));
    tab.addEventListener('click', () => activateTab(tab));
  });

  /* ===== Contact form -> mailto ===== */
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const name = document.getElementById('cname').value;
      const email = document.getElementById('cemail').value;
      const msg = document.getElementById('cmsg').value;
      const mailto = contactForm.dataset.mailto || '';
      const subject = encodeURIComponent(`Portfolio inquiry from ${name}`);
      const body = encodeURIComponent(`${msg}\n\n— ${name} (${email})`);
      window.location.href = `mailto:${mailto}?subject=${subject}&body=${body}`;
    });
  }

  /* ===== Scroll progress, header state, back to top ===== */
  const headerEl = document.querySelector('header.site');
  const scrollProgress = document.getElementById('scrollProgress');
  const scrollTopButton = document.getElementById('scrollTop');
  let scrollTicking = false;
  function updateScrollUI() {
    const y = window.scrollY;
    const max = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    if (scrollProgress) scrollProgress.style.width = `${Math.min((y / max) * 100, 100)}%`;
    if (headerEl) headerEl.classList.toggle('scrolled', y > 20);
    if (scrollTopButton) scrollTopButton.classList.toggle('visible', y > 600);
    scrollTicking = false;
  }
  window.addEventListener('scroll', () => {
    if (!scrollTicking) { requestAnimationFrame(updateScrollUI); scrollTicking = true; }
  }, { passive: true });
  if (scrollTopButton) scrollTopButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: motionEnabled ? 'smooth' : 'auto' });
  });
  updateScrollUI();
});
