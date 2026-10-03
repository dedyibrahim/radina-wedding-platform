from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
demos=json.loads((root/'backend/config/additional-template-demos.json').read_text(encoding='utf-8'))
intro={'paper-petals':'WE SAVED YOU A PLACE','botanica':'THE DESTINATION EDITION','neon-love':'THIS CITY. THIS LOVE.','timeless-romance':'A CELEBRATION OF LOVE'}
headings=['Written in the stars','The wedding issue','At the edge of forever','The celebration of a lifetime','A little note for you','Our destination: together','A documentary of us','A promise in bloom','This city. This love.','A celebration of love']
presets_file=root/'backend/config/template-presets.json';presets=json.loads(presets_file.read_text(encoding='utf-8'))
for index,d in enumerate(demos):
 folder=root/'frontend/src/templates'/d['folder'];p=folder/'Hero.vue';s=p.read_text(encoding='utf-8')
 s=s.replace("import SectionHeading from '../RomanticFloral/components/SectionHeading.vue'", "import HeroCopy from '../shared/HeroCopy.vue'")
 s=s.replace('<p class="new-hero-copy">{{ wedding.sections.home?.content || wedding.openingText }}</p>', '<HeroCopy'+(' :show-heading="false"' if d['key'] in intro or d['key']=='blossom-east' else '')+' />')
 if d['key'] in intro:s=s.replace('<small>'+intro[d['key']]+'</small>', '<small>{{ wedding.sections.home?.heading }}</small>')
 if d['key']=='blossom-east':s=s.replace('<p>{{ wedding.openingText }}</p>', '<p v-if="wedding.sections.home?.heading">{{ wedding.sections.home.heading }}</p>')
 p.write_text(s,encoding='utf-8')
 p=folder/'Opening.vue';s=p.read_text(encoding='utf-8').replace("import SectionHeading from '../RomanticFloral/components/SectionHeading.vue'\n",'')
 if d['key'] in ['royal-heritage','neon-love','botanica']:s=s.replace('<p>{{ wedding.date.display }}</p>','<p>{{ wedding.date.display }}</p><p class="opening-message">{{ wedding.openingText }}</p>',1)
 if d['key'] in ['editorial','monochrome']:s=s.replace('<h1>{{ wedding.bride.shortName }} <i>&</i> {{ wedding.groom.shortName }}</h1>','<h1>{{ wedding.bride.shortName }} <i>&</i> {{ wedding.groom.shortName }}</h1><p class="opening-message">{{ wedding.openingText }}</p>',1)
 p.write_text(s,encoding='utf-8')
 presets[d['key']]['sections']['home']['heading']=headings[index]
presets_file.write_text(json.dumps(presets,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
