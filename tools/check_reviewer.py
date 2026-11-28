"""Check that the generated static reviewer retains every fenced source example."""
from pathlib import Path
from html.parser import HTMLParser
from markdown_it import MarkdownIt
import re

ROOT=Path(__file__).resolve().parents[1]
class CodeReader(HTMLParser):
    def __init__(self):
        super().__init__();self.in_pre=False;self.current='';self.blocks=[]
    def handle_starttag(self,tag,attrs):
        if tag=='pre':self.in_pre=True;self.current=''
    def handle_endtag(self,tag):
        if tag=='pre':self.in_pre=False;self.blocks.append(self.current)
    def handle_data(self,data):
        if self.in_pre:self.current+=data

html=(ROOT/'reviewer.html').read_text(encoding='utf-8')
reader=CodeReader();reader.feed(html)
expected=[];md=MarkdownIt()
for n in range(1,9):
    text=(ROOT/'notes-source'/f'reviewer-m{n}.txt').read_text(encoding='utf-8')
    expected.extend(t.content for t in md.parse(text) if t.type=='fence')
    assert '**Situation ' not in text and '**Exam cue:**' not in text,n
    assert len(re.findall(r'^##### ',text,re.M))==3,n
    assert text.count('#### Key terms and meanings')==1,n
    assert f'id="module-{n}-application"' in html,n
    assert f'href="#module-{n}-application"' in html,n
    assert f'id="module-{n}-source-details"' in html,n
assert expected==reader.blocks,'The rendered code differs from the source code.'
assert html.count('<figure')==11
assert len(re.findall(r'<h3 id="section-',html))==55
assert 'class="token keyword"' in html
assert 'class="token variable"' in html
assert 'code-theme.css?v=8' in html
assert '<script src="assets/prism' not in html,'Static notes must not require the runtime highlighter.'
class ProseReader(HTMLParser):
    def __init__(self):
        super().__init__();self.skip=0;self.text=[];self.controls=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('pre','code','script','style'):self.skip+=1
        if tag in ('button','input','textarea','select'):self.controls.append(tag)
    def handle_endtag(self,tag):
        if tag in ('pre','code','script','style'):self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.text.append(data)
prose=ProseReader();prose.feed(html)
visible=' '.join(prose.text)
assert '?' not in visible,'Use statements in the reading prose; retain question-mark syntax only in code and URLs.'
assert not prose.controls,'Keep quiz and study-state controls outside the notes.'
assert 'Situation 1' not in visible and 'Exam cue:' not in visible
print(f'Validated {len(expected)} exact code examples, 24 explanatory subsections, eight source guides, 55 sections, 11 figures, and reading prose without quiz prompts.')
