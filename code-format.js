/* Shared, local syntax rendering. PrismJS is bundled with its MIT license. */
(() => {
  'use strict';
  const P = globalThis.Prism;
  const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  if (P) {
    P.languages.insertBefore('bash','function',{
      'framework-command': {pattern:/\b(?:php|composer|npm|laravel)(?=\s|$)/m,alias:'function'}
    });
    P.languages.blade = P.languages.extend('markup', {});
    P.languages.insertBefore('blade', 'tag', {
      'blade-comment': {pattern: /\{\{--[\s\S]*?--\}\}/, alias: 'comment'},
      'blade-expression': {
        pattern: /\{!![\s\S]*?!!\}|\{\{[\s\S]*?\}\}/,
        inside: {'delimiter': {pattern: /^\{!!|!!\}$|^\{\{|\}\}$/, alias: 'punctuation'}, rest: P.languages.php}
      },
      'blade-directive': {
        pattern: /@[a-zA-Z_]\w*(?:\((?:[^()'"\n]|'[^'\n]*'|"[^"\n]*"|\([^()\n]*\))*\))?/,
        inside: {'keyword': /^@\w+/, rest: P.languages.php}
      }
    });
  }
  function language(source, hint = '') {
    const aliases = {sh:'bash', shell:'bash', html:'markup', apache:'apacheconf', env:'ini'};
    let name = aliases[hint] || hint;
    if (/\{\{|\{!!|@(csrf|method|error|foreach|if|endif|end)/.test(source) && (!name || name==='markup' || name==='php')) return 'blade';
    if (!name) {
      if (/<\?php|\$\w|->|::|^use |^namespace /m.test(source)) name='php';
      else if (/<[a-z][\s\S]*>/i.test(source)) name='markup';
      else if (/^(?:php |composer |npm |cd |laravel )/m.test(source)) name='bash';
      else if (/^(?:SELECT|CREATE TABLE|INSERT INTO|UPDATE|DELETE FROM)\b/im.test(source)) name='sql';
      else if (/^[\w.]+\s*=/m.test(source)) name='ini';
      else name='text';
    }
    return name;
  }
  function highlight(source, hint) {
    const lang=language(source,hint);
    return P?.languages[lang] ? P.highlight(source, P.languages[lang], lang) : escape(source);
  }
  function block(source, hint) {
    const lang=language(source,hint);
    return `<pre class="study-code" tabindex="0" aria-label="${escape(lang)} code example"><code class="language-${lang}">${highlight(source,lang)}</code></pre>`;
  }
  function prose(source) {
    // Keep stored answers exact. Code formatting affects presentation, never grading.
    const pattern=/(`[^`\n]+`|\$[A-Za-z_]\w*(?:(?:->|::)\w+(?:\([^()\n]*\))?|\[[^\]\n]+\])*(?:\([^()\n]*\))?|\b[A-Z]\w*::\w+\([^()\n]*\)|\{\{[^\n]*?\}\}|@(?:csrf|method|foreach|endforeach|if|endif|error|enderror)(?:\([^()\n]*\))?)/g;
    return String(source).split(pattern).map((part,index) => index%2
      ? `<code class="inline-syntax">${highlight(part.startsWith('`')?part.slice(1,-1):part,language(part,'php'))}</code>` : escape(part)).join('');
  }
  function enhance(root=document) {
    root.querySelectorAll('pre').forEach(pre => {
      if (pre.dataset.syntaxReady) return;
      let code=pre.querySelector('code');
      if (!code) {code=document.createElement('code');code.textContent=pre.textContent;pre.replaceChildren(code);}
      // These may already contain build-time highlighting.
      if (code.querySelector('.token')) {pre.dataset.syntaxReady='true';return;}
      const source=code.textContent;
      const hint=(code.className.match(/language-([\w-]+)/)||[])[1];
      const lang=language(source,hint);
      code.className=`language-${lang}`;
      code.innerHTML=highlight(source,lang);
      pre.classList.add('study-code');
      if (!pre.hasAttribute('tabindex')) pre.tabIndex=0;
      pre.dataset.syntaxReady='true';
    });
  }
  globalThis.StudyCode={highlight,block,prose,language,enhance};
  if (typeof document !== 'undefined') {
    const start=()=>{
      enhance();
      // The existing app replaces its content for each lesson and quiz screen.
      const main=document.querySelector('main');
      if(main)new MutationObserver(records=>{
        if(records.some(record=>Array.from(record.addedNodes).some(node=>node.nodeType===1 && (node.matches?.('pre') || node.querySelector?.('pre')))))enhance(main);
      }).observe(main,{childList:true,subtree:true});
    };
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
  }
})();
