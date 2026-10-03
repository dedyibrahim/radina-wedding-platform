from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
front=root/'frontend'/'src'
for file in ['layouts/PublicLayout.vue','layouts/AdminLayout.vue']:
    p=front/file;s=p.read_text(encoding='utf-8')
    s=s.replace('<Heart :size="20"/>{{ platform.settings.company_name','<img v-if="platform.settings.logo" :src="platform.settings.logo" alt="Logo"/><Heart v-else :size="20"/>{{ platform.settings.company_name')
    s=s.replace('<Heart :size="21"/>{{ platform.settings.company_name','<img v-if="platform.settings.logo" :src="platform.settings.logo" alt="Logo"/><Heart v-else :size="21"/>{{ platform.settings.company_name')
    p.write_text(s,encoding='utf-8')
p=front/'pages'/'public'/'Wedding.vue';s=p.read_text(encoding='utf-8');s=s.replace('v-if="route.meta.preview&&wedding"','v-if="(route.meta.preview||wedding?.is_demo)&&wedding"').replace(':preview="Boolean(route.meta.preview)"',':preview="Boolean(route.meta.preview||wedding.is_demo)"');p.write_text(s,encoding='utf-8')
p=front/'pages'/'admin'/'Templates.vue';s=p.read_text(encoding='utf-8').replace("price:149000,category_id:","price:0,category_id:");p.write_text(s,encoding='utf-8')
archive=root/'legacy-invitation';archive.mkdir(exist_ok=True)
for item in ['src','public','index.html','vite.config.js']:
    source=(root/item).resolve();target=(archive/item).resolve()
    assert source.is_relative_to(root.resolve()) and target.is_relative_to(root.resolve())
    if source.exists() and not target.exists():shutil.move(str(source),str(target))
(archive/'README.md').write_text('Original standalone Vue invitation retained as a source snapshot. The active full-stack platform is in ../frontend and ../backend.\n')
print('Platform branding, safe demo preview, and original source archive ready.')
