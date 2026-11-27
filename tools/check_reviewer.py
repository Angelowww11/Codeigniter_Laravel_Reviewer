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
    assert text.count('**Situation ')==3,n
    assert text.count('#### Key terms —')==1,n
    assert f'id="module-{n}-application"' in html,n
    assert f'href="#module-{n}-application"' in html,n
assert expected==reader.blocks,'The rendered code differs from the source code.'
assert html.count('<figure')==11
assert len(re.findall(r'<h3 id="section-',html))==55
assert 'class="token keyword"' in html
assert 'class="token variable"' in html
assert 'code-theme.css?v=8' in html
assert '<script src="assets/prism' not in html,'Static notes must not require the runtime highlighter.'
print(f'Validated {len(expected)} exact code examples, 24 worked situations, 55 sections, and 11 figures in static HTML.')
