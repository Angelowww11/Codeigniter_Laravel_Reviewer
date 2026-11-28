"""Build a static, readable reviewer. No study state or quiz code is included."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json, re, subprocess
from markdown_it import MarkdownIt

HERE=Path(__file__).resolve().parents[1]/'notes-source'
ROOT=Path(__file__).resolve().parents[1]
connections=json.loads((HERE/'module-connections.json').read_text(encoding='utf-8'))
modules=json.loads(subprocess.check_output(['node','-e',"global.window={};require('./content.js');console.log(JSON.stringify(window.STUDY_DATA.modules.map(({id,title,pages,file})=>({id,title,pages,file}))))"],cwd=ROOT,text=True))
# Highlight all fenced examples in one local process. The output remains static HTML.
parser=MarkdownIt('commonmark',{'html':True}).enable('table')
snippets={}
for source in sorted(HERE.glob('reviewer-m*.txt')):
    for token in parser.parse(source.read_text(encoding='utf-8')):
        if token.type=='fence': snippets[(token.content,token.info.strip())]=None
keys=list(snippets)
rendered=json.loads(subprocess.check_output(['node',str(ROOT/'tools/highlight.cjs')],input=json.dumps([{'code':code,'language':language} for code,language in keys]),cwd=ROOT,text=True,encoding='utf-8'))
snippets=dict(zip(keys,rendered))
md=MarkdownIt('commonmark',{'html':True,'typographer':False,'highlight':lambda code,language,*_:snippets.get((code,language),'')}).enable('table')
def toc():
    return '<ol>'+''.join(f'<li><a href="#module-{m["id"]}"><span>M{m["id"]}</span>{escape(m["title"])}</a></li>' for m in modules)+'</ol><a class="toc-extra" href="#comparison">Framework comparison</a><a class="toc-extra" href="#coverage">PDF coverage &amp; references</a>'

chapters=[];coverages=[];source_map=[];subheads=0;words=0
for m in modules:
    n=m['id'];text=(HERE/f'reviewer-m{n}.txt').read_text(encoding='utf-8')+'\n'+connections[str(n)];words+=len(text.split())
    covered=set();sections=[]
    for match in re.finditer(r'### (\d+\.\d+) ([^\n]+)\n<p class="page-range">PDF pages? ([^·<]+)',text):
        number,title,page_text=match.groups();numbers=[]
        for a,b in re.findall(r'(\d+)(?:–(\d+))?',page_text):numbers+=list(range(int(a),int(b or a)+1))
        covered.update(numbers);sections.append((number,title,page_text.strip(),min(numbers)))
    assert covered==set(range(1,m['pages']+1)),f'M{n} missing {set(range(1,m["pages"]+1))-covered}'
    html=md.render(text)
    html=html.replace('<h4>Workflow notes:',f'<h4 id="module-{n}-application">Workflow notes:')
    html=html.replace('<h4>Source connections:',f'<h4 id="module-{n}-source-details">Source connections:')
    for number,title,page_text,first in sections:
        html=html.replace('<h3>'+escape(number+' '+title)+'</h3>',f'<h3 id="section-{number.replace(".","-")}">{escape(number+" "+title)}</h3>')
    # Every section's source range links to its actual original PDF.
    def link_range(match):
        label=match.group(1);first=int(re.search(r'\d+',label).group())
        url='modules/'+quote(m['file'])+f'#page={first}'
        return f'<p class="page-range"><a href="{url}" target="_blank" rel="noopener">{label} ↗</a></p>'
    html=re.sub(r'<p class="page-range">(.*?)</p>',link_range,html)
    html=re.sub(r'<img src="([^"]+)"([^>]+)>',r'<a href="\1" target="_blank" rel="noopener" aria-label="Open original figure at full size"><img src="\1"\2></a>',html)
    html=re.sub(r'<table>(.*?)</table>',r'<div class="notes-table" tabindex="0" role="region" aria-label="Reference table"><table>\1</table></div>',html,flags=re.S)
    html=html.replace('<pre>','<pre tabindex="0">')
    local='<nav class="chapter-outline" aria-label="Module '+str(n)+' sections">'+''.join(f'<a href="#section-{num.replace(".","-")}">{escape(num+" "+title)}</a>' for num,title,_,_ in sections)+f'<a href="#module-{n}-application">Workflow notes</a></nav>'
    chapters.append(f'<article class="notes-chapter" id="module-{n}" aria-labelledby="module-title-{n}"><header class="chapter-heading"><span class="chapter-number">MODULE {n:02d}</span><h2 id="module-title-{n}">{escape(m["title"])}</h2><p>{m["pages"]} source pages · {"CodeIgniter" if n<5 else "Laravel"} · <a href="modules/{quote(m["file"])}" target="_blank" rel="noopener">Original PDF ↗</a></p></header>{local}{html}<a class="back-contents" href="#contents">↑ Back to contents</a></article>')
    coverages.append('<tr><th scope="row">M'+str(n)+'</th><td>'+str(m['pages'])+' / '+str(m['pages'])+'</td><td>'+', '.join(f'<a href="#section-{num.replace(".","-")}">{escape(num)}: {escape(pages)}</a>' for num,_,pages,_ in sections)+'</td></tr>')
    subheads+=len(sections)
    for page in range(1,m['pages']+1):
        anchors=[]
        for number,title,page_text,_ in sections:
            ranges=[(int(a),int(b or a)) for a,b in re.findall(r'(\d+)(?:–(\d+))?',page_text)]
            if any(a<=page<=b for a,b in ranges): anchors.append('section-'+number.replace('.','-'))
        source_map.append({'module':n,'page':page,'sections':anchors,'role':'front matter' if page<=5 else 'closing discussion' if page==m['pages'] else 'teaching'})

comparison=md.render('''
## Keep the two frameworks separate

This comparison gathers patterns already explained in the eight modules. Similar purpose does not mean identical method names or return values.

| Responsibility | CodeIgniter course pattern | Laravel course pattern |
| --- | --- | --- |
| Local server | `php spark serve` | `php artisan serve` |
| List records | `$model->findAll()` | `Task::all()` or query `->get()` |
| One record | `$model->find($id)`; check null | `Task::findOrFail($id)` or model binding |
| Default result style in the examples | `$task['title']` | `$task->title` |
| Writable fields | `$allowedFields` | `$fillable` |
| New record | `$model->insert($data)` | `Task::create($data)` |
| Update | `$model->update($id, $data)` | `$task->update($data)` |
| Delete | `$model->delete($id)` | `$task->delete()` |
| Safe displayed text | `esc($value)` | `{{ $value }}` |
| CSRF field | `csrf_field()` plus enabled filter | `@csrf` with web protection |
| Validation | `$this->validate($rules)` / file validation example | `$request->validate($rules)` |
| Old input | `old('title', $task['title'])` | `old('title', $task->title)` |
| Route access gate | Registered filter alias | `auth` middleware |
| Class-based record access | CI Model / Query Builder | Eloquent model / ORM |
| Uploaded public-image reference | Generated filename in `public/uploads` example | Relative path on the `public` disk |

<aside class="notes-important"><strong>The workflow worth remembering</strong><p><mark>Match the route → check identity/access → validate input → perform the intended data/file operation → return or redirect → display escaped output.</mark> The syntax changes between frameworks; the responsibilities remain recognizable.</p></aside>
''')
comparison=re.sub(r'<table>(.*?)</table>',r'<div class="notes-table" tabindex="0" role="region" aria-label="Framework comparison"><table>\1</table></div>',comparison,flags=re.S)

out='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f6f5fb"><title>Reviewer Notes · IT0049 · Framework Party</title><meta name="description" content="Detailed student-style CodeIgniter and Laravel reviewer notes covering all eight IT0049 PDFs, with highlighted key points, figures, explained code, and original page references."><script src="appearance.js?v=6"></script><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="design.css?v=6"><link rel="stylesheet" href="reviewer.css?v=9"><link rel="stylesheet" href="code-theme.css?v=8"></head><body class="reviewer-page">
<a class="notes-skip" href="#notes-main">Skip to reviewer</a>
<header class="notes-topbar"><a class="notes-brand" href="index.html">framework party<span>IT0049 / WEB</span></a><nav aria-label="Website sections"><a href="index.html">Home</a><a href="index.html#guided">Study</a><a class="active" href="reviewer.html" aria-current="page">Reviewer Notes</a><a href="index.html#practice">Practice</a><a href="index.html#materials">Original slides</a></nav></header>
<div class="notes-layout"><aside class="notes-sidebar" aria-label="Reviewer contents"><a class="notes-sidebar-title" href="#contents">IN THIS REVIEWER</a>'''+toc()+'''<p>Read straight through, or jump to a module. Use your browser’s Find to locate a term and Print to save a PDF.</p></aside>
<main id="notes-main"><header class="notes-cover" id="contents"><h1>Reviewer<br><span>notes.</span></h1><p class="notes-lead">CodeIgniter &amp; Laravel, written out like a study notebook.</p><p>A continuous reviewer with definitions, comparison tables, highlighted takeaways, original figures, and fully explained code examples. Start anywhere; every chapter stays fully open.</p><div class="notes-cover-meta"><span>8 modules</span><span>300 source pages</span><span>Code + figures + examples</span></div><aside class="notes-reading-key"><strong>How to read the annotations</strong><p><mark>Highlights</mark> mark ideas worth remembering. <b>Take note</b> boxes explain important distinctions. <b>Clarification</b> boxes identify source shortcuts or assumptions. Worked examples explain each connection and its result. Questions remain in the separate Practice area. Each section links to its original PDF page range.</p></aside><p class="notes-scope">These notes follow your supplied classroom PDFs. Code is rewritten for readability; file labels and comments show context. Short fragments assume surrounding framework setup. Added explanations and corrections are identified rather than presented as verbatim slide content.</p><details class="notes-mobile-contents"><summary>Contents · all 8 modules</summary>'''+toc()+'''</details></header>
'''+''.join(chapters)+f'''<section class="notes-chapter" id="comparison">{comparison}</section><section class="notes-chapter" id="coverage"><h2>PDF coverage &amp; references</h2><p>The {subheads} numbered sections above account for all 300 PDF pages. Title, objective, divider, recap, and Q&amp;A pages are included in their relevant chapter ranges; they are not presented as extra technical lessons. Overlapping ranges indicate that a source page contributes to more than one explanation.</p><div class="notes-table" tabindex="0" role="region" aria-label="PDF page coverage"><table><thead><tr><th>Module</th><th>Pages accounted for</th><th>Notes section → PDF pages</th></tr></thead><tbody>{''.join(coverages)}</tbody></table></div><h3>Original course files</h3><ol class="source-files">'''+''.join(f'<li><a href="modules/{quote(m["file"])}" target="_blank" rel="noopener">{escape(m["file"])} ↗</a></li>' for m in modules)+'''</ol><h3>Supplementary accuracy checks</h3><p>The notes primarily follow the eight supplied PDFs. Official documentation was used to clarify the explicitly labeled points below; it does not replace your classroom source or prescribe a framework upgrade.</p><ul><li><a href="https://codeigniter4.github.io/userguide/incoming/routing.html">CodeIgniter routing</a>: explicit handlers, placeholders, and the default method.</li><li><a href="https://codeigniter4.github.io/userguide/libraries/validation.html">CodeIgniter validation</a>: distinct validation rules and field requirements.</li><li><a href="https://codeigniter4.github.io/userguide/libraries/security.html">CodeIgniter CSRF protection</a>: token fields work with enabled protection.</li><li><a href="https://codeigniter4.github.io/userguide/database/connecting.html">CodeIgniter database connections</a>: a database operation is required to test database access.</li><li><a href="https://codeigniter4.github.io/userguide/libraries/sessions.html">CodeIgniter sessions</a>: session operations and flash-data lifecycle.</li><li><a href="https://laravel.com/docs/12.x/validation">Laravel validation</a> and <a href="https://laravel.com/docs/12.x/mail">mail</a>: validation feedback, mailable content, and transport responsibilities.</li><li><a href="https://laravel.com/docs/12.x/requests">Laravel request handling</a> and <a href="https://laravel.com/docs/12.x/authorization">authorization</a>: request context, identity, and resource permissions.</li></ul><p>Original figures belong to the supplied course materials. Flow figures in these notes are explanatory redrawings. No exercise answers or external exam were used as the source of this reviewer.</p><a class="back-contents" href="#contents">↑ Back to contents</a></section><footer class="notes-footer"><a href="index.html">← Return to the study website</a><span>Framework Party · Complete notes, one page at a time.</span></footer></main></div></body></html>'''
table_counter=iter(range(1,1000))
out=re.sub(r'aria-label="Reference table"',lambda _:f'aria-label="Reference table {next(table_counter)}"',out)
(ROOT/'reviewer.html').write_text(out,encoding='utf-8')
(ROOT/'tools/notes-source-map.json').write_text(json.dumps(source_map,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'modules':8,'sections':subheads,'source_pages':300,'draft_words_including_code':words,'figures':out.count('<figure'),'code_examples':out.count('<pre '),'html_bytes':len(out.encode())}))
