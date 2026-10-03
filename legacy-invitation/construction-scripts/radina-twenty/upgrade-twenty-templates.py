"""Add developer-managed presentations; never reads or changes customer data."""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
base = root / 'frontend/src/templates'
items = [
 ('celestial','Celestial','Celestial','Dreamy','Luna','Rayhan','#111d39','#f4f5ff','#b9c7ef','Begin Our Journey','Two souls, written in the stars.','Moonlight Observatory',['Ambient','Piano']),
 ('editorial','Editorial','Editorial','Modern','Bianca','Julian','#faf8f3','#191919','#79716c','Read Our Issue','A new issue. A lifetime together.','The Editorial Atelier',['Classic','Modern']),
 ('ocean-vows','OceanVows','Ocean Vows','Destination','Marina','Rio','#eef8fa','#17465a','#70b6c8','Open Invitation','Where the horizon meets our forever.','Oceanfront Pavilion',['Acoustic','Instrumental']),
 ('royal-heritage','RoyalHeritage','Royal Heritage','Luxury','Aurelia','Alexander','#113b32','#fff6df','#c7aa61','Open the Gates','A celebration worthy of our shared history.','Royal Conservatory',['Classic','Instrumental']),
 ('paper-petals','PaperPetals','Paper & Petals','Romantic','Hana','Theo','#f5ead9','#604737','#ad8e77','Untie Ribbon','Small notes, pressed petals, endless love.','The Paper Garden',['Acoustic','Piano']),
 ('botanica','Botanica','Botanica','Destination','Maya','Rafael','#e9eee3','#213e32','#ad7552','Discover Our Day','An island escape, a promise to stay.','Palm Retreat',['Acoustic','Traditional']),
 ('monochrome','Monochrome','Monochrome','Minimalist','Alena','Nathan','#f5f5f5','#121212','#777777','Reveal Our Story','Life in contrast. Love in focus.','Studio Twenty',['Piano','Classic']),
 ('blossom-east','BlossomEast','Blossom East','Traditional','Reina','Kenji','#faf2e7','#352d29','#a4544d','Open Invitation','Like a blossom, love arrives in its own time.','Blossom Art House',['Instrumental','Ambient']),
 ('neon-love','NeonLove','Neon Love','Modern','Kiara','Ezra','#111126','#f4edff','#d889cf','Enter Wedding','Two hearts. One city. Our electric moment.','The Skyline Loft',['Modern','Cinematic']),
 ('timeless-romance','TimelessRomance','Timeless Romance','Romantic','Eleanor','William','#f6efdf','#4e2932','#aa8d56','Open Invitation','Some promises never go out of style.','Maison de Romance',['Classic','Piano']),
]
def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def sfc(markup,extra=''):
 return '<script setup>\nimport { inject } from "vue"\nimport SectionHeading from "../RomanticFloral/components/SectionHeading.vue"\nconst wedding = inject("wedding")\n'+extra+'\n</script>\n<template>\n'+markup+'\n</template>\n'
names='<h1>{{ wedding.bride.shortName }} <i>&</i> {{ wedding.groom.shortName }}</h1>'
photo='<img :src="wedding.cover" alt="Foto pasangan" fetchpriority="high" />'
guest='<div class="new-cover-guest"><small>Kepada Yth. Bapak/Ibu/Saudara/i</small><strong class="cover-guest">{{ guest }}</strong><button class="button" aria-label="Buka Undangan" @click="$emit(\'open\')">LABEL ↗</button></div>'
covers=[
 '<div class="sky-speckles" aria-hidden="true"></div><span class="crescent" aria-hidden="true">☾</span><div class="orbit-photo">'+photo+'</div><div class="sky-title"><small>WRITTEN IN THE STARS</small>'+names+'<p>{{ wedding.openingText }}</p></div>',
 '<header class="issue-masthead"><small>VOL. 01 · {{ wedding.date.year }}</small><h2>THE<br>WEDDING<br>ISSUE</h2>'+names+'</header><figure class="issue-cover">'+photo+'<figcaption>{{ wedding.date.display }}</figcaption></figure>',
 '<div class="ocean-cover-photo">'+photo+'</div><div class="horizon-title"><small>AT THE EDGE OF FOREVER</small>'+names+'<p>{{ wedding.openingText }}</p></div><div class="wave-line" aria-hidden="true"></div>',
 '<div class="royal-door left" aria-hidden="true"></div><div class="royal-door right" aria-hidden="true"></div><div class="royal-crest"><span>{{ wedding.bride.shortName[0] }} · {{ wedding.groom.shortName[0] }}</span><small>CORDIALLY INVITED</small>'+names+'<p>{{ wedding.date.display }}</p></div>',
 '<div class="paper-stack"><span class="ribbon" aria-hidden="true"></span><small>A LITTLE NOTE FOR YOU</small>'+names+'<p>{{ wedding.openingText }}</p><figure>'+photo+'</figure></div>',
 '<div class="resort-window">'+photo+'</div><div class="palm-leaves" aria-hidden="true">❧<span>❧</span></div><header class="resort-title"><small>OUR DESTINATION · TOGETHER</small>'+names+'<p>{{ wedding.date.display }}</p></header>',
 '<div class="contrast-intro"><small>A DOCUMENTARY OF US</small>'+names+'</div><figure class="contrast-reveal">'+photo+'</figure>',
 '<div class="ink-branch" aria-hidden="true">✿<span>╱</span>✿</div><header class="ink-title"><small>A PROMISE IN BLOOM</small>'+names+'<p>{{ wedding.openingText }}</p></header><figure class="ink-photo">'+photo+'</figure>',
 '<div class="city-cover">'+photo+'</div><div class="neon-title"><small>SAVE OUR NIGHT</small><h1>{{ wedding.bride.shortName }}<span>+</span>{{ wedding.groom.shortName }}</h1><p>{{ wedding.date.display }}</p></div>',
 '<div class="classic-invitation"><small>YOU ARE WARMLY INVITED TO</small>'+names+'<div class="classic-rule" aria-hidden="true">❦</div><p>{{ wedding.openingText }}</p><p>{{ wedding.date.display }}</p></div>',
]
hero_parts=[
 '<div class="constellation-hero"><img :src="wedding.hero" alt="Momen pasangan"><span aria-hidden="true">✧</span>'+names+'</div>',
 '<header class="edition-title"><b>VOL. 01</b>'+names+'<span>{{ wedding.date.display }}</span></header><figure class="editorial-full"><img :src="wedding.hero" alt="Momen pasangan"><figcaption>THE PEOPLE · THE PROMISE · THE CELEBRATION</figcaption></figure>',
 '<figure class="ocean-horizon"><img :src="wedding.hero" alt="Momen pasangan">'+names+'<div class="wave-line" aria-hidden="true"></div></figure>',
 '<div class="royal-portrait"><span class="crest-mini">♧</span><img :src="wedding.hero" alt="Momen pasangan">'+names+'</div>',
 '<div class="handmade-hero"><div class="paper-note"><small>WE SAVED YOU A PLACE</small>'+names+'</div><figure><img :src="wedding.hero" alt="Momen pasangan"><figcaption>{{ wedding.date.display }}</figcaption></figure><span class="pressed-petal" aria-hidden="true">✿</span></div>',
 '<figure class="resort-hero"><img :src="wedding.hero" alt="Momen pasangan"><div><small>THE DESTINATION EDITION</small>'+names+'</div></figure>',
 '<figure class="documentary-hero"><img :src="wedding.hero" alt="Momen pasangan"><figcaption>'+names+'<span>{{ wedding.date.display }}</span></figcaption></figure>',
 '<div class="art-hero"><div>'+names+'<p>{{ wedding.openingText }}</p></div><figure><img :src="wedding.hero" alt="Momen pasangan"></figure><span aria-hidden="true">✿</span></div>',
 '<figure class="urban-hero"><img :src="wedding.hero" alt="Momen pasangan"><div><small>THIS CITY. THIS LOVE.</small>'+names+'</div><span class="city-coordinate">{{ wedding.date.display }}</span></figure>',
 '<header class="european-title"><small>A CELEBRATION OF LOVE</small>'+names+'</header><div class="european-triptych"><img :src="wedding.hero" alt="Momen pasangan"><img v-for="image in wedding.gallery.slice(0,2)" :key="image.src" :src="image.src" :alt="image.alt" loading="lazy"></div>',
]
bio='<h3>{{ person.name }}</h3><p>{{ person.order }}</p><p>{{ person.father }} <span v-if="person.father && person.mother">&</span> {{ person.mother }}</p><a v-if="person.instagram" :href="`https://instagram.com/${person.instagram}`" target="_blank" rel="noopener noreferrer">@{{ person.instagram }}</a>'
portrait='<img v-if="person.photo" :src="person.photo" :alt="person.name" loading="lazy">'
couples=[
 '<div class="people-constellation"><article v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><span class="star-index">✦ {{ i+1 }}</span><figure>'+portrait+'</figure><div>'+bio+'</div></article><span class="constellation-link" aria-hidden="true">✧ ─── ✧</span></div>',
 '<article class="interview-spread" v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><header><b>{{ i===0 ? "BRIDE 01" : "GROOM 02" }}</b><span>MEET THE PEOPLE</span></header><figure>'+portrait+'<figcaption>{{ person.shortName }} · IN CONVERSATION</figcaption></figure><div class="interview-biography">'+bio+'</div></article>',
 '<div class="shoreline-people"><article v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><div class="wave-portrait">'+portrait+'</div><div class="shoreline-biography"><small>{{ i===0?"HER SHORE":"HIS SHORE" }}</small>'+bio+'</div></article></div>',
 '<div class="royal-family"><article v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><div class="crest-mini">{{ person.shortName[0] }}</div><figure>'+portrait+'</figure><div class="royal-lineage">'+bio+'</div></article><span class="royal-union" aria-hidden="true">&</span></div>',
 '<div class="polaroid-pair"><article v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><figure><span class="paper-tape" aria-hidden="true"></span>'+portrait+'<figcaption>{{ person.shortName }}</figcaption></figure><div class="journal-biography">'+bio+'</div></article></div>',
 '<div class="tropical-people"><article v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><figure>'+portrait+'<span class="palm-shadow" aria-hidden="true">❧</span></figure><aside><small>THE {{ i===0?"BRIDE":"GROOM" }}</small>'+bio+'</aside></article></div>',
 '<div class="documentary-people"><article v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><figure>'+portrait+'<figcaption>PORTRAIT {{ String(i+1).padStart(2,"0") }} / {{ person.shortName }}</figcaption></figure><div class="documentary-caption">'+bio+'</div></article></div>',
 '<div class="blossom-portraits"><article v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><figure>'+portrait+'<span aria-hidden="true">✿</span></figure><div class="ink-biography"><small>{{ i===0?"THE BRIDE":"THE GROOM" }}</small>'+bio+'</div></article></div>',
 '<div class="city-posters"><article v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><figure>'+portrait+'<figcaption><b>{{ person.shortName }}</b><small>LOVE / {{ i+1 }}</small></figcaption></figure><div class="poster-notes">'+bio+'</div></article></div>',
 '<div class="classic-portraits"><article v-for="(person,i) in [wedding.bride,wedding.groom]" :key="i" data-reveal><small>PORTRAIT OF THE {{ i===0?"BRIDE":"GROOM" }}</small><figure>'+portrait+'</figure><div>'+bio+'</div><span aria-hidden="true">❦</span></article></div>',
]
story_content='<h3>{{ chapter.title }}</h3><p>{{ chapter.text }}</p>'
story_photo='<img v-if="chapter.image" :src="chapter.image" :alt="chapter.title" loading="lazy">'
stories=[
 '<div class="star-map-timeline"><article v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal><span class="story-star">✦</span><small>{{ chapter.year }}</small><div>'+story_content+'</div>'+story_photo+'</article></div>',
 '<div class="article-chapters"><article v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal><header><span>CHAPTER {{ String(i+1).padStart(2,"0") }}</span><b>{{ chapter.year }}</b></header><div class="article-columns">'+story_content+'</div><figure>'+story_photo+'<figcaption>{{ chapter.year }} · OUR ARCHIVE</figcaption></figure></article></div>',
 '<div class="tidal-journey"><article v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal><span class="wave-marker" aria-hidden="true">≈</span><figure>'+story_photo+'</figure><div><small>{{ chapter.year }}</small>'+story_content+'</div></article></div>',
 '<ol class="royal-chronicle"><li v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal><span class="chronicle-seal">{{ i+1 }}</span><time>{{ chapter.year }}</time><div>'+story_content+'</div><figure>'+story_photo+'</figure></li></ol>',
 '<div class="pressed-journal"><article v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal><div class="journal-date"><span>{{ chapter.year }}</span><small>NOTE {{ i+1 }}</small></div><figure>'+story_photo+'<span class="paper-tape" aria-hidden="true"></span></figure><div class="journal-entry">'+story_content+'</div></article></div>',
 '<div class="island-path"><article v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal><span class="path-number">{{ i+1 }}</span><div class="travel-caption"><time>{{ chapter.year }}</time>'+story_content+'</div><figure>'+story_photo+'</figure></article></div>',
 '<div class="documentary-archive"><figure v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal>'+story_photo+'<figcaption><header><b>{{ chapter.year }}</b><span>ARCHIVE / {{ i+1 }}</span></header>'+story_content+'</figcaption></figure></div>',
 '<div class="brush-scroll"><article v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal><time>{{ chapter.year }}</time><span class="ink-dot" aria-hidden="true">●</span><div>'+story_content+'</div><figure>'+story_photo+'</figure></article></div>',
 '<div class="metro-route"><article v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal><span class="metro-station">{{ String(i+1).padStart(2,"0") }}</span><div><small>{{ chapter.year }} / NEXT STOP</small>'+story_content+'</div><figure>'+story_photo+'</figure></article></div>',
 '<div class="romance-chapters"><article v-for="(chapter,i) in wedding.loveStory" :key="i" data-reveal><header><span>CHAPTER</span><b>{{ ["I","II","III","IV"][i] || i+1 }}</b><time>{{ chapter.year }}</time></header><figure>'+story_photo+'</figure><div>'+story_content+'</div></article></div>',
]
event_details='<h3>{{ event.title }}</h3><p>{{ date(event.date) }}</p><p>{{ event.time }} {{ zone(event.timezone) }}</p><strong>{{ event.venue }}</strong><p>{{ event.address }}</p><a v-if="event.maps" class="button button-outline" :href="event.maps" target="_blank" rel="noopener noreferrer">Lihat Lokasi ↗</a>'
events=[
 '<ol class="moon-calendar"><li v-for="(event,i) in wedding.events" :key="i" data-reveal><span class="moon-phase" aria-hidden="true">{{ i%2 ? "◐" : "☾" }}</span><div class="lunar-date"><b>{{ event.date?.slice(-2) }}</b><small>{{ wedding.date.month }}</small></div><div>'+event_details+'</div></li></ol>',
 '<div class="celebration-columns"><article v-for="(event,i) in wedding.events" :key="i" data-reveal><header><small>THE AGENDA</small><b>{{ String(i+1).padStart(2,"0") }}</b></header><div>'+event_details+'</div></article></div>',
 '<div class="coastal-itinerary"><article v-for="(event,i) in wedding.events" :key="i" data-reveal><time>{{ event.time.split(" – ")[0] }}</time><span aria-hidden="true">≈</span><div>'+event_details+'</div></article></div>',
 '<div class="royal-summons"><article v-for="(event,i) in wedding.events" :key="i" data-reveal><span class="crest-mini" aria-hidden="true">♧</span><small>THE HONOUR OF YOUR PRESENCE</small><div>'+event_details+'</div><span aria-hidden="true">✧</span></article></div>',
 '<div class="handwritten-agenda"><article v-for="(event,i) in wedding.events" :key="i" data-reveal><span class="paper-tape" aria-hidden="true"></span><header><small>PLEASE SAVE THIS NOTE</small><b>{{ wedding.date.day }}.{{ wedding.date.monthNumber }}</b></header><div>'+event_details+'</div></article></div>',
 '<div class="resort-schedule"><article v-for="(event,i) in wedding.events" :key="i" data-reveal><aside><b>{{ i+1 }}</b><time>{{ event.time.split(" – ")[0] }}</time></aside><div>'+event_details+'</div></article></div>',
 '<dl class="type-only-events"><div v-for="(event,i) in wedding.events" :key="i" data-reveal><dt>{{ String(i+1).padStart(2,"0") }} / {{ event.title }}</dt><dd><time>{{ event.time }}</time><div>'+event_details+'</div></dd></div></dl>',
 '<div class="vertical-invitations"><article v-for="(event,i) in wedding.events" :key="i" data-reveal><span class="vertical-date">{{ wedding.date.display }}</span><div>'+event_details+'</div><span class="red-seal">{{ i+1 }}</span></article></div>',
 '<div class="digital-passes"><article v-for="(event,i) in wedding.events" :key="i" data-reveal><header><span>WEDDING PASS</span><b>0{{ i+1 }}</b></header><div>'+event_details+'</div><footer><span class="pass-bars" aria-hidden="true"></span><small>{{ wedding.bride.shortName }} + {{ wedding.groom.shortName }}</small></footer></article></div>',
 '<div class="formal-programme"><article v-for="(event,i) in wedding.events" :key="i" data-reveal><small>THE CELEBRATION / {{ i+1 }}</small><span class="classic-rule" aria-hidden="true">❦</span><div>'+event_details+'</div></article></div>',
]
event_script='const date = value => new Date(`${value}T12:00:00+07:00`).toLocaleDateString("id-ID", {weekday:"long",day:"numeric",month:"long",year:"numeric"})\nconst zone = value => ({"Asia/Jakarta":"WIB","Asia/Makassar":"WITA","Asia/Jayapura":"WIT"})[value] || value'
presets_path=root/'backend/config/template-presets.json'
presets=json.loads(presets_path.read_text(encoding='utf-8'))
orders=[['home','couple','quote','story','date','event','gallery','location','gift','rsvp','wishes','closing'],['home','story','couple','event','gallery','quote','date','gift','location','rsvp','wishes','closing'],['home','event','couple','story','gallery','date','quote','location','gift','rsvp','wishes','closing'],['home','quote','couple','date','event','story','gallery','gift','location','rsvp','wishes','closing'],['home','couple','story','gallery','quote','event','date','gift','location','rsvp','wishes','closing'],['home','couple','event','location','story','gallery','quote','date','gift','rsvp','wishes','closing'],['home','story','gallery','couple','event','quote','date','gift','location','rsvp','wishes','closing'],['home','quote','couple','story','event','date','gallery','gift','location','rsvp','wishes','closing'],['home','story','couple','gallery','event','date','quote','gift','location','rsvp','wishes','closing'],['home','couple','quote','event','date','story','gallery','gift','location','rsvp','wishes','closing']]
for i,(key,folder,name,category,bride,groom,bg,ink,accent,label,opening,venue,mood) in enumerate(items):
 p=base/folder
 write(p/'Opening.vue',sfc('<section class="design-cover new-cover cover-'+key+'">'+covers[i]+guest.replace('LABEL',label)+'</section>','defineProps({guest:String})\ndefineEmits(["open"])'))
 write(p/'Hero.vue',sfc('<section id="home" class="new-hero hero-'+key+'">'+hero_parts[i]+'<p class="new-hero-copy">{{ wedding.sections.home?.content || wedding.openingText }}</p><button class="hero-scroll" aria-label="Gulir ke cerita kami" @click="scrollToSection(\'couple\')">↓</button></section>','import { scrollToSection } from "../../composables/useSectionNavigation"'))
 for filename,section,title,markup in [('Couple','couple','The people in our story',couples[i]),('Story','story','Our story',stories[i]),('Event','event','The celebration',events[i])]:
  write(p/(filename+'.vue'),sfc('<section id="'+section+'" class="section new-'+section+'"><SectionHeading title="'+title+'" />'+markup+'</section>',event_script if section=='event' else ''))
 write(p/'index.vue','''<script setup>
import WeddingExperience from '../shared/WeddingExperience.vue'
import '../shared/experience-base.css'
import '../shared/theme-base.css'
import '../shared/new-experiences.css'
import './presentation.css'
import Opening from './Opening.vue'
import Hero from './Hero.vue'
import Couple from './Couple.vue'
import Story from './Story.vue'
import Event from './Event.vue'
defineProps({wedding:Object,preview:Boolean})
const presentationComponents = {couple:Couple,story:Story,event:Event}
</script>
<template><WeddingExperience :wedding="wedding" :preview="preview" theme="'''+key+'" design="'+key+'" :cover-component="Opening" :hero-component="Hero" :presentation-components="presentationComponents" /></template>\n')
 headings={'home':name,'couple':'Two lives, one promise','quote':'Words we carry','story':['Written in the stars','The chapters','Tides of us','Our chronicle','Notes from our journal','Our island journey','The archive','A story in bloom','Our next stop','Chapters of a romance'][i],'event':['Under the same moon','The celebration issue','Your destination itinerary','A royal invitation','A note for your calendar','The resort programme','The programme','An invitation in bloom','Your wedding pass','The formal programme'][i],'gallery':['Our constellation','The photo spread','By the shore','The portrait gallery','Collected memories','The travel journal','An exhibition of us','The art of together','City frames','A gallery of romance'][i],'gift':['Moonlight wishes','A token of love','Gifts from the shore','A gracious gesture','A little gift tag','Island wishes','Gifts, simply','A heartfelt offering','Send some love','With our gratitude'][i],'rsvp':'Join our day','wishes':'Your words, our keepsake','closing':'With love, '+bride+' & '+groom}
 presets[key]={'name':name,'opening_text':opening,'order':orders[i],'mood':mood,'sections':{k:{'enabled':True,'heading':v,'subheading':'','content':''} for k,v in headings.items()},'quote':opening,'quote_source':'Our promise','closing_text':'We are grateful for every moment shared with you. With love, '+bride+' & '+groom+'.','category':category,'gallery_style':['Star-map grid','Editorial spread','Coastal reel','Palace wall','Scattered polaroids','Travel journal','Exhibition wall','Art gallery','Urban snap reel','Museum gallery'][i]}
 write(p/'presentation.css','.design-'+key+'{--ivory:'+bg+';--cream:'+bg+';--ink:'+ink+';--gold:'+accent+';--rose:'+accent+';--muted:'+ink+';--theme-bg:'+bg+';--theme-ink:'+ink+';}\n')
registry=base/'templateRegistry.js'
t=registry.read_text(encoding='utf-8')
for key,folder,name,*_ in items:
 if "'"+key+"': defineAsyncComponent" not in t:
  t=t.replace('export const templateRegistry = {','export const templateRegistry = {\n  \''+key+'\': defineAsyncComponent(() => import(\'./'+folder+'/index.vue\')),')
  t=t.replace('export const templateOptions = [','export const templateOptions = [\n  { value: \''+key+'\', label: '+json.dumps(name)+', component: \''+folder+'.vue\' },')
write(registry,t)
write(presets_path,json.dumps(presets,ensure_ascii=False,indent=2)+'\n')
catalog=root/'backend/app/Services/TemplateCatalog.php'
t=catalog.read_text(encoding='utf-8')
t=t.replace("'blush'];","'blush', "+', '.join("'"+x[0]+"'" for x in items)+'];')
t=t.replace("'Blush.vue'];","'Blush.vue', "+', '.join("'"+x[1]+".vue'" for x in items)+'];')
write(catalog,t)
write(root/'backend/config/additional-template-demos.json',json.dumps([{'key':x[0],'folder':x[1],'name':x[2],'category':x[3],'bride':x[4],'groom':x[5],'quote':x[10],'venue':x[11]} for x in items],ensure_ascii=False,indent=2))
