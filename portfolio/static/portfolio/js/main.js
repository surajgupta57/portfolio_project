document.addEventListener('DOMContentLoaded', function () {

  /* ===== Mobile nav toggle ===== */
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.querySelector('.nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const open = navLinks.style.display === 'flex';
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

  /* ===== Scroll reveal ===== */
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.15 });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('in'));
  }

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

  /* ===== Header background on scroll ===== */
  const headerEl = document.querySelector('header.site');
  if (headerEl) {
    window.addEventListener('scroll', () => {
      headerEl.style.boxShadow = window.scrollY > 20 ? '0 6px 24px rgba(16,28,48,.06)' : 'none';
    });
  }
});
