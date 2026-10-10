(() => {
'use strict';
const $ = (s) => document.querySelector(s);
const menu = $('.menu-toggle');
menu?.addEventListener('click', () => {const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); menu.setAttribute('aria-label',open?'Close navigation':'Open navigation'); $('.site-nav').classList.toggle('open',open);});
const chat = $('.chat-toggle'), panel = $('.chat-panel');
const setChat = open => {panel.hidden = !open; chat.setAttribute('aria-expanded', String(open));};
chat?.addEventListener('click', () => setChat(panel.hidden)); $('.chat-close')?.addEventListener('click',()=>setChat(false));
let photos=[],photoIndex=0;
const dialog=$('#lightbox');
const showPhoto=()=> {const current=photos[photoIndex]; $('#lightbox-image').src=current.src; $('#lightbox-image').alt=current.caption; $('#lightbox-caption').textContent=current.caption; $('.lightbox-prev').hidden=$('.lightbox-next').hidden=photos.length<2;};
const openPhotos=(items,index=0)=>{photos=items;photoIndex=index;showPhoto();dialog.showModal();};
const movePhoto=step=>{photoIndex=(photoIndex+step+photos.length)%photos.length;showPhoto();};
$('.lightbox-close')?.addEventListener('click',()=>dialog.close()); $('.lightbox-prev')?.addEventListener('click',()=>movePhoto(-1)); $('.lightbox-next')?.addEventListener('click',()=>movePhoto(1));
dialog?.addEventListener('click',event=>{if(event.target===dialog)dialog.close();}); dialog?.addEventListener('keydown',event=>{if(event.key==='ArrowLeft')movePhoto(-1);if(event.key==='ArrowRight')movePhoto(1);});
document.querySelectorAll('[data-photo]').forEach(button=>button.addEventListener('click',()=>openPhotos([{src:button.dataset.photo,caption:button.dataset.caption||''}])));
const slides=window.NYS_DATA?.slides||[];let slideIndex=0;
const updateSlide=()=>{const image=$('.slide-image img');image.src=slides[slideIndex];image.alt=`Noble Youth Society photo ${slideIndex+1} of ${slides.length}`;$('.slide-counter').textContent=`${slideIndex+1}/${slides.length}`;};
const moveSlide=step=>{slideIndex=(slideIndex+step+slides.length)%slides.length;updateSlide();};
$('.slide-prev')?.addEventListener('click',()=>moveSlide(-1));$('.slide-next')?.addEventListener('click',()=>moveSlide(1));$('.slide-image')?.addEventListener('click',()=>openPhotos(slides.map((src,i)=>({src,caption:`Noble Youth Society photo ${i+1} of ${slides.length}`})),slideIndex));
let touchX=0;$('.slideshow')?.addEventListener('touchstart',event=>{touchX=event.changedTouches[0].clientX;},{passive:true});$('.slideshow')?.addEventListener('touchend',event=>{const distance=event.changedTouches[0].clientX-touchX;if(Math.abs(distance)>50)moveSlide(distance>0?-1:1);},{passive:true});
const form=$('#contact-form');let message='';
form?.addEventListener('submit',event=>{event.preventDefault();const values=Object.fromEntries(new FormData(form));message=`Name: ${values.name}\nEmail: ${values.email}\nPhone: ${values.phone}\nAddress: ${values.address}\nSubject: ${values.subject}\n\n${values.message}`;$('#message-preview').textContent=message;$('#email-draft').href=`mailto:nobleyouthsociety@gmail.com?subject=${encodeURIComponent(values.subject||'NYS website inquiry')}&body=${encodeURIComponent(message)}`;$('#copy-status').textContent='';$('#message-dialog').showModal();});
$('.message-close')?.addEventListener('click',()=>$('#message-dialog').close());$('#copy-message')?.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(message);$('#copy-status').textContent='Copied. Paste it into your email app to send.';}catch{$('#copy-status').textContent='Select and copy the message above.';}});
const searchForm=$('#search-form');
const search=()=>{const query=$('#search-input').value.trim().toLowerCase();const terms=query.split(/\s+/).filter(Boolean);const results=terms.length?(window.NYS_DATA?.search||[]).filter(item=>terms.every(term=>(item.title+' '+item.text).toLowerCase().includes(term))):[];const container=$('#search-results');container.replaceChildren();$('#search-summary').textContent=query?`${results.length} result${results.length===1?'':'s'} for “${query}”`:'Enter a word or phrase to search.';for(const item of results){const article=document.createElement('article');article.className='search-result';const heading=document.createElement('h2');const link=document.createElement('a');link.href=item.url;link.textContent=item.title;heading.append(link);const p=document.createElement('p');const start=Math.max(0,item.text.toLowerCase().indexOf(terms[0])-80);p.textContent=item.text.slice(start,start+320)+'…';article.append(heading,p);container.append(article);}};
if(searchForm){$('#search-input').value=new URLSearchParams(location.search).get('q')||'';searchForm.addEventListener('submit',event=>{event.preventDefault();search();});search();}
})();
