// Build-time highlighting keeps the continuous reviewer readable without JavaScript.
require('../assets/prism/prism.js');
require('../code-format.js');
let input='';
process.stdin.setEncoding('utf8');
process.stdin.on('data',chunk=>input+=chunk);
process.stdin.on('end',()=>{
  const blocks=JSON.parse(input);
  process.stdout.write(JSON.stringify(blocks.map(({code,language})=>StudyCode.block(code,language))));
});
