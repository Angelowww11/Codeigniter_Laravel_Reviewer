const assert=require('node:assert/strict');global.window={};require('../content.js');
const {modules,questions}=window.STUDY_DATA;
const source=require('./question-bank.json');
assert.deepEqual(questions,source,'Rebuild content.js from the canonical question bank.');
assert.equal(questions.length,480);assert.equal(new Set(questions.map(q=>q.id)).size,480);
for(const m of modules){const deck=questions.filter(q=>q.module===m.id);assert.equal(deck.length,60);assert.equal(deck.filter(q=>q.kind==='application').length,24);assert.equal(new Set(deck.map(q=>q.prompt)).size,60);for(const q of deck){assert.equal(q.choices.length,4);assert.equal(new Set(q.choices).size,4);assert(q.choices.includes(q.answer));assert(q.page>=1&&q.page<=m.pages);assert(q.explanation.trim());assert.deepEqual(Object.keys(q.choiceExplanations),q.choices);assert.equal(q.choiceExplanations[q.answer],q.explanation);assert(Object.values(q.choiceExplanations).every(reason=>typeof reason==='string'&&reason.trim()));assert(!/printed demo|does the (?:PDF|module)|checklist identify|which .*demonstration/i.test(q.prompt),q.id);assert(!/See Module \d, PDF page|Identify the responsibility before/.test(q.explanation),q.id);assert(!JSON.stringify(q).includes('\ufffd'),q.id);}}
console.log('Validated 480 questions, 24 applied checks per module, unique IDs/prompts, answer options, canonical source, and PDF references.');
