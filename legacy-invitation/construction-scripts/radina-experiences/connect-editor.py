from pathlib import Path
p=Path(__file__).resolve().parents[1]/'frontend/src/pages/admin/WeddingEditor.vue'
s=p.read_text(encoding='utf-8')
s=s.replace('import WeddingGiftManager', "import MusicSelector from '../../components/MusicSelector.vue'\nimport SectionManager from '../../components/SectionManager.vue'\nimport WeddingGiftManager",1)
s=s.replace("  ['template', 'Template'],", "  ['template', 'Template'],\n  ['sections', 'Section Manager'],")
s=s.replace("  result.gift_methods ||= []", "  result.section_content ||= {}\n  result.music.playlist ||= []\n  result.gift_methods ||= []")
s=s.replace("<template v-else-if=\"tab === 'music'\"", "<template v-else-if=\"tab === 'sections'\"><SectionManager v-model=\"form\" :template-key=\"previewWedding.template?.template_key\" /></template>\n        <template v-else-if=\"tab === 'music'\"",1)
s=s.replace('<h2>Soundtrack cerita Anda</h2>', '<h2>Soundtrack cerita Anda</h2><MusicSelector v-model="form.music" :wedding-id="form.id" :template-key="previewWedding.template?.template_key" />',1)
p.write_text(s,encoding='utf-8')
