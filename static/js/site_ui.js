(()=>{
  'use strict';
  const header=document.querySelector('.header');
  const nav=header?.querySelector('.nav');
  const toggle=header?.querySelector('.converti-mobile-menu-toggle');
  if(!header||!nav||!toggle)return;
  const close=()=>{header.classList.remove('is-menu-open');toggle.setAttribute('aria-expanded','false')};
  toggle.addEventListener('click',()=>{
    const open=!header.classList.contains('is-menu-open');
    header.classList.toggle('is-menu-open',open);
    toggle.setAttribute('aria-expanded',String(open));
  });
  nav.addEventListener('click',e=>{if(e.target.closest('a'))close()});
  window.addEventListener('resize',()=>{if(window.innerWidth>720)close()},{passive:true});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
})();
