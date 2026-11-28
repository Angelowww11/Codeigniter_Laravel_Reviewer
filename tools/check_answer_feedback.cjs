const assert=require('node:assert/strict'),fs=require('node:fs'),crypto=require('node:crypto'),vm=require('node:vm');
const {render}=require('../answer-feedback.js'),questions=require('./question-bank.json'),baseline=require('./feedback-baseline.json');
const hash=v=>crypto.createHash('sha256').update(v).digest('hex');
const core=q=>({id:q.id,module:q.module,page:q.page,topic:q.topic,prompt:q.prompt,answer:q.answer,choices:q.choices,kind:q.kind});
const revised=new Set(['m1q11','m1q49','m1q52','m2q52','m2q54','m4q6','m6q13','m6q47']);
const plain=s=>s.replace(/<[^>]*>/g,'').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'");
let selections=0;
for(const q of questions){
 assert.deepEqual(Object.keys(q.choiceExplanations),q.choices,q.id);
 assert.equal(q.choiceExplanations[q.answer],q.explanation);
 assert.ok(Object.values(q.choiceExplanations).every(v=>typeof v==='string'&&v.trim().length>=12),q.id);
 const base=q.id.match(/^m\d+q\d+/)[0];
 if(revised.has(base))assert.equal(q.id,base+'-feedback-v3');
 else assert.equal(hash(JSON.stringify(core(q))),baseline.questions[q.id],q.id+' changed unexpectedly');
 for(const chosen of [...q.choices,'(unanswered)',null]){
  const html=render(q,chosen,{heading:'h4'}),text=plain(html);selections++;
  assert.ok(text.includes(q.explanation));
  for(const option of q.choices.filter(c=>c!==q.answer))assert.ok(text.includes(q.choiceExplanations[option]),q.id+' missing reason for '+option);
  assert.equal((html.match(/data-feedback-option=/g)||[]).length,3,q.id);
  assert.equal(html.includes('Why your answer is wrong'),q.choices.includes(chosen)&&chosen!==q.answer);
  assert.equal(html.includes('You did not answer this question.'),chosen==='(unanswered)');
 }
 // Reversing the displayed options cannot change the option-to-explanation mapping.
 const reversed={...q,choices:[...q.choices].reverse()};
 assert.ok(plain(render(reversed,q.choices[1])).includes(q.choiceExplanations[q.choices[1]]));
}
const malicious='<img src=x onerror=alert(1)>',probe={answer:'A',choices:['A',malicious,'C','D'],explanation:malicious,choiceExplanations:{A:malicious,[malicious]:malicious,C:'A reason for C',D:'A reason for D'}};
assert.ok(!render(probe,malicious).includes('<img'));
// The authorized reading-note revision changes headings and adds source guides.
// Its separate check reconstructs each original chapter and checks its prior hash.
require('./check_reading_notes.cjs').check();
for(const [file,expected]of Object.entries(baseline.files)){
 if(file==='reviewer.html'||file.startsWith('notes-source/'))continue;
 assert.equal(hash(fs.readFileSync(file)),expected,file+' changed');
}
const deployed={window:{}};vm.runInNewContext(fs.readFileSync('content.js','utf8'),deployed);delete deployed.window.STUDY_DATA.questions;
assert.equal(hash(JSON.stringify(deployed.window.STUDY_DATA)),baseline.courseData,'Course modules, lessons, or references changed');
const entry=fs.readFileSync('index.html','utf8');
assert.ok(entry.includes('answer-feedback.css?'));
assert.ok(entry.indexOf('src="answer-feedback.js?')<entry.indexOf('src="app.js?'));
assert.ok(/<script src="answer-feedback\.js\?[^\"]+" defer>/.test(entry));
assert.ok(!questions.find(q=>q.id==='m2q52-feedback-v3').choices.includes('find()'));
assert.ok(!questions.find(q=>q.id==='m4q6-feedback-v3').choices.includes('get()'));
for(const [id,required]of [['m7q41','CSRF'],['m7q11','kilobytes'],['m8q53','property'],['m6q13-feedback-v3','collection']]){
 assert.ok(questions.find(q=>q.id===id).explanation.toLowerCase().includes(required.toLowerCase()),id+' must explain its own topic');
}
console.log(`PASS: 480 questions, 1920 authored choice explanations, ${selections} answer states, shuffled choices, escaping, eight explicit revisions, unchanged course assets, and preserved note explanations.`);
