from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]/'frontend'/'src'
template=root/'templates'/'RomanticFloral'
template.mkdir(parents=True,exist_ok=True)
for folder in ['components','composables','utils']:
    shutil.copytree(root/folder,template/folder,dirs_exist_ok=True)
for path in (template/'components').glob('*.vue'):
    source=path.read_text(encoding='utf-8')
    if "import { wedding } from '../data/wedding'" in source:
        source=source.replace("import { wedding } from '../data/wedding'","import { inject } from 'vue'\nconst wedding = inject('wedding')")
    if path.name in ['WeddingCover.vue','HeroSection.vue','GallerySection.vue']:
        # CMS images may have arbitrary unique filenames; do not invent srcset variants.
        import re
        source=re.sub(r' :srcset="[^"]*" sizes="[^"]*"','',source)
    path.write_text(source,encoding='utf-8')
print('Romantic Floral components now consume injected API data.')
