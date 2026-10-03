from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
src=root/'frontend'/'src'
template=src/'templates'/'RomanticFloral'
shutil.copy2(template/'composables'/'useAudio.js',src/'composables'/'useAudio.js')
for path in (template/'components').glob('*.vue'):
    text=path.read_text(encoding='utf-8')
    text=text.replace("'./BaseModal.vue'","'../../../components/BaseModal.vue'").replace("'../composables/","'../../../composables/")
    path.write_text(text,encoding='utf-8')
path=template/'RomanticFloralTemplate.vue';text=path.read_text(encoding='utf-8').replace("'./components/BaseToast.vue'","'../../components/BaseToast.vue'").replace("'./composables/","'../../composables/");path.write_text(text,encoding='utf-8')
unused=[template/'components'/'BaseModal.vue',template/'components'/'BaseToast.vue',template/'components'/'WeddingRenderer.vue',template/'utils'/'weddingView.js',*(template/'composables').glob('*.js')]
for path in unused:
    assert path.resolve().is_relative_to(src.resolve())
    if path.exists():path.unlink()
archive=root/'legacy-invitation'/'construction-scripts';archive.mkdir(exist_ok=True)
for name in ['scaffold-platform.py','generate-models.py','prepare-template-engine.py','update-api-template.py','finalize-platform.py','polish-platform.py','configure-local-backend.php']:
    source=root/'scripts'/name;target=archive/name
    assert source.resolve().is_relative_to(root.resolve()) and target.resolve().is_relative_to(root.resolve())
    if source.exists():shutil.move(str(source),str(target))
print('Shared modal, toast, and composables consolidated; construction scripts archived.')
