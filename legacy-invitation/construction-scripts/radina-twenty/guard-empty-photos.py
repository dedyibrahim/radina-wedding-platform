from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
for filename in ['Opening.vue','Hero.vue']:
 for path in (root/'frontend/src/templates').glob('*/'+filename):
  text=path.read_text(encoding='utf-8')
  text=re.sub(r'<img(?![^>]*\bv-if=)(?=[^>]*:src="wedding\.(cover|hero)(?:\s*\|\|\s*wedding\.cover)?")',lambda match: '<img v-if="wedding.'+match.group(1)+'"',text)
  path.write_text(text,encoding='utf-8')
