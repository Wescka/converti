(function(){
  'use strict';
  const header = document.querySelector('.header');
  const toggle = document.querySelector('.site-mobile-menu-toggle');
  const nav = header && header.querySelector('.nav');
  if (!header || !toggle || !nav) return;

  function setOpen(open){
    header.classList.toggle('is-menu-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.documentElement.classList.toggle('converti-menu-open', open);
  }
  toggle.addEventListener('click', function(){ setOpen(!header.classList.contains('is-menu-open')); });
  nav.addEventListener('click', function(e){ if (e.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') setOpen(false); });
  window.addEventListener('resize', function(){ if(window.innerWidth > 860) setOpen(false); }, {passive:true});
})();
