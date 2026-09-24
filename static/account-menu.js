(() => {
  const trigger = document.querySelector('.eco-account-trigger');
  const menu = document.getElementById('eco-account-menu');
  if (!trigger || !menu) return;

  function positionMenu() {
    const rect = trigger.getBoundingClientRect();
    const left = Math.max(12, Math.min(rect.right - menu.offsetWidth, window.innerWidth - menu.offsetWidth - 12));
    const top = Math.max(12, Math.min(rect.bottom + 8, window.innerHeight - menu.offsetHeight - 12));
    menu.style.left = `${left}px`;
    menu.style.top = `${top}px`;
  }

  menu.addEventListener('toggle', () => {
    const open = menu.matches(':popover-open');
    trigger.setAttribute('aria-expanded', String(open));
    if (open) positionMenu();
  });
  window.addEventListener('resize', () => {
    if (menu.matches(':popover-open')) positionMenu();
  });
  window.addEventListener('scroll', () => {
    if (menu.matches(':popover-open')) menu.hidePopover();
  }, true);
})();
