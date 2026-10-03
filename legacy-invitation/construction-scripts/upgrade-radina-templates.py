from pathlib import Path
import json,re

def write(path,s):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def edit(path,a,b):
 p=Path(path);s=p.read_text(encoding='utf-8');assert a in s,path;p.write_text(s.replace(a,b),encoding='utf-8')
catalog=[('romantic-floral','RomanticFloral','Romantic Floral','Romantic','#f7f5ee','#6e7a60','Bunga watercolor, botanical halus, ivory dan dusty rose.','floral'),('elegant-luxury','ElegantLuxury','Elegant Luxury','Elegant','#241d19','#d7b477','Editorial mewah, monogram emas dan bingkai garis klasik.','luxury'),('minimalist-white','MinimalistWhite','Minimalist White','Minimalist','#ffffff','#79756c','White space, tipografi minimal dan fotografi yang jernih.','minimal'),('nusantara-heritage','NusantaraHeritage','Nusantara Heritage','Traditional','#f8ecda','#792e36','Motif geometris terinspirasi Nusantara, maroon dan emas.','heritage'),('garden-dream','GardenDream','Garden Dream','Romantic','#f1f5eb','#526c4b','Arch taman, daun sage dan suasana outdoor yang hangat.','garden'),('classic-vintage','ClassicVintage','Classic Vintage','Elegant','#efe2cd','#715542','Tekstur kertas, foto sepia dan bingkai kartu pos klasik.','vintage'),('midnight-romance','MidnightRomance','Midnight Romance','Modern','#18191e','#d6a093','Burgundy, charcoal dan fotografi kontras dalam layout modern.','midnight'),('sakinah','Sakinah','Sakinah','Traditional','#faf6e9','#647659','Bingkai arch, pola geometris halus dan palet ivory hijau.','sakinah'),('eternal-story','EternalStory','Eternal Story','Modern','#151718','#ddcbb1','Foto layar penuh dan bab cerita cinta bergaya sinematik.','cinematic'),('blush','Blush','Blush','Modern','#fff1f4','#94607c','Gradient pink lavender, kartu lembut dan tipografi modern.','blush')]
# Fixed registry. API cannot supply executable paths.
imports='\n'.join(f"  '{key}': defineAsyncComponent(() => import('./{folder}/index.vue'))," for key,folder,*_ in catalog)
write('frontend/src/templates/templateRegistry.js',f"import {{ defineAsyncComponent }} from 'vue'\nexport const templateRegistry = {{\n{imports}\n}}\nexport const templateOptions = "+json.dumps([{'value':k,'label':n,'component':f+'.vue'} for k,f,n,*_ in catalog])+"\n")
write('backend/app/Services/TemplateCatalog.php',"<?php\nnamespace App\\Services;\nclass TemplateCatalog { public const KEYS = "+str([x[0] for x in catalog]).replace("[","[").replace("]","]")+"; public const COMPONENTS = "+str(['RomanticFloralTemplate.vue']+[x[1]+'.vue' for x in catalog])+"; }\n")
edit('backend/app/Http/Requests/SaveTemplateRequest.php',"Rule::in(['RomanticFloralTemplate.vue'])", "Rule::in(\\App\\Services\\TemplateCatalog::COMPONENTS)")
edit('backend/app/Http/Requests/SaveTemplateRequest.php',"'is_featured' =>", "'template_key' => ['required', Rule::in(\\App\\Services\\TemplateCatalog::KEYS)],\n            'is_featured' =>")
write('backend/database/seeders/RadinaSeeder.php', '''<?php
namespace Database\Seeders;
use Illuminate\Database\Seeder;
use App\Models\Template;
use App\Models\TemplateCategory;
class RadinaSeeder extends Seeder {
 public function run(): void {
  $catalog = '''+json.dumps([[k,f,n,c,d] for k,f,n,c,b,a,d,t in catalog],ensure_ascii=False).replace('[','[').replace(']',']')+''';
  foreach($catalog as [$key,$folder,$name,$category,$description]){
   $cat=TemplateCategory::firstOrCreate(['slug'=>strtolower($category)],['name'=>$category]);
   $template=Template::firstOrCreate(['slug'=>$key],['category_id'=>$cat->id,'name'=>$name,'description'=>$description,'price'=>149000,'component_name'=>$folder.'.vue','template_key'=>$key,'status'=>'ACTIVE','is_featured'=>in_array($key,['romantic-floral','elegant-luxury','garden-dream']),'thumbnail'=>'/images/templates/'.$key.'.svg','preview_image'=>'/images/templates/'.$key.'.svg','features'=>['Musik latar','RSVP & ucapan','Galeri foto','Wedding gift','CMS bersama','Responsive']]);
   if($template->template_key==='romantic-floral' && $key!=='romantic-floral')$template->update(['template_key'=>$key]);
  }
 }
}
''')
# PHP arrays above are valid JSON-like PHP except JSON syntax uses only strings and arrays here.
edit('backend/database/seeders/DatabaseSeeder.php',"        $existing = Order::where", "        $this->call(RadinaSeeder::class);\n        $existing = Order::where")
# Brand assets and theme-specific catalog artwork use safe built-in SVGs.
for key,folder,name,category,bg,accent,description,theme in catalog:
 ornament=''
 if theme in ['floral','garden']:
  for x,y in [(50,110),(365,410),(95,400)]:
   ornament+=f'<g transform="translate({x} {y})" fill="{accent}" opacity=".28">'+''.join(f'<ellipse cy="-18" rx="10" ry="24" transform="rotate({i*60})"/>' for i in range(6))+'</g>'
 elif theme=='heritage':ornament=f'<path d="M10 30L30 10L50 30L30 50ZM350 490L370 470L390 490L370 510Z" fill="none" stroke="{accent}" stroke-width="3"/>'
 elif theme=='sakinah':ornament=f'<path d="M90 390V200Q90 90 200 50Q310 90 310 200V390" fill="none" stroke="{accent}" stroke-width="2"/>'
 elif theme=='blush':ornament='<circle cx="70" cy="60" r="110" fill="#ddd0ef" opacity=".65"/><circle cx="370" cy="460" r="125" fill="#f3c6d1" opacity=".65"/>'
 else:ornament=f'<rect x="28" y="28" width="344" height="464" rx="{70 if theme=="midnight" else 0}" fill="none" stroke="{accent}" opacity=".55"/>'
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 520"><rect width="400" height="520" fill="{bg}"/>{ornament}<text x="200" y="158" text-anchor="middle" fill="{accent}" font-family="Arial" font-size="10" letter-spacing="4">RADINA COLLECTION</text><text x="200" y="236" text-anchor="middle" fill="{accent}" font-family="Georgia" font-size="45">Alya</text><text x="200" y="276" text-anchor="middle" fill="{accent}" font-family="Georgia" font-size="30">&amp;</text><text x="200" y="325" text-anchor="middle" fill="{accent}" font-family="Georgia" font-size="45">Rizky</text><text x="200" y="379" text-anchor="middle" fill="{accent}" font-family="Arial" font-size="10" letter-spacing="3">12 DECEMBER 2026</text><text x="200" y="453" text-anchor="middle" fill="{accent}" font-family="Georgia" font-size="18">{name}</text></svg>'''
 write('frontend/public/images/templates/'+key+'.svg',svg)
 write(f'frontend/src/templates/{folder}/index.vue',f'''<script setup>
import WeddingExperience from '../shared/WeddingExperience.vue'
defineProps({{ wedding: {{ type: Object, required: true }}, preview: Boolean }})
</script><template><WeddingExperience :wedding="wedding" :preview="preview" theme="{theme}" /></template>
''')
# Move presentation orchestration to shared engine without duplicating business logic.
s=Path('frontend/src/templates/RomanticFloral/RomanticFloralTemplate.vue').read_text();s=s.replace("from './components/","from '../RomanticFloral/components/");s=s.replace('ref, provide, nextTick, onUnmounted, watch','ref, reactive, provide, inject, nextTick, onUnmounted, watch');s=s.replace('preview: Boolean })','preview: Boolean, theme: { type: String, default: \'floral\' } })');s=s.replace('const wedding = weddingView(props.wedding)',"const wedding = reactive(weddingView(props.wedding))\nwatch(() => props.wedding, (value) => Object.assign(wedding, weddingView(value)), { deep: true })");s=s.replace('const opened = ref(false),',"const opened = inject('invitationOpened', ref(false)),");s=s.replace('<div class="wedding-page">','<div class="wedding-page" :class="`theme-${theme}`">');write('frontend/src/templates/shared/WeddingExperience.vue',s)
write('frontend/src/components/WeddingRenderer.vue', '''<script setup>
import { computed, ref, provide } from 'vue'
import { templateRegistry } from '../templates/templateRegistry'
const props = defineProps({ wedding: { type: Object, required: true }, preview: Boolean })
const invitationOpened = ref(false)
provide('invitationOpened', invitationOpened)
const selectedTemplate = computed(() => templateRegistry[props.wedding.template?.template_key || 'romantic-floral'])
defineExpose({ showCover: () => { invitationOpened.value = false }, showInvitation: () => { invitationOpened.value = true } })
</script><template><component v-if="selectedTemplate" :is="selectedTemplate" :wedding="wedding" :preview="preview" /><div v-else class="page-state">Template belum tersedia. Hubungi administrator.</div></template>
''')
# Event IDs are semantic, not database identities.
for filename,key in [('EventSection.vue','event'),('LoveStory.vue','story'),('ClosingSection.vue','closing')]:
 p=Path('frontend/src/templates/RomanticFloral/components/'+filename);s=p.read_text();s=re.sub(r'<section([^>]*?) id="[^"]+"',f'<section\\1 id="{key}"',s,count=1) if 'id="' in s.split('<section',1)[-1].split('>',1)[0] else s.replace('<section ',f'<section id="{key}" ',1);p.write_text(s)
# Prevent hash navigation entirely, keep query guest untouched, consistent main + More navigation.
p=Path('frontend/src/templates/RomanticFloral/components/FloatingNavigation.vue');s=p.read_text();s=s.replace("import { House, Heart, CalendarDays, Images, MailCheck }", "import { House, Heart, CalendarDays, Images, Gift, Ellipsis }");s=s.replace("const wedding = inject('wedding')", "import { scrollToSection } from '../../../composables/useSectionNavigation'\nconst more = ref(false)\nconst wedding = inject('wedding')")
a=s.index('const items = [');b=s.index("const active =",a)
s=s[:a]+'''const items = [
 {id:'home',label:'Home',icon:House}, {id:'couple',label:'Couple',icon:Heart},
 {id:'event',label:'Event',icon:CalendarDays}, {id:'gallery',label:'Gallery',icon:Images},
 {id:'gift',label:'Gift',icon:Gift}
].filter(item => item.id==='event' ? wedding.events.length : item.id==='gallery' ? wedding.settings.enable_gallery && wedding.gallery.length : item.id==='gift' ? wedding.settings.enable_gift && wedding.giftMethods.length : true)
function navigate(key) { active.value = key; more.value=false; scrollToSection(key) }
''' + s[b:]
a=s.index('<template>');s=s[:a]+'''<template>
 <nav class="floating-nav" aria-label="Navigasi undangan">
  <button v-for="item in items" :key="item.id" :class="{active:active===item.id}" :aria-current="active===item.id ? 'location' : undefined" @click="navigate(item.id)"><component :is="item.icon" :size="18"/><span>{{item.label}}</span></button>
  <button aria-label="Section lainnya" :aria-expanded="more" @click="more=!more"><Ellipsis :size="18"/><span>More</span></button>
  <div v-if="more" class="wedding-more-menu">
   <button v-if="wedding.settings.enable_story && wedding.loveStory.length" @click="navigate('story')">Story</button>
   <button v-if="wedding.settings.enable_rsvp" @click="navigate('rsvp')">RSVP</button>
   <button v-if="wedding.settings.enable_wishes" @click="navigate('wishes')">Wishes</button>
  </div>
 </nav>
</template>
''';p.write_text(s)
# New shared gift contract; existing legacy bank data remains for old API consumers.
edit('frontend/src/utils/weddingView.js','    bankAccounts:', "    giftMethods: (data.gift_methods || []).filter(g => g.is_active),\n    bankAccounts:")
edit('frontend/src/templates/RomanticFloral/components/InvitationContent.vue','(wedding.bankAccounts.length || wedding.giftAddress)','wedding.giftMethods.length')
# Stable admin preview section controls, public demo retains interactive cover.
p=Path('frontend/src/pages/public/Wedding.vue');s=p.read_text();s=s.replace('ArrowLeft, ArrowUpRight','ArrowLeft, ArrowUpRight');s=s.replace("const route = useRoute(),","import RadinaLogo from '../../components/RadinaLogo.vue'\nimport { nextTick } from 'vue'\nimport { scrollToSection } from '../../composables/useSectionNavigation'\nconst renderer = ref(null)\nasync function previewSection(key) {\n if (key === 'cover') { renderer.value?.showCover(); window.scrollTo({top:0}); return }\n renderer.value?.showInvitation(); await nextTick(); setTimeout(() => scrollToSection(key), 400)\n}\nconst route = useRoute(),");s=s.replace('<span>Pratinjau ·','<RadinaLogo iconOnly /><span>Pratinjau ·');s=s.replace('    <WeddingRenderer','    <div v-if="route.params.id && wedding" class="preview-controls"><button v-for="item in [[\'cover\',\'Preview Cover\'],[\'couple\',\'Couple\'],[\'event\',\'Event\'],[\'gallery\',\'Gallery\'],[\'gift\',\'Gift\'],[\'closing\',\'Closing\']]" :key="item[0]" @click="previewSection(item[0])">{{item[1]}}</button></div>\n    <WeddingRenderer');s=s.replace('      :wedding="wedding"','      ref="renderer"\n      :wedding="wedding"');p.write_text(s)
# Admin component picker uses registered entries only.
edit('frontend/src/pages/admin/Templates.vue','<script setup>','<script setup>\nimport { templateOptions } from \'../../templates/templateRegistry\'')
edit('frontend/src/pages/admin/Templates.vue',"      component_name: 'RomanticFloralTemplate.vue',", "      component_name: 'RomanticFloralTemplate.vue', template_key: 'romantic-floral',")
edit('frontend/src/pages/admin/Templates.vue','      ...form,',"      ...form, template_key: templateOptions.find(x=>x.component===form.component_name)?.value || 'romantic-floral',")
edit('frontend/src/pages/admin/Templates.vue',":options=\"[{ value: 'RomanticFloralTemplate.vue', label: 'Romantic Floral' }]\"", ':options="templateOptions.map(x=>({value:x.component,label:x.label}))"')
write('frontend/src/assets/styles/themes.css', '''/* Each design shares behavior and content, with its own composition and ornament language. */
.wedding-page{--theme-bg:var(--ivory);--theme-ink:var(--ink)}
.wedding-page .floating-nav button{display:flex;flex:1;flex-direction:column;align-items:center;gap:5px;min-width:0;min-height:48px;padding:7px 3px;background:transparent;color:inherit;font-size:9px;border-radius:24px}.wedding-page .floating-nav button.active{background:var(--cream);color:var(--ink)}.wedding-more-menu{position:absolute;bottom:calc(100% + 8px);right:0;background:var(--ivory);color:var(--ink);border:1px solid var(--gold);border-radius:20px;padding:12px;display:flex;gap:8px;box-shadow:0 12px 30px #0002}.wedding-more-menu button{padding:10px!important;font-size:12px!important}.wedding-page .section{background:var(--ivory);color:var(--ink)}.wedding-page .invitation-shell{background:var(--ivory)}
.theme-luxury{--ivory:#241d19;--cream:#302720;--ink:#f1e0c4;--sage:#cfac74;--gold:#d7b477}.theme-luxury .hero-image-wrap{border-radius:0;border:1px solid var(--gold);padding:12px;width:85%}.theme-luxury .hero-image-wrap img{border-radius:0}.theme-luxury .hero-title h1{font-size:clamp(3rem,11vw,5.8rem);text-transform:uppercase;letter-spacing:4px}.theme-luxury .section{border-bottom:1px solid #d7b47744}.theme-luxury .section-heading:before{content:'◆';display:block;color:var(--gold);margin-bottom:15px}.theme-luxury .flower-motion,.theme-luxury .hero-floral{display:none}.theme-luxury .event-card{border:1px solid var(--gold);border-radius:0;background:transparent}.theme-luxury .desktop-ambience{background:radial-gradient(ellipse,#655035,#16110e)}
.theme-minimal{--ivory:#fff;--cream:#f5f3ee;--ink:#3e3d3b;--sage:#79756c;--gold:#b6a991}.theme-minimal .flower-motion,.theme-minimal .botanical-ornament,.theme-minimal .hero-floral,.theme-minimal .hero-top{display:none}.theme-minimal .hero-image-wrap{border-radius:0;width:calc(100% - 48px);aspect-ratio:4/5}.theme-minimal .hero-image-wrap img{border-radius:0}.theme-minimal .hero-title h1{font-size:clamp(3rem,12vw,5rem);font-weight:300}.theme-minimal .section{padding-block:85px}.theme-minimal .event-card,.theme-minimal .bank-card{border-radius:0;border:0;border-top:1px solid #ddd;background:transparent}.theme-minimal .section-heading .eyebrow{letter-spacing:4px}.theme-minimal .desktop-ambience{background:#f2f1ed}
.theme-heritage{--ivory:#f8ecda;--cream:#ead7b9;--ink:#5b272b;--sage:#792e36;--gold:#b38a48}.theme-heritage .flower-motion{display:none}.theme-heritage .section:before{content:'';position:absolute;left:12px;right:12px;top:0;height:9px;background:repeating-linear-gradient(45deg,transparent 0 8px,#b38a4870 8px 10px,transparent 10px 18px)}.theme-heritage .hero-image-wrap{border-radius:140px 140px 4px 4px;border:6px double var(--gold);padding:8px}.theme-heritage .hero-title h1{color:#792e36}.theme-heritage .event-card{border:4px double var(--gold);border-radius:0;background:#f8ecda}.theme-heritage .desktop-ambience{background:repeating-linear-gradient(45deg,#5b272b,#5b272b 30px,#662d32 30px,#662d32 32px)}
.theme-garden{--ivory:#f1f5eb;--cream:#e3ead9;--ink:#34482f;--sage:#526c4b;--gold:#a1aa7d}.theme-garden .hero-image-wrap{border-radius:50% 50% 5px 5px;border:9px double #a1aa7d;padding:7px}.theme-garden .section{background-image:radial-gradient(ellipse at 0 100%,#c5d9b540,transparent 50%)}.theme-garden .couple-grid{gap:45px}.theme-garden .bride-portrait,.theme-garden .groom-portrait{border-radius:50%}.theme-garden .event-card{background:#fff9;border-radius:120px 120px 12px 12px;padding-top:50px}.theme-garden .desktop-ambience{background:radial-gradient(ellipse,#e3ead9,#b3c5a3)}
.theme-vintage{--ivory:#efe2cd;--cream:#e3d0b3;--ink:#604938;--sage:#715542;--gold:#ad8b60}.theme-vintage .section{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' opacity='.06' filter='url(%23n)'/%3E%3C/svg%3E")}.theme-vintage .hero-image-wrap{border-radius:0;border:10px solid #fff7e6;box-shadow:0 5px 20px #60493830;transform:rotate(-3deg);width:76%}.theme-vintage .hero-image-wrap img{border-radius:0;filter:sepia(.45)}.theme-vintage .flower-motion{display:none}.theme-vintage .event-card{border:3px double var(--gold);border-radius:0;background:transparent}.theme-vintage .gallery-grid img{filter:sepia(.35)}.theme-vintage .section-heading h2{font-style:italic}.theme-vintage .desktop-ambience{background:#cbb797}
.theme-midnight{--ivory:#18191e;--cream:#25232b;--ink:#f5e5df;--sage:#d6a093;--gold:#bf8b76}.theme-midnight .hero-image-wrap{width:calc(100% - 24px);border-radius:160px 8px 160px 8px;aspect-ratio:3/4}.theme-midnight .hero-image-wrap img{border-radius:160px 8px 160px 8px;filter:contrast(1.15)}.theme-midnight .flower-motion,.theme-midnight .hero-floral{display:none}.theme-midnight .hero-title h1{font-family:var(--serif);font-size:clamp(3.2rem,14vw,6rem)}.theme-midnight .section{background-image:radial-gradient(ellipse at top,#482a3540,transparent 65%)}.theme-midnight .event-card,.theme-midnight .bank-card{background:#25232b;border:1px solid #bf8b7660}.theme-midnight .desktop-ambience{background:radial-gradient(ellipse,#482a35,#121317)}
.theme-sakinah{--ivory:#faf6e9;--cream:#eae9d7;--ink:#43513a;--sage:#647659;--gold:#baa269}.theme-sakinah .flower-motion{display:none}.theme-sakinah .hero-image-wrap{border-radius:50% 50% 0 0;border:5px double var(--gold);padding:7px}.theme-sakinah .section-heading:before{content:'✧';font-size:35px;color:var(--gold)}.theme-sakinah .section{background-image:radial-gradient(circle at 10px 10px,#baa26920 1px,transparent 1px);background-size:24px 24px}.theme-sakinah .event-card{border-radius:100px 100px 8px 8px;border:1px solid var(--gold);padding-top:48px;background:#faf6e9}.theme-sakinah .desktop-ambience{background:#d8dec9}
.theme-cinematic{--ivory:#151718;--cream:#222628;--ink:#f1e9dd;--sage:#ddcbb1;--gold:#b79b78}.theme-cinematic .hero-section{padding:0;position:relative;isolation:isolate;justify-content:center}.theme-cinematic .hero-image-wrap{position:absolute;inset:0;z-index:-2;width:100%;height:100%;border-radius:0;aspect-ratio:auto}.theme-cinematic .hero-image-wrap img{height:100%;width:100%;border-radius:0;object-fit:cover}.theme-cinematic .hero-section:after{content:'';position:absolute;inset:0;background:linear-gradient(#0005,#0002,#000b);z-index:-1;pointer-events:none}.theme-cinematic .hero-title,.theme-cinematic .hero-top,.theme-cinematic .hero-bottom{color:white;z-index:1}.theme-cinematic .hero-title{margin:auto 0 10px}.theme-cinematic .hero-bottom{margin-top:auto}.theme-cinematic .hero-floral,.theme-cinematic .flower-motion{display:none}.theme-cinematic .invitation-content{display:flex;flex-direction:column}.theme-cinematic .hero-section{order:-3}.theme-cinematic .story-section{order:-2}.theme-cinematic .quote-section{order:-1}.theme-cinematic .timeline-item{padding-block:25px}.theme-cinematic .section-heading h2{font-size:clamp(2.8rem,10vw,4.7rem)}.theme-cinematic .event-card,.theme-cinematic .bank-card{background:#222628;border-color:#b79b78}.theme-cinematic .desktop-ambience{background:#16191b}
.theme-blush{--ivory:#fff1f4;--cream:#f4e2ef;--ink:#684d65;--sage:#94607c;--gold:#bd8aa1}.theme-blush .section{background-image:radial-gradient(ellipse at 90% 10%,#ded0ed80,transparent 60%)}.theme-blush .hero-image-wrap{width:80%;border-radius:38% 62% 48% 52% / 50% 45% 55% 50%;border:8px solid #ffffff80}.theme-blush .hero-image-wrap img{border-radius:inherit}.theme-blush .hero-title h1{font-size:clamp(3.5rem,15vw,6rem)}.theme-blush .flower-motion{opacity:.65}.theme-blush .event-card,.theme-blush .bank-card{border:0;background:#fff9;border-radius:28px;box-shadow:0 10px 25px #94607c0d}.theme-blush .desktop-ambience{background:linear-gradient(135deg,#f6d8df,#ded4ef,#dceaf0)}
.wedding-page .bank-number{color:var(--ink)}.wedding-page .bank-owner,.wedding-page .section-subtitle,.wedding-page .event-detail,.wedding-page .event-venue,.wedding-page .story-section p{color:var(--ink)}.wedding-page .hero-image-wrap{max-width:100%}.wedding-page .section,.wedding-page .hero-title{overflow-wrap:anywhere}.wedding-page .bank-card{min-width:0}.wedding-page .gift-section .button{max-width:100%}
@media(max-width:359px){.wedding-page .floating-nav button{font-size:8px;padding-inline:1px}.radina-gift-tabs button{font-size:11px;padding:8px 10px}.theme-luxury .hero-title h1{letter-spacing:1px}.wedding-page .section{padding-inline:22px}}
@media(prefers-reduced-motion:reduce){.wedding-page *{animation:none!important;scroll-behavior:auto!important;transition:none!important}}
''')
edit('frontend/src/main.js',"import './assets/styles/platform.css'","import './assets/styles/platform.css'\nimport './assets/styles/themes.css'")
