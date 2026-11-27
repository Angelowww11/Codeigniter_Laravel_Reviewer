/* A local study app. No accounts, remote services, or submitted study data. */
(() => {
  'use strict';
  const {modules, questions} = window.STUDY_DATA;
  const byId = Object.fromEntries(questions.map(q => [q.id, q]));
  const KEY = 'framework-party-it0049-v1';
  const main = document.querySelector('main');
  const modes = {
    quiz: {title:'Practice quiz',icon:'✳',description:'Pick an answer. Get the explanation right away.',foot:'Multiple choice'},
    recall: {title:'Type it out',icon:'⌨',description:'Recall the answer before you reveal it. Grade yourself.',foot:'Active recall · self-graded'},
    flash: {title:'Flip the cards',icon:'▱',description:'A quick question on the front. The answer on the back.',foot:'Flashcards · self-graded'},
    loop: {title:'Training loop',icon:'↻',description:'Work through missed questions. Retry until they stick.',foot:'Your missed questions'},
    exam: {title:'Exam rehearsal',icon:'◷',description:'One minute per question. Review answers at the end.',foot:'Timed · no hints'},
    path: {title:'Practice path',icon:'⇢',description:'Work through the deck in module order. Save and resume.',foot:'All selected questions'}
  };
  let storageWorks = true;
  function initial(){ return {selected:modules.map(m=>m.id),records:{},stars:[],history:[],session:null,count:20,study:{module:1,page:6,read:[],bookmarks:[]}}; }
  function validStudy(value){
    const s=value&&typeof value==='object'?value:{};
    const validKey=k=>typeof k==='string'&&/^m[1-8]p\d+$/.test(k)&&Number(k.split('p')[1])>=1&&Number(k.split('p')[1])<=modules[Number(k[1])-1].pages;
    const module=modules.some(m=>m.id===s.module)?s.module:1;
    return {module,page:Number.isInteger(s.page)?Math.max(1,Math.min(modules[module-1].pages,s.page)):6,read:[...new Set((Array.isArray(s.read)?s.read:[]).filter(validKey))],bookmarks:[...new Set((Array.isArray(s.bookmarks)?s.bookmarks:[]).filter(validKey))]};
  }
  function readStore(){
    try {
      const raw=JSON.parse(localStorage.getItem(KEY)||'null');
      if(!raw || typeof raw!=='object')return initial();
      const s={...initial(),...raw};
      s.selected=Array.isArray(s.selected)?s.selected.filter(id=>modules.some(m=>m.id===id)):initial().selected;
      s.stars=Array.isArray(s.stars)?s.stars.filter(id=>byId[id]):[];
      s.records=s.records&&typeof s.records==='object'?s.records:{};
      s.study=validStudy(s.study);
      s.history=Array.isArray(s.history)?s.history.slice(0,50):[];
      s.count=s.count==='all'?60:Math.max(1,Math.min(60,Math.floor(Number(s.count))||20));
      if(s.session && (!Array.isArray(s.session.queue) || !s.session.queue.length || s.session.queue.some(id=>!byId[id]) || !Number.isInteger(s.session.cursor) || !Array.isArray(s.session.answers) || !modes[s.session.mode]))s.session=null;
      return s;
    } catch { return initial(); }
  }
  let state=readStore(), page=['#materials','#guided','#practice','#progress','#bank','#notes'].includes(location.hash)?location.hash.slice(1):'home', bankPage=1, search='', bankStatus='all', notesModule='all',materialReader=false;
  let focusEnd=0, focusRemaining=25*60, toastTimer;
  function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch{if(storageWorks){storageWorks=false;toast('Storage is unavailable. Keep this page open to preserve this session.');}document.querySelector('.local-badge').textContent='Progress kept for this visit only';}}
  function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  const prose = value => window.StudyCode ? window.StudyCode.prose(value) : esc(value);
  function shuffle(a){const r=[...a];for(let i=r.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[r[i],r[j]]=[r[j],r[i]];}return r;}
  function selectedQuestions(){return questions.filter(q=>state.selected.includes(q.module));}
  function missed(pool=selectedQuestions()){return pool.filter(q=>state.records[q.id]?.lastCorrect===false);}
  function stats(pool=questions){const seen=pool.filter(q=>state.records[q.id]);const right=seen.filter(q=>state.records[q.id].lastCorrect);return {seen:seen.length,right:right.length,percent:seen.length?Math.round(right.length/seen.length*100):0};}
  function footer(){return '<footer class="footer"><span>Framework Party · Made for your IT0049 modules</span><span>Original practice questions · Study aid, not an official exam</span></footer>';}
  function source(q,label){const m=modules[q.module-1];return `<a class="source-link" href="modules/${encodeURIComponent(m.file)}#page=${q.page}" target="_blank" rel="noopener">${esc(label||`M${q.module} · PDF page ${q.page}`)} ↗</a>`;}
  function tag(q){return `<span class="tag ${q.module<5?'ci':'lv'}">M${q.module} · ${q.module<5?'CodeIgniter':'Laravel'}</span><span>${esc(q.topic)}</span>`;}
  function star(q){return `<button class="star" data-star="${q.id}" aria-label="${state.stars.includes(q.id)?'Unstar':'Star'} question" aria-pressed="${state.stars.includes(q.id)}">${state.stars.includes(q.id)?'★':'☆'}</button>`;}
  function toast(message){const el=document.querySelector('#toast');el.textContent=message;el.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.hidden=true,4500);}
  function sidebar(){
    document.querySelector('#module-select').innerHTML=modules.map((m,i)=>`${i===0||i===4?`<span class="module-group">${m.framework}</span>`:''}<label class="module-check ${state.selected.includes(m.id)?'checked':''}"><input type="checkbox" data-module="${m.id}" ${state.selected.includes(m.id)?'checked':''} aria-label="Include module ${m.id}: ${esc(m.title)}"><span><span class="module-mini">M${m.id}</span><span class="module-name">${esc(m.title.replace(/^CodeIgniter |^Laravel |^CI /,''))}</span></span></label>`).join('');
    document.querySelector('#select-all').textContent=state.selected.length===8?'Clear all':'Select all';
  }
  function navigate(to){
    if(page==='session' && state.session)save();
    page=to;bankPage=1;render();window.scrollTo({top:0,behavior:'instant'});main.focus({preventScroll:true});
    try{history.replaceState(null,'',location.pathname+location.search+(['materials','guided','practice','progress','bank','notes'].includes(to)?'#'+to:''));}catch{}
  }
  function render(){
    sidebar();
    document.body.classList.toggle('session-active',page==='session');document.body.dataset.page=page;document.querySelector('#more-menu')?.removeAttribute('open');
    document.querySelectorAll('nav [data-page]').forEach(b=>{b.classList.toggle('active',b.dataset.page===page);if(b.dataset.page===page)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');});
    if(page==='home')home();else if(page==='practice')practiceOptions();else if(page==='materials')materials();else if(page==='guided')window.GuidedStudy.render(main,{openOriginal:l=>openMaterial(l.module,l.page),practice:id=>{state.selected=[id];save();navigate('practice');}});else if(page==='bank')bank();else if(page==='notes')notes();else if(page==='progress')progress();else if(page==='session')sessionView();
  }
  function breadcrumb(right='Your next little level-up'){return `<div class="breadcrumb"><span>YOUR STUDY ROOM <span aria-hidden="true">/</span> IT0049</span><span>${right}</span></div>`;}
  function resumeBanner(){const s=state.session;return s?`<div class="resume-banner"><div><strong>You have a session in progress.</strong><p>${esc(modes[s.mode].title)} · ${s.cursor} answered · ${s.queue.length-s.cursor} remaining${s.mode==='exam'?' · timer keeps running':''}</p></div><button class="primary blue" data-resume>Resume →</button><button class="text-button" data-discard>Discard</button></div>`:'';}
  function home(){
    main.innerHTML=resumeBanner()+`<section class="quiet-home"><span class="eyebrow">IT0049 · YOUR STUDY SPACE</span><h1>One thing at a time.</h1><p>Your complete lessons are here. Choose what you need for this session.</p><div class="quiet-choices"><button class="quiet-choice" data-page="guided"><span class="eyebrow">LEARN AT YOUR PACE</span><h2>Study the lessons</h2><p>Choose a module, then work through one lesson.</p><span class="quiet-action">Continue studying →</span></button><button class="quiet-choice" data-page="practice"><span class="eyebrow">CHECK WHAT STICKS</span><h2>Practice</h2><p>Answer questions and see why each answer works.</p><span class="quiet-action">Set up practice →</span></button></div><p class="quiet-originals">Need your classroom materials? <button class="inline-link" data-page="materials">Open the original slides ↗</button></p></section>`+footer();
  }
  function modulePicker(){return `<label class="quiet-module-picker">Module<select id="practice-module"><option value="all" ${state.selected.length!==1?'selected':''}>All selected modules</option>${modules.map(m=>`<option value="${m.id}" ${state.selected.length===1&&state.selected[0]===m.id?'selected':''}>M${m.id} · ${esc(m.title)}</option>`).join('')}</select></label>`;}
  function practiceOptions(){
    const pool=selectedQuestions();
    main.innerHTML=resumeBanner()+`<section class="quiet-practice"><span class="eyebrow">PRACTICE</span><h1 class="page-title">A session that suits you.</h1><p class="page-intro">Choose a module and 1–60 questions. Each module has 60 questions, including 24 applied checks. Explain the decision, then compare the reasoning.</p><div class="quiet-settings">${modulePicker()}<label>Questions<select id="run-count">${Array.from({length:60},(_,i)=>i+1).map(n=>`<option value="${n}" ${String(state.count)===String(n)?'selected':''}>${n==='all'?'All selected':n}</option>`).join('')}</select></label></div><p class="small muted">${pool.length} questions available in your selection.</p><button class="primary blue" data-start="quiz" ${!pool.length?'disabled':''}>Start practice quiz →</button><details class="quiet-details"><summary>Other ways to practice</summary><div class="mode-grid">${Object.entries(modes).filter(([id])=>id!=='quiz').map(([id,m])=>`<button class="mode-card" data-start="${id}" ${!pool.length||id==='loop'&&!missed().length?'disabled':''}><span class="mode-symbol" aria-hidden="true">${m.icon}</span><h3>${m.title}</h3><p>${m.description}</p><span class="card-foot">${m.foot} ↗</span></button>`).join('')}</div><button class="text-button" data-page="bank">Browse the question bank →</button></details></section>`+footer();
  }
  function openMaterial(module,slide){
    state.study.module=Number(module);
    state.study.page=Math.max(1,Math.min(modules[Number(module)-1].pages,Number(slide)||1));
    materialReader=true;save();navigate('materials');
  }
  function materials(){
    const versions = '<div class="learning-versions" role="group" aria-label="Study material versions"><button class="primary blue" aria-current="page" data-page="materials">▤ Original slides</button><button class="secondary" data-page="guided">✳ Guided study</button></div>';
    if(!materialReader){
      const studied=state.study.read.length;
      main.innerHTML=versions+breadcrumb('Read the lesson. See the original slide.')+`<span class="eyebrow">YOUR FULL COURSE LIBRARY</span><h1 class="page-title">Your modules, explained.</h1><p class="page-intro">Read a topic guide, study the original slide screenshots, and follow the code at your own pace. All 300 pages of your eight modules are here.</p><div class="material-welcome"><div><span class="eyebrow">PICK UP WHERE YOU LEFT OFF</span><h2>M${state.study.module} · ${esc(modules[state.study.module-1].title)}</h2><p>Last opened: page ${state.study.page} · ${studied} of 300 pages marked studied</p></div><button class="primary" data-read-module="${state.study.module}" data-read-page="${state.study.page}">Continue reading →</button></div><p class="subtle">All eight modules are available here. The sidebar checkboxes choose your quiz material.</p><div class="materials-grid">${modules.map(m=>{const count=state.study.read.filter(k=>k.startsWith('m'+m.id+'p')).length;const entry=window.MODULE_LESSONS[m.id][0].entry;return `<article class="material-module"><button class="module-cover" data-read-module="${m.id}" data-read-page="${entry}" aria-label="Open study materials for module ${m.id}"><img src="${window.MODULE_SLIDES[m.id][1].image}" alt="Title slide of module ${m.id}: ${esc(m.title)}" loading="lazy" width="1600" height="900"><span class="cover-badge">${m.pages} original slides</span></button><div class="material-module-body"><span class="eyebrow">MODULE ${m.id} · ${m.framework.toUpperCase()}</span><h2>${esc(m.title)}</h2><p>${esc(m.subtitle)}</p><div class="mini-track"><i style="width:${count/m.pages*100}%"></i></div><div class="material-module-footer"><span>${count}/${m.pages} pages studied</span><button class="text-button" data-read-module="${m.id}" data-read-page="${state.study.module===m.id?state.study.page:entry}">Study module ↗</button></div></div></article>`;}).join('')}</div>`+footer();return;
    }
    const s=state.study,m=modules[s.module-1],slides=window.MODULE_SLIDES[m.id],slide=slides[s.page-1],topics=window.MODULE_LESSONS[m.id];
    const topic=topics.find(t=>s.page>=t.start&&s.page<=t.end),topicIndex=topics.indexOf(topic),key=`m${m.id}p${s.page}`,read=s.read.includes(key),bookmarked=s.bookmarks.includes(key);
    const relevant=m.notes.filter(n=>n.page>=topic.start&&n.page<=topic.end);
    main.innerHTML=versions+`<div class="reader-top"><button class="text-button" data-material-library>← All study materials</button><label for="reader-module" class="visually-hidden">Choose study module</label><select id="reader-module">${modules.map(mm=>`<option value="${mm.id}" ${mm.id===m.id?'selected':''}>M${mm.id} · ${esc(mm.title)}</option>`).join('')}</select></div><div class="reader-heading"><span class="eyebrow">MODULE ${m.id} · ${m.framework.toUpperCase()}</span><h1 class="page-title">${esc(m.title)}</h1><p>Read the explanation, then work through the original module slides.</p></div><div class="reader-layout"><details class="lesson-menu quiet-details"><summary>Topics and module options</summary><span class="eyebrow">IN THIS MODULE</span>${topics.map((t,i)=>`<button data-topic="${i}" class="lesson-topic ${topicIndex===i?'active':''}" ${topicIndex===i?'aria-current="step"':''}><span>${esc(t.title)}</span><small>Pages ${t.start}–${t.end}</small></button>`).join('')}<div class="lesson-count"><strong>${s.read.filter(k=>k.startsWith('m'+m.id+'p')).length}/${m.pages}</strong><span>pages marked studied</span></div><a href="modules/${encodeURIComponent(m.file)}" target="_blank" rel="noopener" class="source-link">Open full PDF ↗</a><button class="secondary" data-practice-module="${m.id}">Practice this module →</button></details><div class="lesson-main"><section class="lesson-explanation"><div class="lesson-number">TOPIC ${topicIndex+1} OF ${topics.length}</div><h2>${esc(topic.title)}</h2><p>${esc(topic.guide)}</p><div class="takeaway"><strong>Check your understanding</strong><p>${esc(topic.takeaway)}</p></div></section><section class="slide-panel" aria-labelledby="slide-title"><div class="slide-panel-head"><div><span class="eyebrow">FROM YOUR ORIGINAL MODULE</span><h2 id="slide-title">${esc(slide.title)}</h2></div><button class="star" data-slide-bookmark aria-label="${bookmarked?'Remove':'Add'} page bookmark" aria-pressed="${bookmarked}">${bookmarked?'★':'☆'}</button></div><button class="slide-image-button" data-enlarge-slide aria-label="Enlarge screenshot of module ${m.id}, page ${s.page}"><img id="current-slide" src="${slide.image}" alt="Original module ${m.id}, PDF page ${s.page}: ${esc(slide.title)}. Read the slide text below for a text version." width="1600" height="900"><span>⤢ Enlarge slide to read code</span></button><div class="slide-pager"><button class="secondary" data-slide-step="-1" ${s.page===1?'disabled':''}>← Previous</button><label for="slide-page">Page <select id="slide-page">${slides.map(p=>`<option value="${p.page}" ${p.page===s.page?'selected':''}>${p.page}</option>`).join('')}</select> of ${m.pages}</label><button class="secondary" data-slide-step="1" ${s.page===m.pages?'disabled':''}>Next →</button></div><div class="slide-actions"><button class="${read?'secondary read-marked':'primary blue'}" data-slide-read aria-pressed="${read}">${read?'✓ Marked studied':'Mark page studied ✓'}</button>${source({module:m.id,page:s.page},'Open this page in the PDF')}</div><details class="slide-transcript"><summary>Read the slide text</summary><pre>${esc(slide.text||'This slide contains visual material. Use the screenshot or original PDF.')}</pre><p>Text extracted from the original PDF. Refer to the screenshot for code indentation, tables, and diagrams.</p></details></section>${relevant.length?`<section class="reader-notes"><h2>Key ideas for this topic</h2>${relevant.map(n=>`<article class="note-card"><h3>${esc(n.title)}</h3>${n.body.includes('\n')?`<pre>${esc(n.body)}</pre>`:`<p>${esc(n.body)}</p>`}<button class="text-button" data-jump-slide="${n.page}">See the original · page ${n.page} →</button></article>`).join('')}</section>`:''}<details class="topic-slides"><summary>Browse all ${topic.end-topic.start+1} slides in this topic</summary><div class="slide-thumbnails">${slides.slice(topic.start-1,topic.end).map(p=>`<button data-jump-slide="${p.page}" class="${p.page===s.page?'active':''}" aria-label="Read page ${p.page}: ${esc(p.title)}"><img src="${p.image}" alt="" loading="lazy" width="1600" height="900"><span>Page ${p.page}${s.read.includes(`m${m.id}p${p.page}`)?' · ✓':''}</span></button>`).join('')}</div></details>${s.bookmarks.some(k=>k.startsWith('m'+m.id+'p'))?`<div class="reader-bookmarks"><strong>Your bookmarked pages</strong><div>${s.bookmarks.filter(k=>k.startsWith('m'+m.id+'p')).map(k=>`<button class="secondary" data-jump-slide="${Number(k.split('p')[1])}">★ Page ${Number(k.split('p')[1])}</button>`).join('')}</div></div>`:''}<div class="next-topic">${topicIndex<topics.length-1?`<button class="primary" data-topic="${topicIndex+1}">Next topic: ${esc(topics[topicIndex+1].title)} →</button>`:`<button class="primary" data-practice-module="${m.id}">Ready to practice M${m.id}? →</button>`}</div></div></div>`+footer();
  }
  function changeSlide(value){
    const y=window.scrollY;
    state.study.page=Math.max(1,Math.min(modules[state.study.module-1].pages,Number(value)));
    save();materials();window.scrollTo({top:y,behavior:'instant'});
  }
  function bank(){
    const lower=search.toLowerCase();
    let pool=selectedQuestions().filter(q=>(q.prompt+' '+q.answer+' '+q.topic+' '+q.explanation).toLowerCase().includes(lower));
    if(bankStatus==='stars')pool=pool.filter(q=>state.stars.includes(q.id));
    if(bankStatus==='missed')pool=missed(pool);
    if(bankStatus==='unseen')pool=pool.filter(q=>!state.records[q.id]);
    const pages=Math.max(1,Math.ceil(pool.length/12));bankPage=Math.min(bankPage,pages);
    main.innerHTML=breadcrumb('Find it. Understand it. Revisit it.')+'<span class="eyebrow">THE WHOLE COLLECTION</span><h1 class="page-title">Your question bank.</h1><p class="page-intro">Search the concepts, star the tricky ones, and open an answer when you’re ready. Module selections apply here too.</p>'+`${modulePicker()}<div class="toolbar"><input id="question-search" type="search" placeholder="Search questions, code, or topics…" aria-label="Search questions" value="${esc(search)}"><select id="bank-status" aria-label="Filter questions">${[['all','All questions'],['stars','Starred questions'],['missed','Needs review'],['unseen','Not yet tried']].map(([v,t])=>`<option value="${v}" ${v===bankStatus?'selected':''}>${t}</option>`).join('')}</select></div><div class="bank-reference"><p class="subtle">${pool.length} matching questions · Answers are hidden until you open them.</p><button class="text-button" data-page="notes">Quick reference notes ↗</button></div><div id="bank-list">${pool.slice((bankPage-1)*12,bankPage*12).map(q=>`<article class="bank-item"><div class="question-meta">${tag(q)}${star(q)}</div><h3>${prose(q.prompt)}</h3><details><summary>Reveal answer & explanation</summary><div class="answer-body"><strong>${prose(q.answer)}</strong><p>${prose(q.explanation)}</p>${source(q)}</div></details></article>`).join('')||'<div class="empty"><h3>No questions here yet.</h3><p>Try another search, filter, or module selection.</p></div>'}</div>${pages>1?`<div class="pagination"><button class="secondary" data-bank-page="${bankPage-1}" ${bankPage===1?'disabled':''}>← Previous</button><span>${bankPage} / ${pages}</span><button class="secondary" data-bank-page="${bankPage+1}" ${bankPage===pages?'disabled':''}>Next →</button></div>`:''}`+footer();
  }
  function notes(){
    const shown=modules.filter(m=>state.selected.includes(m.id)&&(notesModule==='all'||m.id===Number(notesModule)));
    const compare=[['Routes','app/Config/Routes.php','routes/web.php'],['Controllers','app/Controllers','app/Http/Controllers'],['Views','app/Views/*.php','resources/views/*.blade.php'],['Command-line tool','Spark','Artisan'],['Read all records','$model->findAll()','Task::all()'],['Missing single record','find($id) → null; check it','findOrFail($id) → 404'],['Mass assignment','$allowedFields','$fillable'],['Form token','csrf_field()','@csrf'],['Output escaping',"esc($task['title'])",'{{ $task->title }}'],['Route protection','Filter','Middleware'],['Public uploads','public/uploads + filename','Public disk + storage:link + path']];
    main.innerHTML=breadcrumb('Keep the two frameworks straight.')+'<span class="eyebrow">UNDERSTAND BEFORE YOU MEMORIZE</span><h1 class="page-title">Your module field guide.</h1><p class="page-intro">Short study notes and code patterns from your slides. Page links open the original PDF. Classroom examples are kept in their module context.</p>'+`<div class="toolbar"><select id="notes-module" aria-label="Choose notes module"><option value="all">All selected modules</option>${modules.map(m=>`<option value="${m.id}" ${Number(notesModule)===m.id?'selected':''}>M${m.id} · ${esc(m.title)}</option>`).join('')}</select><button class="secondary" data-print>Print notes</button></div><details class="bank-item"><summary>CodeIgniter ↔ Laravel: quick comparison</summary><div class="table-wrap"><table class="compare-table"><thead><tr><th>Responsibility</th><th>CodeIgniter</th><th>Laravel</th></tr></thead><tbody>${compare.map(row=>'<tr>'+row.map(v=>`<td>${esc(v)}</td>`).join('')+'</tr>').join('')}</tbody></table></div><p class="small muted">Cross-module comparison drawn from M1–M8. Use the module notes below for original page references.</p></details><div class="note-layout">${shown.map(m=>`<section><div class="module-heading"><span>M${m.id}</span><h2>${esc(m.title)}</h2></div>${m.notes.map(n=>`<article class="note-card"><h3>${esc(n.title)}</h3>${n.body.includes('\n')?`<pre>${esc(n.body)}</pre>`:`<p>${esc(n.body)}</p>`}${source({module:m.id,page:n.page})}</article>`).join('')}<a class="source-link" href="modules/${encodeURIComponent(m.file)}" target="_blank" rel="noopener">Open full module · ${m.pages} pages ↗</a></section>`).join('')||'<div class="empty"><h3>Select a module to read its notes.</h3><p>Use the module checkboxes to choose your material.</p></div>'}</div>`+footer();
  }
  function progress(){
    const st=stats();
    main.innerHTML=breadcrumb('Every attempt gives you a direction.')+'<span class="eyebrow">YOUR OWN SCOREBOARD</span><h1 class="page-title">Little by little, it sticks.</h1><p class="page-intro">Your latest answer on each question updates its status. Flashcards and typed recall use your own assessment. Everything stays in this browser.</p>'+`<section class="stats-strip"><div class="stat"><strong>${st.seen}</strong><span>unique questions<br>tried</span></div><div class="stat"><strong>${st.right}</strong><span>latest answer<br>correct</span></div><div class="stat"><strong>${missed(questions).length}</strong><span>questions to<br>revisit</span></div><div class="stat"><strong>${state.history.length}</strong><span>completed<br>sessions</span></div></section><div class="section-head"><h2>Your module map</h2><span>All modules</span></div><div class="module-grid">${modules.map(m=>{const deck=questions.filter(q=>q.module===m.id),st=stats(deck);return `<article class="progress-deck"><span class="eyebrow">MODULE ${m.id}</span><h3>${esc(m.title)}</h3><div class="mini-track"><i style="width:${st.right/deck.length*100}%"></i></div><div class="legend">${st.right} latest correct · ${st.seen-st.right} to revisit · ${deck.length-st.seen} untried</div></article>`;}).join('')}</div><div class="section-head"><h2>Recent sessions</h2><span>Last 50 saved</span></div>${state.history.length?`<div class="history-list">${state.history.map(h=>`<div class="history-row"><div>${esc(modes[h.mode]?.title||h.mode)}${h.self?' · self-graded':''}<small>${esc(new Date(h.date).toLocaleString(undefined,{dateStyle:'medium',timeStyle:'short'}))}${h.timedOut?' · time expired':''}</small></div><strong>${h.correct}/${h.total} · ${h.percent}%</strong></div>`).join('')}</div>`:'<div class="empty"><h3>Your first session starts here.</h3><p>Choose a study mode and finish a session to see it on your scoreboard.</p><button class="primary" data-page="home">Pick a mode →</button></div>'}<div class="toolbar-actions"><button class="secondary" data-export>Export my progress</button><label class="secondary" for="import-progress" style="cursor:pointer">Import progress</label><input type="file" id="import-progress" accept="application/json,.json" hidden><button class="danger" data-reset>Reset progress</button></div>`+footer();
  }
  function start(mode){
    let pool=mode==='loop'?missed():selectedQuestions();
    if(!pool.length){toast(mode==='loop'?'No missed questions in the selected modules.':'Select at least one module first.');return;}
    if(state.session && !confirm('Replace your saved session with a new one? Your answered-question progress will stay.'))return;
    if(mode!=='path')pool=shuffle(pool);
    pool=pool.slice(0,Math.max(1,Math.min(60,Math.floor(Number(state.count))||20)));
    const ids=pool.map(q=>q.id), options={};pool.forEach(q=>options[q.id]=shuffle(q.choices));
    state.session={mode,queue:ids,initial:ids.length,cursor:0,answers:[],options,revealed:false,draft:'',started:Date.now(),deadline:mode==='exam'?Date.now()+ids.length*60000:null};
    save();navigate('session');
  }
  function sessionView(){
    const s=state.session;if(!s){navigate('home');return;}
    if(s.mode==='exam'&&Date.now()>=s.deadline){finish(true);return;}
    const q=byId[s.queue[s.cursor]];if(!q){finish();return;}
    const self=s.mode==='recall'||s.mode==='flash', current=s.answers.find(a=>a.index===s.cursor), reviewable=s.mode!=='exam';
    const done=s.cursor+(current?1:0), pct=Math.min(100,done/s.queue.length*100);
    main.innerHTML=`<div class="session-head"><div><h1>${modes[s.mode].title}</h1><div class="session-sub">${s.mode==='loop'?`${s.queue.length-s.cursor} remaining · missed questions return to the queue`:`Question ${s.cursor+1} of ${s.queue.length}`}${self?' · self-graded':''}</div></div><div class="button-row">${s.deadline?'<span id="exam-clock" class="session-clock" aria-label="Time remaining"></span>':''}<button class="secondary" data-page="home">Save & exit</button></div></div><div class="progress-line" role="progressbar" aria-label="Session progress" aria-valuenow="${Math.round(pct)}" aria-valuemin="0" aria-valuemax="100"><span style="width:${pct}%"></span></div><article class="question-card"><div class="question-meta">${tag(q)}${s.mode==='exam'?'':star(q)}</div>${s.mode==='flash'?`<div class="flash-face"><span class="eyebrow">${s.revealed?'THE ANSWER':'RECALL IT BEFORE YOU FLIP'}</span><h2>${prose(s.revealed?q.answer:q.prompt)}</h2></div>`:`<h2>${prose(q.prompt)}</h2>`}${self?`${s.mode==='recall'?`<label class="typed-label" for="recall-answer">Your answer</label><input id="recall-answer" class="typed-input" placeholder="Try it from memory…" value="${esc(s.draft)}" ${s.revealed?'readonly':''} autocomplete="off">`:''}${!s.revealed?`<div class="button-row" style="margin-top:25px"><button class="primary blue" data-reveal>${s.mode==='flash'?'Flip the card':'Reveal & compare'} ↻</button></div>`:`<div class="feedback"><strong>${s.mode==='recall'?prose(q.answer):'Why this is the answer'}</strong><p>${prose(q.explanation)}</p>${source(q)}${!current?'<div class="self-grade"><button class="primary blue" data-grade="true">Got it ✓</button><button class="secondary" data-grade="false">Review again ↻</button></div>':''}</div>`}`:`<div class="choices">${s.options[q.id].map((option,i)=>{const correct=reviewable&&current&&option===q.answer,incorrect=reviewable&&current&&!current.correct&&option===current.chosen,selected=!reviewable&&current&&option===current.chosen;return `<button class="choice ${correct?'correct':''} ${incorrect?'incorrect':''} ${selected?'selected':''}" data-option="${i}" ${current?'disabled':''}><span class="letter">${correct?'✓':incorrect?'×':String.fromCharCode(65+i)}</span><span>${prose(option)}</span></button>`;}).join('')}</div>`}${current&&!self?reviewable?`<div class="feedback ${current.correct?'':'wrong'}" role="status"><strong>${current.correct?'That’s right.':'Keep this one on your radar.'}</strong><p>${prose(q.explanation)}</p>${source(q)}${s.mode==='loop'&&!current.correct?'<p>You’ll see this question again in this training loop.</p>':''}</div>`:'<div class="notice" role="status">Answer saved. Explanations appear when the rehearsal ends.</div>':''}<div class="session-bottom"><span class="hint">${s.mode==='exam'?'No hints or answer reveals during rehearsal.':self?'Be honest with your self-assessment.':'Read the explanation, even when you get it right.'}</span>${current?`<button class="primary" data-next>${s.cursor===s.queue.length-1?'Finish session':'Next question'} →</button>`:''}</div></article>${s.mode==='loop'?'<p class="small muted" style="text-align:center;margin-top:22px">Pause anytime with Save & exit. The loop ends when every queued question is answered correctly.</p>':''}`+footer();
    tickClocks();
  }
  function answer(correct,chosen){
    const s=state.session;if(!s||s.answers.some(a=>a.index===s.cursor))return;
    if(s.mode==='exam'&&Date.now()>=s.deadline){finish(true);return;}
    const q=byId[s.queue[s.cursor]];
    s.answers.push({id:q.id,index:s.cursor,chosen:chosen||s.draft||'(self-assessed)',correct});
    // Rehearsal feedback and status changes are deferred until finish.
    if(s.mode!=='exam')record(q.id,correct);
    if(s.mode==='loop'&&!correct)s.queue.push(q.id);
    save();sessionView();
  }
  function record(id,correct){const old=state.records[id]||{attempts:0,correct:0};state.records[id]={attempts:old.attempts+1,correct:old.correct+(correct?1:0),lastCorrect:correct,lastAt:new Date().toISOString()};}
  function finish(timedOut=false){
    const s=state.session;if(!s)return;
    const exam=s.mode==='exam';
    if(exam){s.queue.forEach((id,index)=>{if(!s.answers.some(a=>a.index===index))s.answers.push({id,index,chosen:'(unanswered)',correct:false});});s.answers.forEach(a=>record(a.id,a.correct));}
    const correct=s.answers.filter(a=>a.correct).length,total=s.answers.length,self=s.mode==='recall'||s.mode==='flash',percent=total?Math.round(correct/total*100):0;
    const h={mode:s.mode,date:new Date().toISOString(),correct,total,percent,self,timedOut};
    state.history.unshift(h);state.history=state.history.slice(0,50);state.session=null;save();page='result';
    document.body.classList.remove('session-active');document.querySelectorAll('nav button').forEach(b=>{b.classList.remove('active');b.removeAttribute('aria-current');});
    main.innerHTML=`<section class="score-panel"><span class="eyebrow">${timedOut?'TIME’S UP · SESSION SAVED':'ANOTHER SESSION IN THE BOOKS'}</span><h1>${percent===100?'That’s a strong finish.':percent>=70?'You’re finding your rhythm.':'Now you know what to revisit.'}</h1><p>${esc(modes[s.mode].title)}${self?' · self-assessed results':''}${s.mode==='loop'?' · includes repeat attempts':''}</p><div class="result-stats"><div><strong>${percent}%</strong><span>${self?'you marked correct':'accuracy'}</span></div><div><strong>${correct}/${total}</strong><span>correct attempts</span></div><div><strong>${Math.floor((Date.now()-s.started)/60000)}m</strong><span>elapsed since start</span></div></div><div class="button-row"><button class="primary" data-page="home">Back to study room →</button><button class="secondary" data-start="loop" ${missed().length?'':'disabled'}>Train missed questions ↻</button></div></section><div class="section-head"><h2>Your session review</h2><span>${total} attempts</span></div>${s.answers.map(a=>{const q=byId[a.id];return `<article class="bank-item"><div class="question-meta">${tag(q)}<span class="tag">${a.correct?'✓ Correct':'↻ Revisit'}</span>${star(q)}</div><h3>${prose(q.prompt)}</h3><p class="review-choice muted">Your ${self?'recall / assessment':'answer'}: ${esc(a.chosen)}${self?' · '+(a.correct?'Got it':'Review again'):''}</p><strong class="review-choice">Answer: ${prose(q.answer)}</strong><p class="small">${prose(q.explanation)}</p>${source(q)}</article>`;}).join('')}`+footer();
    window.scrollTo({top:0,behavior:'instant'});main.focus({preventScroll:true});
  }
  function clock(n){return `${String(Math.floor(Math.max(0,n)/60)).padStart(2,'0')}:${String(Math.max(0,n)%60).padStart(2,'0')}`;}
  function tickClocks(){
    if(focusEnd){focusRemaining=Math.max(0,Math.ceil((focusEnd-Date.now())/1000));if(!focusRemaining){focusEnd=0;toast('Focus session complete. Time for a short break.');document.querySelector('#focus-status').textContent='Session complete. Take a short break.';}}
    document.querySelector('#focus-label').textContent=clock(focusRemaining);document.querySelector('#focus-clock').textContent=clock(focusRemaining);document.querySelector('#focus-toggle').textContent=focusEnd?'Pause timer':focusRemaining===0?'Start another session':'Start timer';
    const s=state.session;if(s?.mode==='exam'){
      const remaining=Math.max(0,Math.ceil((s.deadline-Date.now())/1000));const el=document.querySelector('#exam-clock');if(el){el.textContent=clock(remaining);el.classList.toggle('timer-ending',remaining<=60);}
      if(remaining===0){if(page!=='session'){page='session';}finish(true);}
    }
  }
  document.addEventListener('click',event=>{
    const b=event.target.closest('button');if(!b||b.disabled)return;
    if(b.hasAttribute('data-read-module')){openMaterial(b.dataset.readModule,b.dataset.readPage);return;}
    if(b.hasAttribute('data-material-library')){materialReader=false;navigate('materials');return;}
    if(b.hasAttribute('data-topic')){const t=window.MODULE_LESSONS[state.study.module][Number(b.dataset.topic)];state.study.page=t.entry;save();materials();document.querySelector('.reader-heading').scrollIntoView({block:'start'});return;}
    if(b.hasAttribute('data-slide-step')){changeSlide(state.study.page+Number(b.dataset.slideStep));return;}
    if(b.hasAttribute('data-jump-slide')){changeSlide(b.dataset.jumpSlide);document.querySelector('.slide-panel').scrollIntoView({block:'start'});return;}
    if(b.hasAttribute('data-slide-read')||b.hasAttribute('data-slide-bookmark')){const key=`m${state.study.module}p${state.study.page}`,field=b.hasAttribute('data-slide-read')?'read':'bookmarks';state.study[field]=state.study[field].includes(key)?state.study[field].filter(k=>k!==key):[...state.study[field],key];save();const y=scrollY;materials();window.scrollTo({top:y,behavior:'instant'});document.querySelector(field==='read'?'[data-slide-read]':'[data-slide-bookmark]').focus({preventScroll:true});return;}
    if(b.hasAttribute('data-practice-module')){state.selected=[Number(b.dataset.practiceModule)];save();navigate('practice');return;}
    if(b.hasAttribute('data-enlarge-slide')){const s=state.study,p=window.MODULE_SLIDES[s.module][s.page-1],img=document.querySelector('#slide-enlarged');img.src=p.image;img.alt=`Module ${s.module}, page ${s.page}: ${p.title}`;document.querySelector('#slide-dialog-title').textContent=`M${s.module} · Page ${s.page} · ${p.title}`;img.classList.remove('full-size');document.querySelector('#slide-zoom').textContent='View at full size';document.querySelector('#slide-dialog').showModal();return;}
    if(b.dataset.page){navigate(b.dataset.page);return;}
    if(b.hasAttribute('data-start')){start(b.dataset.start);return;}
    if(b.dataset.deck){state.selected=[Number(b.dataset.deck)];save();navigate('practice');toast(`Module ${b.dataset.deck} selected.`);return;}
    if(b.hasAttribute('data-resume')){navigate('session');return;}
    if(b.hasAttribute('data-discard')){if(confirm('Discard the saved session? Answered-question progress will stay.')){state.session=null;save();render();}return;}
    if(b.dataset.star){const id=b.dataset.star;state.stars=state.stars.includes(id)?state.stars.filter(x=>x!==id):[...state.stars,id];save();b.textContent=state.stars.includes(id)?'★':'☆';b.setAttribute('aria-pressed',String(state.stars.includes(id)));b.setAttribute('aria-label',state.stars.includes(id)?'Unstar question':'Star question');if(page==='bank'&&bankStatus==='stars')bank();return;}
    if(b.dataset.bankPage){bankPage=Number(b.dataset.bankPage);bank();main.focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});return;}
    if(b.hasAttribute('data-reveal')){state.session.revealed=true;save();sessionView();return;}
    if(b.hasAttribute('data-grade')){answer(b.dataset.grade==='true');return;}
    if(b.hasAttribute('data-option')){const s=state.session;if(!s)return;const q=byId[s.queue[s.cursor]],chosen=s.options[q.id][Number(b.dataset.option)];answer(chosen===q.answer,chosen);return;}
    if(b.hasAttribute('data-next')){const s=state.session;if(!s)return;s.cursor++;s.revealed=false;s.draft='';if(s.cursor>=s.queue.length){finish();}else{save();sessionView();window.scrollTo({top:0,behavior:'instant'});main.focus({preventScroll:true});}return;}
    if(b.hasAttribute('data-print')){window.print();return;}
    if(b.hasAttribute('data-export')){const blob=new Blob([JSON.stringify({app:'framework-party',version:1,progress:state,guided:window.GuidedStudy.exportProgress()},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='framework-party-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('Progress exported. Keep this file as your backup.');return;}
    if(b.hasAttribute('data-reset')){if(confirm('Reset all study pages, bookmarks, guided reviews, answers, stars, history, and your saved session in this browser? Export a backup first if you want to keep them.')){state=initial();window.GuidedStudy.reset();save();render();toast('Your study progress has been reset.');}return;}
  });
  document.addEventListener('change',async event=>{
    const el=event.target;
    if(el.id==='reader-module'){const m=Number(el.value);openMaterial(m,window.MODULE_LESSONS[m][0].entry);return;}
    if(el.id==='slide-page'){changeSlide(el.value);return;}
    if(el.dataset.module){const id=Number(el.dataset.module);state.selected=el.checked?[...new Set([...state.selected,id])]:state.selected.filter(x=>x!==id);save();if(page==='session'){sidebar();toast('Module selection applies to your next session.');}else render();return;}
    if(el.id==='practice-module'){state.selected=el.value==='all'?modules.map(m=>m.id):[Number(el.value)];save();render();return;}
    if(el.id==='run-count'){state.count=Math.max(1,Math.min(60,Math.floor(Number(el.value))||20));save();return;}
    if(el.id==='bank-status'){bankStatus=el.value;bankPage=1;bank();return;}
    if(el.id==='notes-module'){notesModule=el.value;notes();return;}
    if(el.id==='import-progress'&&el.files[0]){
      try{
        const file=el.files[0];if(file.size>2000000)throw Error('Backup is too large.');
        const raw=JSON.parse(await file.text());if(raw.app!=='framework-party'||raw.version!==1||!raw.progress||typeof raw.progress!=='object')throw Error('This is not a Framework Party backup.');
        const p=raw.progress;
        if(!p.records||typeof p.records!=='object'||!Array.isArray(p.stars)||!Array.isArray(p.history))throw Error('The backup is missing progress data.');
        const valid=initial();valid.selected=Array.isArray(p.selected)?p.selected.filter(id=>modules.some(m=>m.id===id)):valid.selected;
        for(const [id,r]of Object.entries(p.records)){if(byId[id]&&r&&typeof r.lastCorrect==='boolean'&&Number.isInteger(r.attempts)&&r.attempts>0&&Number.isInteger(r.correct)&&r.correct>=0&&r.correct<=r.attempts)valid.records[id]={attempts:r.attempts,correct:r.correct,lastCorrect:r.lastCorrect,lastAt:typeof r.lastAt==='string'?r.lastAt:new Date().toISOString()};}
        valid.stars=[...new Set(p.stars.filter(id=>byId[id]))];valid.history=p.history.filter(h=>h&&modes[h.mode]&&Number.isFinite(h.correct)&&Number.isFinite(h.total)&&h.total>0&&h.correct>=0&&h.correct<=h.total&&!isNaN(Date.parse(h.date))).slice(0,50).map(h=>({mode:h.mode,date:h.date,correct:h.correct,total:h.total,percent:Math.round(h.correct/h.total*100),self:h.mode==='flash'||h.mode==='recall',timedOut:!!h.timedOut}));
        if(!confirm('Replace this browser’s progress with the imported answers, stars, and history? An in-progress session will be cleared.'))return;
        valid.study=validStudy(p.study);state=valid;if(raw.guided)window.GuidedStudy.importProgress(raw.guided);save();render();toast('Study progress, answers, stars, and session history imported.');
      }catch(error){toast(error.message||'The progress file could not be read.');}
    }
  });
  document.addEventListener('input',event=>{
    const el=event.target;if(el.id==='recall-answer'&&state.session){state.session.draft=el.value;save();}
    if(el.id==='question-search'){const pos=el.selectionStart;search=el.value;bankPage=1;bank();const newEl=document.querySelector('#question-search');newEl.focus();newEl.setSelectionRange(pos,pos);}
  });
  document.addEventListener('keydown',event=>{if(event.key==='Enter'&&event.target.id==='recall-answer'&&!state.session?.revealed){event.preventDefault();state.session.revealed=true;save();sessionView();}});
  document.querySelector('#select-all').addEventListener('click',()=>{state.selected=state.selected.length===8?[]:modules.map(m=>m.id);save();page==='session'?sidebar():render();});
  const focusDialog=document.querySelector('#focus-dialog');
  document.querySelector('#focus-open').onclick=()=>focusDialog.showModal();document.querySelector('#focus-close').onclick=()=>focusDialog.close();
  document.querySelector('#focus-toggle').onclick=()=>{if(focusEnd){focusRemaining=Math.max(0,Math.ceil((focusEnd-Date.now())/1000));focusEnd=0;document.querySelector('#focus-status').textContent='Paused. Pick up when you’re ready.';}else{if(!focusRemaining)focusRemaining=25*60;focusEnd=Date.now()+focusRemaining*1000;document.querySelector('#focus-status').textContent='Focus time. One concept at a time.';}tickClocks();};
  document.querySelector('#focus-reset').onclick=()=>{focusEnd=0;focusRemaining=25*60;document.querySelector('#focus-status').textContent='Ready when you are.';tickClocks();};
  document.querySelector('#slide-close').onclick=()=>document.querySelector('#slide-dialog').close();
  document.querySelector('#slide-zoom').onclick=()=>{const img=document.querySelector('#slide-enlarged'),full=img.classList.toggle('full-size');document.querySelector('#slide-zoom').textContent=full?'Fit to window':'View at full size';};
  window.addEventListener('beforeunload',save);
  save();render();tickClocks();setInterval(tickClocks,1000);
})();
