const assert=require('node:assert/strict');global.window={};require('../content.js');
const {modules,questions}=window.STUDY_DATA;
assert.equal(questions.length,480);assert.equal(new Set(questions.map(q=>q.id)).size,480);
for(const m of modules){const deck=questions.filter(q=>q.module===m.id);assert.equal(deck.length,60);assert.equal(new Set(deck.map(q=>q.prompt)).size,60);for(const q of deck){assert.equal(q.choices.length,4);assert.equal(new Set(q.choices).size,4);assert(q.choices.includes(q.answer));assert(q.page>=1&&q.page<=m.pages);assert(q.explanation.trim());}}
console.log('Validated 480 questions, 60 per module, unique IDs/prompts, answer options, and PDF page references.');
