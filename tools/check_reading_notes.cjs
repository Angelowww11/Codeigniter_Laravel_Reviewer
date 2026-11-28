const fs=require('node:fs'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
function check(){
 const rewrites=require('./notes-style-rewrites.json'),baseline=require('./feedback-baseline.json');
 for(let module=1;module<=8;module++){
  const audit=rewrites[module],current=fs.readFileSync(audit.file,'utf8');let original=current.replace(/\r\n/g,'\n');
  for(const [before,after] of [...audit.replacements].reverse()){
   assert(original.includes(after),`${audit.file}: missing approved explanatory rewrite`);
   original=original.replaceAll(after,before);
  }
  if(audit.original_crlf)original=original.replace(/\n/g,'\r\n');
  assert.equal(hash(original),audit.original_sha256,`${audit.file}: an original explanation or code example was removed or changed outside the approved style edits`);
  assert.equal(audit.original_sha256,baseline.files[audit.file],`${audit.file}: original hash differs from the earlier preservation check`);
 }
 const coverage=require('./notes-source-map.json'),supplement=require('../notes-source/module-connections.json');
 assert.equal(coverage.length,300);assert.equal(new Set(coverage.map(p=>`${p.module}/${p.page}`)).size,300);
 const html=fs.readFileSync('reviewer.html','utf8');
 for(const page of coverage){assert(page.sections.length);for(const id of page.sections)assert(html.includes(`id="${id}"`),`Broken source-page link: ${page.module}/${page.page}`);}
 assert.equal(Object.keys(supplement).length,8);
 for(let module=1;module<=8;module++){
  assert(supplement[module].includes('#### Source connections:'));
  assert(supplement[module].includes('<p class="page-range">PDF pages '));
  assert(html.includes(`id="module-${module}-source-details"`));
 }
 assert(html.includes('reviewer.css?v=9'));
 assert(!/Situational reasoning|Situation [123]|Exam cue:|Apply the concepts:/.test(html));
 return {modules:8,sourcePages:coverage.length};
}
module.exports={check};
if(require.main===module){const result=check();console.log(`Checked ${result.modules} complete original note chapters, preserved explanations and code, ${result.sourcePages} source-page links, and the reading-note format.`);}
