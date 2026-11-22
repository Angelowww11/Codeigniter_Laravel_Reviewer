window.GuidedStudy = (() => {
  'use strict';
  const lessons=window.GUIDED_LESSONS,lookup=Object.fromEntries(lessons.map(l=>[l.id,l]));
  const key='framework-party-guided-v1';
  let root,actions,reader=false,filter='all',dueQueue=[],feedback='',storageAvailable=true;
  function empty(){return {current:lessons[0].id,step:0,attempts:{},reviews:{},scheduled:{},baseStages:{}};}
  function clean(raw){
    const s=empty();if(!raw||typeof raw!=='object')return s;
    if(Object.hasOwn(lookup,raw.current))s.current=raw.current;
    if([0,1,2].includes(raw.step))s.step=raw.step;
    for(const id of Object.keys(lookup)){
      s.scheduled[id]=raw.scheduled?.[id]===true;
      s.baseStages[id]=Number.isInteger(raw.baseStages?.[id])?Math.max(0,Math.min(5,raw.baseStages[id])):0;
      const a=raw.attempts?.[id];
      if(Array.isArray(a))s.attempts[id]=Array.from({length:3},(_,i)=>({text:typeof a[i]?.text==='string'?a[i].text.slice(0,5000):'',revealed:!!a[i]?.revealed,grade:typeof a[i]?.grade==='boolean'?a[i].grade:null}));
      const r=raw.reviews?.[id];
      if(r&&Number.isFinite(r.due)&&Number.isFinite(r.last)&&Number.isInteger(r.streak)&&r.streak>=0&&['again','good','easy'].includes(r.rating))s.reviews[id]={due:r.due,last:r.last,streak:Math.min(5,r.streak),rating:r.rating};
    }
    return s;
  }
  let state;
  try{state=clean(JSON.parse(localStorage.getItem(key)||'null'));}catch{state=empty();}
  function save(){try{localStorage.setItem(key,JSON.stringify(state));}catch{storageAvailable=false;}}
  function e(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  function attempt(id){if(!state.attempts[id]){state.baseStages[id]=state.reviews[id]?.streak||0;state.attempts[id]=Array.from({length:3},()=>({text:'',revealed:false,grade:null}));}return state.attempts[id];}
  function due(){return lessons.filter(l=>state.reviews[l.id]?.due<=Date.now()).sort((a,b)=>state.reviews[a.id].due-state.reviews[b.id].due);}
  function dueLabel(r){if(!r)return 'Not reviewed yet';if(r.due<=Date.now())return 'Ready for review';return 'Review '+new Date(r.due).toLocaleDateString(undefined,{timeZone:'Asia/Manila',month:'short',day:'numeric'});}
  function tabs(){return '<div class="learning-versions" role="group" aria-label="Study material versions"><button class="secondary" data-page="materials">▤ Original slides</button><button class="primary blue" aria-current="page" data-page="guided">✳ Guided study</button></div>';}
  function render(target,callbacks){root=target;actions=callbacks;draw();}
  function draw(){if(!root)return;reader?lessonView():library();}
  function open(id,recallOnly=false){
    if(!Object.hasOwn(lookup,id))return;
    state.current=id;state.step=recallOnly?2:0;reader=true;feedback='';
    if(recallOnly){state.attempts[id]=Array.from({length:3},()=>({text:'',revealed:false,grade:null}));state.scheduled[id]=false;state.baseStages[id]=state.reviews[id]?.streak||0;}
    save();draw();window.scrollTo({top:0,behavior:'instant'});root.focus({preventScroll:true});
  }
  function library(){
    if(filter==='all')filter=String(lookup[state.current].module);
    const shown=lessons.filter(l=>l.module===Number(filter)),m=window.STUDY_DATA.modules[Number(filter)-1],dueList=due();
    root.innerHTML=`<div class="quiet-library"><span class="eyebrow">YOUR COMPLETE STUDY MATERIAL</span><h1 class="page-title">Choose one lesson.</h1><p class="page-intro">All explanations, examples, and recall checks are still here. Focus on one module at a time.</p><label class="quiet-module-picker" for="guided-module">Module<select id="guided-module">${window.STUDY_DATA.modules.map(m=>`<option value="${m.id}" ${String(m.id)===filter?'selected':''}>M${m.id} · ${e(m.title)}</option>`).join('')}</select></label><section class="guided-module"><div class="guided-module-title"><span>M${m.id}</span><div><h2>${e(m.title)}</h2><p>${shown.length} lessons · ${m.framework}</p></div></div><div class="guided-lesson-list">${shown.map(l=>`<button data-g-open="${l.id}" class="guided-lesson-link"><span class="lesson-index">${l.topic+1}</span><span class="guided-link-text"><strong>${e(l.title)}</strong><small>${e(l.idea)}</small></span><span class="review-status">${e(dueLabel(state.reviews[l.id]))} →</span></button>`).join('')}</div></section>${dueList.length?`<details class="quiet-details"><summary>Reviews ready (${dueList.length})</summary><p>Start with recall before rereading.</p><button class="secondary" data-g-review>Review due topics →</button></details>`:''}<details class="quiet-details"><summary>References and more</summary><div class="button-row"><button class="text-button" data-page="notes">Quick reference notes →</button><button class="text-button" data-page="materials">Original slides →</button><button class="text-button" data-g-resume>Resume last lesson →</button></div></details>${!storageAvailable?'<p class="notice">Browser storage is unavailable. Keep this page open to retain progress for this visit.</p>':''}</div>`;
  }
  function lessonView(){
    const l=lookup[state.current],m=window.STUDY_DATA.modules[l.module-1],a=attempt(l.id),review=state.reviews[l.id];
    const ownLessons=lessons.filter(x=>x.module===l.module),index=lessons.indexOf(l);
    root.innerHTML=`<div class="guided-reader-top"><button class="text-button" data-g-library>← Guided course</button><span>${e(dueLabel(review))}</span></div><div class="guided-lesson-heading"><span class="eyebrow">M${l.module} · ${e(m.framework.toUpperCase())} · LESSON ${l.topic+1}/${ownLessons.length}</span><h1>${e(l.title)}</h1><p>${e(l.idea)}</p></div><div class="guided-reader"><details class="guided-contents quiet-details"><summary>Other lessons in this module</summary><span class="eyebrow">THIS MODULE</span>${ownLessons.map(x=>`<button class="lesson-topic ${x.id===l.id?'active':''}" data-g-open="${x.id}" ${x.id===l.id?'aria-current="step"':''}><span>${x.topic+1}. ${e(x.title)}</span><small>${e(dueLabel(state.reviews[x.id]))}</small></button>`).join('')}<button class="secondary" data-g-original="${l.id}">See original slides ↗</button><button class="text-button" data-g-practice="${l.module}">Practice M${l.module} →</button></details><div class="guided-body"><div class="guided-step-nav" role="tablist" aria-label="Lesson steps">${['Understand','Worked example','Recall'].map((name,i)=>`<button role="tab" id="guided-tab-${i}" aria-controls="guided-step-panel" aria-selected="${state.step===i}" tabindex="${state.step===i?'0':'-1'}" class="${state.step===i?'active':''}" data-g-step="${i}"><b>${i+1}</b><span>${name}</span></button>`).join('')}</div><section id="guided-step-panel" role="tabpanel" aria-labelledby="guided-tab-${state.step}" tabindex="0">${state.step===0?understand(l):state.step===1?worked(l):recall(l,a)}</section><details class="guided-source quiet-details"><summary>Original slides and references</summary><span>Based on M${l.module}, pages ${l.range[0]}–${l.range[1]} · Example rewritten for practice</span><button class="text-button" data-g-original="${l.id}">Compare with the original →</button></details><div class="guided-lesson-navigation">${index>0?`<button class="secondary" data-g-open="${lessons[index-1].id}">← Previous lesson</button>`:'<span></span>'}${index<lessons.length-1?`<button class="secondary" data-g-open="${lessons[index+1].id}">Next lesson →</button>`:'<button class="secondary" data-g-library>Back to the course →</button>'}</div></div></div>`;
  }
  function understand(l){return `<article class="guided-paper"><span class="eyebrow">STEP 1 · MAKE SENSE OF IT</span><h2>The idea in small pieces.</h2><ol class="guided-chunks">${l.steps.map((step,i)=>`<li><span>${i+1}</span><p>${e(step)}</p></li>`).join('')}</ol><div class="guided-flow" role="group" aria-label="Concept flow">${l.flow.map((v,i)=>`${i?'<span class="flow-arrow" aria-hidden="true">→</span>':''}<span class="flow-node">${e(v)}</span>`).join('')}</div><aside class="memory-cue"><span aria-hidden="true">✳</span><div><strong>A cue to remember</strong><p>${e(l.memory)}</p></div></aside><div class="guided-step-footer"><span>Explain the idea in your own words before moving on.</span><button class="primary blue" data-g-step="1">See it in an example →</button></div></article>`;}
  function worked(l){return `<article class="guided-paper"><span class="eyebrow">STEP 2 · FOLLOW THE REASONING</span><h2>A focused example.</h2><p>${e(l.scenario)}</p><div class="guided-code-head"><span>Learning fragment · surrounding module setup assumed</span><button data-g-copy class="text-button">Copy example</button></div><pre class="guided-code"><code>${e(l.code)}</code></pre><h3>Read it this way</h3><ol class="guided-trace">${l.trace.map(line=>`<li>${e(line)}</li>`).join('')}</ol><aside class="guided-trap"><strong>Easy to mix up</strong><p>${e(l.trap)}</p></aside><div class="guided-step-footer"><button class="text-button" data-g-step="0">← Back to the idea</button><button class="primary blue" data-g-step="2">Try it from memory →</button></div></article>`;}
  function recall(l,a){
    const graded=a.filter(x=>x.grade!==null).length,remembered=a.filter(x=>x.grade===true).length;
    const intervals=[1,3,7,14,30],streak=state.baseStages[l.id]||0,days=intervals[Math.min(streak,4)],easyDays=intervals[Math.min(streak+1,4)];
    return `<article class="guided-paper"><span class="eyebrow">STEP 3 · CLOSE THE NOTES IN YOUR HEAD</span><h2>What can you recall?</h2><p>Answer in your own words before revealing the model answer. Compare the meaning, then assess yourself. Your writing is saved here as a draft.</p><div class="guided-recall-count" aria-live="polite">${graded}/3 checks assessed${graded?' · '+remembered+' you remembered':''}</div>${l.checks.map((c,i)=>`<section class="guided-check"><label for="guided-answer-${i}"><span>CHECK ${i+1}</span><strong>${e(c.q)}</strong></label><textarea id="guided-answer-${i}" data-g-draft="${i}" placeholder="Try an answer before looking…" rows="3">${e(a[i].text)}</textarea>${a[i].revealed?`<div class="guided-model-answer"><span class="eyebrow">COMPARE YOUR ANSWER</span><p>${e(c.a)}</p><div class="guided-assess" role="group" aria-label="Assess recall check ${i+1}"><button class="${a[i].grade===true?'primary blue':'secondary'}" data-g-grade="true" data-g-check="${i}" aria-pressed="${a[i].grade===true}">I remembered ✓</button><button class="${a[i].grade===false?'primary':'secondary'}" data-g-grade="false" data-g-check="${i}" aria-pressed="${a[i].grade===false}">Needs another look ↻</button></div></div>`:`<button class="secondary" data-g-reveal="${i}">Reveal model answer</button>`}</section>`).join('')}<section class="guided-schedule"><span class="eyebrow">SPACED REVIEW · SELF-ASSESSED</span><h3>When should this come back?</h3><p>${graded===3?'Choose how the whole lesson felt. Again gives you a short retry; Good and Easy leave more time before the next recall.':'Reveal and assess all three checks to schedule your next review.'}</p><div class="review-rating"><button data-g-rate="again" ${graded<3||state.scheduled[l.id]?'disabled':''}><strong>Again</strong><span>In 10 minutes</span></button><button data-g-rate="good" ${graded<3||state.scheduled[l.id]?'disabled':''}><strong>Good</strong><span>In ${days} day${days===1?'':'s'}</span></button><button data-g-rate="easy" ${graded<3||state.scheduled[l.id]?'disabled':''}><strong>Easy</strong><span>In ${easyDays} days</span></button></div><p class="small muted">Review dates appear in this app when you return. These ratings track your own recall, not a guarantee of mastery.</p>${feedback?`<div class="notice" role="status">${e(feedback)}</div>`:''}${feedback&&dueQueue.length?'<button class="primary blue" data-g-next-due>Next due topic →</button>':''}${feedback||state.scheduled[l.id]?`<button class="secondary" data-g-retry="${l.id}">Try these checks again</button>`:''}</section></article>`;
  }
  document.addEventListener('click',async event=>{
    const b=event.target.closest('button');if(!b||b.disabled||!root?.isConnected)return;
    if(b.dataset.gOpen){dueQueue=[];open(b.dataset.gOpen);return;}
    if(b.hasAttribute('data-g-resume')){reader=true;feedback='';draw();window.scrollTo({top:0,behavior:'instant'});return;}
    if(b.hasAttribute('data-g-library')){reader=false;feedback='';draw();window.scrollTo({top:0,behavior:'instant'});return;}
    if(b.hasAttribute('data-g-step')){state.step=Number(b.dataset.gStep);feedback='';save();draw();document.querySelector('.guided-step-nav').scrollIntoView({block:'start'});document.querySelector(`#guided-tab-${state.step}`).focus({preventScroll:true});return;}
    if(b.hasAttribute('data-g-original')){actions.openOriginal(lookup[b.dataset.gOriginal]);return;}
    if(b.hasAttribute('data-g-practice')){actions.practice(Number(b.dataset.gPractice));return;}
    if(b.hasAttribute('data-g-reveal')){const y=scrollY,i=Number(b.dataset.gReveal);attempt(state.current)[i].revealed=true;save();draw();window.scrollTo({top:y,behavior:'instant'});document.querySelector(`[data-g-check="${i}"]`).focus({preventScroll:true});return;}
    if(b.hasAttribute('data-g-grade')){const y=scrollY,i=Number(b.dataset.gCheck);attempt(state.current)[i].grade=b.dataset.gGrade==='true';state.scheduled[state.current]=false;feedback='';save();draw();window.scrollTo({top:y,behavior:'instant'});document.querySelector(`[data-g-check="${i}"][data-g-grade="${b.dataset.gGrade}"]`).focus({preventScroll:true});return;}
    if(b.hasAttribute('data-g-rate')){
      if(attempt(state.current).some(a=>a.grade===null)||state.scheduled[state.current])return;
      const rating=b.dataset.gRate,intervals=[1,3,7,14,30],stage=state.baseStages[state.current]||0;
      const days=rating==='again'?0:intervals[Math.min(stage+(rating==='easy'?1:0),4)];
      state.reviews[state.current]={last:Date.now(),due:Date.now()+(rating==='again'?600000:days*86400000),streak:rating==='again'?0:Math.min(5,stage+1),rating};
      state.scheduled[state.current]=true;
      feedback=`Saved. This lesson returns to your review list ${rating==='again'?'in 10 minutes':`in ${days} day${days===1?'':'s'}`}.`;
      save();const y=scrollY;draw();window.scrollTo({top:y,behavior:'instant'});return;
    }
    if(b.hasAttribute('data-g-review')){dueQueue=due().map(l=>l.id);if(dueQueue.length)open(dueQueue.shift(),true);return;}
    if(b.hasAttribute('data-g-next-due')){if(dueQueue.length)open(dueQueue.shift(),true);return;}
    if(b.dataset.gRetry){if(confirm('Start a fresh recall attempt for this lesson? Its review schedule will stay.'))open(b.dataset.gRetry,true);return;}
    if(b.hasAttribute('data-g-copy')){
      try{await navigator.clipboard.writeText(lookup[state.current].code);b.textContent='Copied ✓';}catch{b.textContent='Select the example to copy';}return;
    }
  });
  document.addEventListener('input',event=>{if(event.target.hasAttribute('data-g-draft')){attempt(state.current)[Number(event.target.dataset.gDraft)].text=event.target.value.slice(0,5000);save();}});
  document.addEventListener('change',event=>{if(event.target.id==='guided-module'){filter=event.target.value;library();}});
  document.addEventListener('keydown',event=>{
    const tab=event.target.closest('[data-g-step][role="tab"]');if(!tab||!['ArrowRight','ArrowLeft','Home','End'].includes(event.key))return;
    event.preventDefault();const i=Number(tab.dataset.gStep);state.step=event.key==='Home'?0:event.key==='End'?2:(i+(event.key==='ArrowRight'?1:2))%3;save();draw();document.querySelector(`#guided-tab-${state.step}`).focus();
  });
  return {render,exportProgress:()=>JSON.parse(JSON.stringify(state)),importProgress:raw=>{state=clean(raw);reader=false;save();},reset:()=>{state=empty();reader=false;dueQueue=[];save();}};
})();
