// JavaScript for browsers without Popover API support:
document.querySelectorAll('[popover]').forEach(popover => {
  if (!HTMLElement.prototype.hasOwnProperty('popover')) {
    const target = document.querySelector(`[popovertarget="${popover.id}"]`);
    target.addEventListener('click', () => {
      popover.classList.toggle('hidden');
    });
  }
});