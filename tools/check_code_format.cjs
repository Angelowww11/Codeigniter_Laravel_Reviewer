const assert=require('node:assert/strict');
require('../assets/prism/prism.js');
require('../code-format.js');
const samples=[
  ['php',"$task->update(['title' => 'A < B']); // Keep the value"],
  ['php','<?php if ($task): ?><h1><?= esc($task[\'title\']) ?></h1><?php endif; ?>'],
  ['html','<form method="POST">\n @csrf\n @method(\'PATCH\')\n {{ $task->title }}\n</form>'],
  ['sql',"SELECT title FROM tasks WHERE status = 'pending';"],
  ['ini',"database.default.hostname = localhost\nCI_ENVIRONMENT = development"],
  ['sh','php artisan storage:link'],
  ['apache','RewriteEngine On\nRewriteRule ^(.*)$ public/$1 [L]'],
  ['text','plain <script>alert("test")</script> & text'],
];
function decode(html){return html.replace(/<[^>]*>/g,'').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&amp;/g,'&');}
for(const [language,code] of samples){
  const html=StudyCode.highlight(code,language);
  assert.equal(decode(html),code,`Source changed for ${language}`);
  assert(!html.includes('<script>'),'Unescaped input');
  if(language!=='text')assert(html.includes('class="token'),`Missing tokens for ${language}`);
}
const blade=StudyCode.highlight('@csrf {{ $task->title }}','html');
assert(blade.includes('blade-directive'));
assert(blade.includes('token variable'));
assert(StudyCode.prose('Read `$task->title`, then <img src=x onerror=alert(1)>').includes('&lt;img'));
assert(!StudyCode.prose('<script>alert(1)</script>').includes('<script>'));
console.log('Validated source-preserving syntax tokens, Blade directives, and escaped code/prose.');
