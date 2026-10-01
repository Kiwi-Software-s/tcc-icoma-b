(() => {
  const toggle = document.querySelector('.mobile-menu-toggle');
  const drawer = document.getElementById('mobile-main-menu');
  if (!toggle || !drawer) return;

  const closeTargets = document.querySelectorAll('[data-mobile-menu-close]');

  function setOpen(open) {
    document.body.classList.toggle('mobile-menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    drawer.setAttribute('aria-hidden', String(!open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  }

  toggle.addEventListener('click', () => {
    setOpen(!document.body.classList.contains('mobile-menu-open'));
  });

  closeTargets.forEach((el) => el.addEventListener('click', () => setOpen(false)));
  drawer.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setOpen(false)));

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') setOpen(false);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) setOpen(false);
  });
})();
