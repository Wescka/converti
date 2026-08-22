(()=>{'use strict';
const I=window.CVB_I18N||{},$=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const page=$('#cvbPage');try{localStorage.removeItem('converti_cv_builder_v1')}catch(_){}
const state={template:'modern',accent:'#2a7bff',accentGradient:'linear-gradient(135deg,#2a7bff,#65a7ff)',photo:'',experience:[],education:[],skills:[],languages:[],certifications:[]};
const listKinds=['experience','education','skills','languages','certifications'];
const esc=s=>String(s??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const val=k=>$(`[data-bind="${k}"]`)?.value.trim()||'';
const initials=n=>(n||'CV').split(/\s+/).filter(Boolean).slice(0,2).map(x=>x[0]).join('').toUpperCase();
const schemas={experience:[['role',I.role||'Cargo'],['company',I.company||'Empresa'],['period',I.period||'Periodo'],['description',I.description||'Descripción','textarea']],education:[['degree',I.degree||'Título'],['school',I.school||'Institución'],['period',I.period||'Periodo'],['description',I.description||'Descripción','textarea']],skills:[['name',I.skill||'Habilidad']],languages:[['name',I.language_name||'Idioma'],['level',I.level||'Nivel']],certifications:[['name',I.cert_name||'Certificación'],['issuer',I.issuer||'Emisor'],['year',I.year||'Año']]};
const containers={experience:'#experienceBlocks',education:'#educationBlocks',skills:'#skillsBlocks',languages:'#languagesBlocks',certifications:'#certificationBlocks'};
function renderContact(){const items=[val('email'),val('phone'),val('city'),val('website')].filter(Boolean);$('#cvContact').innerHTML=items.map(x=>`<div class="cvb-contact-item">${esc(x)}</div>`).join('')}
function renderList(target,items,kind){const el=$(target);if(!el)return;if(kind==='experience')el.innerHTML=items.map(x=>`<article class="cvb-entry"><div class="cvb-entry-head"><strong>${esc(x.role)}</strong><span>${esc(x.period)}</span></div><div class="cvb-entry-sub">${esc(x.company)}</div>${x.description?`<p>${esc(x.description)}</p>`:''}</article>`).join('');if(kind==='education')el.innerHTML=items.map(x=>`<article class="cvb-entry"><div class="cvb-entry-head"><strong>${esc(x.degree)}</strong><span>${esc(x.period)}</span></div><div class="cvb-entry-sub">${esc(x.school)}</div>${x.description?`<p>${esc(x.description)}</p>`:''}</article>`).join('');if(kind==='certifications')el.innerHTML=items.map(x=>`<article class="cvb-entry"><div class="cvb-entry-head"><strong>${esc(x.name)}</strong><span>${esc(x.year)}</span></div><div class="cvb-entry-sub">${esc(x.issuer)}</div></article>`).join('')}
function renderAll(){if(!page)return;$('#cvName').textContent=val('name')||I.full_name||'Nombre';$('#cvTitle').textContent=val('title');$('#cvProfile').textContent=val('profile');$('#cvPhotoPlaceholder').textContent=initials(val('name'));renderContact();$('#cvSkills').innerHTML=state.skills.filter(x=>x.name).slice(0,8).map(x=>`<span class="cvb-chip">${esc(x.name)}</span>`).join('');$('#cvLanguages').innerHTML=state.languages.filter(x=>x.name).map(x=>`<div class="cvb-language-item"><span>${esc(x.name)}</span><span>${esc(x.level)}</span></div>`).join('');renderList('#cvExperience',state.experience,'experience');renderList('#cvEducation',state.education,'education');renderList('#cvCertifications',state.certifications,'certifications');page.style.setProperty('--accent',state.accent);page.style.setProperty('--accent-grad',state.accentGradient||state.accent);page.className=`cvb-page template-${state.template}`;if(page.scrollHeight>page.clientHeight+2)page.classList.add('cvb-density-compact');if(page.scrollHeight>page.clientHeight+2)page.classList.add('cvb-density-tight');syncExportAvailability();requestAnimationFrame(()=>{if(typeof fitPreview==='function')fitPreview()})}
function renderEditor(kind){const box=$(containers[kind]);if(!box)return;box.innerHTML='';state[kind].forEach((item,idx)=>{const card=document.createElement('div');card.className='cvb-dynamic-card';schemas[kind].forEach(([key,label,type])=>{const wrap=document.createElement('label');if(type==='textarea')wrap.classList.add('wide');wrap.innerHTML=`<span class="sr-only">${esc(label)}</span>${type==='textarea'?`<textarea rows="3" placeholder="${esc(label)}">${esc(item[key]||'')}</textarea>`:`<input placeholder="${esc(label)}" value="${esc(item[key]||'')}">`}`;const input=wrap.querySelector('input,textarea');input.addEventListener('input',()=>{state[kind][idx][key]=input.value;renderAll()});card.appendChild(wrap)});const rm=document.createElement('button');rm.type='button';rm.className='cvb-remove-btn';rm.title=I.remove||'Eliminar';rm.textContent='×';rm.onclick=()=>{state[kind].splice(idx,1);renderEditor(kind);renderAll()};card.appendChild(rm);box.appendChild(card)})}
function add(kind){if(kind==='skills'&&state.skills.length>=8)return;const obj={};schemas[kind].forEach(([k])=>obj[k]='');state[kind].push(obj);renderEditor(kind);renderAll();$(containers[kind])?.lastElementChild?.querySelector('input,textarea')?.focus()}
function closeAssistant(){$('#cvbAiPanel').hidden=true;$$('[data-assistant]').forEach(b=>b.classList.remove('is-active'))}
function resetDraft(){['name','title','email','phone','city','website','profile'].forEach(k=>{const e=$(`[data-bind="${k}"]`);if(e)e.value=''});listKinds.forEach(k=>state[k]=[]);state.template='modern';state.accent='#2a7bff';state.accentGradient='linear-gradient(135deg,#2a7bff,#65a7ff)';state.photo='';const img=$('#cvPhotoPreview');if(img){img.removeAttribute('src');img.style.display='none'};const ph=$('#cvPhotoPlaceholder');if(ph)ph.style.display='';listKinds.forEach(renderEditor);if($('#cvbAccent'))$('#cvbAccent').value=state.accent;$$('.cvb-color-swatch').forEach((b,i)=>b.classList.toggle('is-active',i===0));$$('.cvb-template-btn').forEach(b=>b.classList.toggle('is-active',b.dataset.template==='modern'));if($('#photo'))$('#photo').value='';const pfn=$('#cvbPhotoFileName');if(pfn)pfn.textContent=I.photo_empty||'Ninguna foto seleccionada';renderAll()}
$$('[data-bind]').forEach(e=>e.addEventListener('input',renderAll));$$('[data-add]').forEach(b=>b.addEventListener('click',()=>add(b.dataset.add)));$$('.cvb-template-btn').forEach(b=>b.addEventListener('click',()=>{state.template=b.dataset.template;$$('.cvb-template-btn').forEach(x=>x.classList.toggle('is-active',x===b));renderAll()}));
$$('.cvb-color-swatch').forEach(b=>b.addEventListener('click',()=>{state.accent=b.dataset.accent||'#2a7bff';state.accentGradient=b.dataset.gradient||state.accent;$$('.cvb-color-swatch').forEach(x=>x.classList.toggle('is-active',x===b));if($('#cvbAccent'))$('#cvbAccent').value=state.accent;renderAll()}));$('#cvbAccent')?.addEventListener('input',e=>{state.accent=e.target.value;state.accentGradient=e.target.value;$$('.cvb-color-swatch').forEach(x=>x.classList.remove('is-active'));renderAll()});
$('#photo')?.addEventListener('change',e=>{const f=e.target.files?.[0],nameEl=$('#cvbPhotoFileName');if(nameEl)nameEl.textContent=f?f.name:(I.photo_empty||'Ninguna foto seleccionada');if(!f||!f.type.startsWith('image/'))return;const r=new FileReader();r.onload=()=>{state.photo=r.result;const img=$('#cvPhotoPreview');img.src=state.photo;img.style.display='block';$('#cvPhotoPlaceholder').style.display='none';renderAll()};r.readAsDataURL(f)});
async function exportCv(){
  if(!hasMeaningfulCv())return;
  const format=$('#cvbExportFormat')?.value||'pdf';
  const btn=$('#cvbDownload');
  if(btn)btn.disabled=true;
  try{
    const locale=document.documentElement.lang==='pt-BR'?'pt-br':document.documentElement.lang.split('-')[0];
    const endpoint=format==='pdf'?'/api/cv/export-pdf':'/api/cv/export-docx';
    const r=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cv:currentCv(),photo:state.photo,accent:state.accent,template:state.template,locale})});
    if(!r.ok)throw new Error(format==='pdf'?'No se pudo generar el archivo PDF.':'No se pudo generar el archivo Word.');
    const blob=await r.blob(),url=URL.createObjectURL(blob),a=document.createElement('a');
    const disposition=r.headers.get('Content-Disposition')||'',match=disposition.match(/filename="?([^";]+)"?/i);
    a.href=url;a.download=match?decodeURIComponent(match[1]):(`CV_Converti.${format==='pdf'?'pdf':'docx'}`);document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),2500);
  }catch(err){alert(err.message||'No se pudo generar el archivo Word.')}finally{if(btn)btn.disabled=false}
}
$('#cvbDownload')?.addEventListener('click',exportCv);
$('#cvbClear')?.addEventListener('click',()=>{if(confirm(I.clear_confirm||'¿Limpiar el CV?')){resetDraft();closeAssistant()}});
$('#cvbLang')?.addEventListener('change',e=>location.href=e.target.value);

const navCreate=$('#cvbNavCreate');
navCreate?.addEventListener('click',e=>{
  try{
    const target=new URL(navCreate.href,location.href);
    if(target.pathname===location.pathname){
      e.preventDefault();
      history.replaceState(null,'',location.pathname);
      window.scrollTo({top:0,behavior:'smooth'});
    }
  }catch(_){}
});

let importPreviewUrl='';
const assistantMeta={import:[I.flow_import_title||I.ai_import,I.flow_import_text||''],text:[I.flow_text_title||I.ai_paste,I.flow_text_text||''],computrabajo:[I.compu_title||'CompuTrabajo',I.compu_text||''],email:[I.email_title||'Correo de postulación',I.email_context||'']};let activeImportAction='import_and_improve';
function openAssistant(name){const panel=$('#cvbAiPanel');if(!panel)return;panel.hidden=false;const panelName=name==='computrabajo'?'import':name;activeImportAction=name==='computrabajo'?'computrabajo_import':'import_and_improve';$$('[data-assistant]').forEach(b=>b.classList.toggle('is-active',b.dataset.assistant===name));$$('[data-assistant-panel]').forEach(p=>p.hidden=p.dataset.assistantPanel!==panelName);$('#cvbAssistantTitle').textContent=(assistantMeta[name]||assistantMeta.import)[0];$('#cvbAssistantSubtitle').textContent=(assistantMeta[name]||assistantMeta.import)[1];panel.dataset.mode=name;const editor=$('.cvb-editor');if(editor)editor.scrollTo({top:0,behavior:'smooth'})}
$$('[data-assistant]').forEach(b=>b.addEventListener('click',()=>openAssistant(b.dataset.assistant)));$('#cvbAssistantClose')?.addEventListener('click',closeAssistant);$('#cvbStartManual')?.addEventListener('click',()=>{resetDraft();closeAssistant();$('[data-bind="name"]')?.focus()});
function currentCv(){return{name:val('name'),title:val('title'),email:val('email'),phone:val('phone'),city:val('city'),website:val('website'),profile:val('profile'),experience:state.experience,education:state.education,skills:state.skills,languages:state.languages,certifications:state.certifications}}
function hasMeaningfulCv(){
  const fields=['name','title','email','phone','city','website','profile'];
  if(fields.some(k=>val(k)))return true;
  if(state.photo)return true;
  return listKinds.some(k=>state[k].some(item=>Object.values(item||{}).some(v=>String(v||'').trim())));
}
function syncExportAvailability(){
  const control=$('#cvbExportControl'),btn=$('#cvbDownload');
  const ready=hasMeaningfulCv();
  if(control)control.hidden=!ready;
  if(btn)btn.disabled=!ready;
}

function setField(key,value){const e=$(`[data-bind="${key}"]`);if(e)e.value=value||''}
function applyCv(data){if(!data||typeof data!=='object')return;['name','title','email','phone','city','website','profile'].forEach(k=>setField(k,data[k]));listKinds.forEach(k=>{if(Array.isArray(data[k]))state[k]=(k==='skills'?data[k].slice(0,8):data[k]);renderEditor(k)});renderAll()}
const aiStatus=$('#cvbAiStatus');
function setAiMessage(text,kind=''){if(!aiStatus)return;aiStatus.textContent=text||'';aiStatus.className=`cvb-ai-status ${kind?`is-${kind}`:''}`}
function setAiBusy(busy){$$('#cvbAiPanel button,.cvb-inline-ai,#cvbAiCurrent,#cvbAiAts').forEach(b=>b.disabled=busy)}
async function runAi(action,{useImport=false}={}){const file=$('#cvbAiFile')?.files?.[0],text=$('#cvbAiText')?.value?.trim()||'';if(useImport&&!file&&!text){setAiMessage(I.ai_need_content||'Sube o pega contenido primero.','error');return}setAiBusy(true);setAiMessage(useImport?(I.ai_extracting||'Leyendo CV…'):(I.ai_processing||'Mejorando CV…'),'loading');try{let r;if(useImport){const fd=new FormData();fd.append('action',action);fd.append('locale',document.documentElement.lang==='pt-BR'?'pt-br':document.documentElement.lang.split('-')[0]);fd.append('current',JSON.stringify(currentCv()));if(text)fd.append('text',text);if(file)fd.append('file',file);r=await fetch('/api/cv/ai',{method:'POST',body:fd})}else{r=await fetch('/api/cv/ai',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action,locale:document.documentElement.lang==='pt-BR'?'pt-br':document.documentElement.lang.split('-')[0],current:currentCv(),text})})}const d=await r.json().catch(()=>({}));if(!r.ok||!d.ok){throw new Error(d.message||I.ai_unavailable||'IA no disponible.')}applyCv(d.cv);setAiMessage(I.ai_done||'Listo. Revisa el resultado.','success');closeAssistant();$('.cvb-editor')?.scrollTo({top:0,behavior:'smooth'})}catch(err){setAiMessage(err.message||I.ai_unavailable||'IA no disponible.','error')}finally{setAiBusy(false)}}
$('#cvbAiFile')?.addEventListener('change',e=>{const f=e.target.files?.[0],nameEl=$('#cvbAiFileName'),frame=$('#cvbImportPdfPreview'),empty=$('#cvbImportPreviewEmpty');if(nameEl)nameEl.textContent=f?f.name:'';if(!frame||!empty)return;if(importPreviewUrl){URL.revokeObjectURL(importPreviewUrl);importPreviewUrl=''}if(f&&f.type==='application/pdf'){importPreviewUrl=URL.createObjectURL(f);frame.src=importPreviewUrl;frame.style.display='block';empty.style.display='none'}else{frame.removeAttribute('src');frame.style.display='none';empty.style.display='grid';if(f)empty.textContent=f.name+' · DOCX'}});

async function generateApplicationEmail(){
  const context=$('#cvbEmailContext')?.value.trim()||'';
  if(!context){setAiMessage(I.email_context||'Indica el puesto o pega la oferta.','error');return}
  setAiBusy(true);setAiMessage(I.ai_processing||'Generando…','loading');
  try{
    const locale=document.documentElement.lang==='pt-BR'?'pt-br':document.documentElement.lang.split('-')[0];
    const r=await fetch('/api/cv/application-email',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({locale,cv:currentCv(),context})});
    const d=await r.json().catch(()=>({}));
    
    if(!r.ok||!d.ok)throw new Error(d.message||I.ai_unavailable||'IA no disponible.');
    $('#cvbEmailSubject').value=d.email?.subject||'';
    $('#cvbEmailBody').value=d.email?.body||'';
    $('#cvbEmailResult').hidden=false;
    setAiMessage(I.ai_done||'Listo. Revisa el resultado.','success');
  }catch(err){setAiMessage(err.message||I.ai_unavailable||'IA no disponible.','error')}
  finally{setAiBusy(false)}
}
$('#cvbEmailGenerate')?.addEventListener('click',generateApplicationEmail);
$('#cvbEmailCopy')?.addEventListener('click',async()=>{
  const subject=$('#cvbEmailSubject')?.value||'',body=$('#cvbEmailBody')?.value||'';
  try{await navigator.clipboard.writeText(`${subject}\n\n${body}`)}catch(_){}
});

$('#cvbAiImport')?.addEventListener('click',()=>runAi(activeImportAction,{useImport:true}));$('#cvbAiTextBuild')?.addEventListener('click',()=>runAi('import_and_improve',{useImport:true}));$('#cvbAiCurrent')?.addEventListener('click',()=>runAi('ultra_improve'));$('#cvbAiAts')?.addEventListener('click',()=>runAi('ats'));$$('.cvb-inline-ai').forEach(b=>b.addEventListener('click',()=>runAi(b.dataset.aiAction||'ultra_improve')));
function updateExportLabel(){const span=$('#cvbDownload span'),fmt=$('#cvbExportFormat')?.value||'pdf';if(span)span.textContent=`${I.download||'Descargar'} ${fmt==='docx'?'Word':'PDF'}`}
$('#cvbExportFormat')?.addEventListener('change',updateExportLabel);updateExportLabel();
let parallaxQueued=false;function updateParallax(){parallaxQueued=false;const y=Math.min(180,window.scrollY*.08);$$('.cvb-side-art').forEach((el,i)=>el.style.setProperty('--parallax-y',`${i?y:-y}px`))}
window.addEventListener('scroll',()=>{if(!parallaxQueued){parallaxQueued=true;requestAnimationFrame(updateParallax)}},{passive:true});updateParallax();
resetDraft();

function fitPreview(){
  const shell=$('#cvbPageShell'),stage=$('#cvbPageStage');
  if(!shell||!stage||!page)return;
  page.style.transform='none';
  const baseW=page.offsetWidth||794,baseH=page.offsetHeight||1123;
  const availableW=Math.max(260,shell.clientWidth-20),availableH=Math.max(420,shell.clientHeight-20);
  const scale=Math.min(1,availableW/baseW,availableH/baseH);
  stage.style.width=`${Math.round(baseW*scale)}px`;
  stage.style.height=`${Math.round(baseH*scale)}px`;
  page.style.transform=`scale(${scale})`;
}
const previewRO=window.ResizeObserver?new ResizeObserver(()=>requestAnimationFrame(fitPreview)):null;
if(previewRO&&$('#cvbPageShell'))previewRO.observe($('#cvbPageShell'));
window.addEventListener('resize',()=>requestAnimationFrame(fitPreview),{passive:true});
requestAnimationFrame(fitPreview);

})();