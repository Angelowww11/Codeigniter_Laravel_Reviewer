"""Rebuild the deployed bank from the reviewed canonical question source."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'content.js').read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
questions = json.loads((ROOT / 'tools/question-bank.json').read_text(encoding='utf-8'))
assert len(questions) == 480
assert len({q['id'] for q in questions}) == 480
for module in range(1, 9):
    assert sum(q['module'] == module for q in questions) == 60

data['questions'] = questions
(ROOT / 'content.js').write_text('window.STUDY_DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n', encoding='utf-8')
print('Built 480 questions from tools/question-bank.json; 60 per module.')
