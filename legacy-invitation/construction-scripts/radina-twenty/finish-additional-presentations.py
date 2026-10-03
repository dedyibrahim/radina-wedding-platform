from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];base=root/'frontend/src/templates'
items=json.loads((root/'backend/config/additional-template-demos.json').read_text(encoding='utf-8'))
wrappers=['star-map-gallery','magazine-photo-spread','coastal-photo-reel','palace-photo-wall','scattered-photo-notes','resort-travel-journal','documentary-exhibition','blossom-art-gallery','urban-snap-reel','museum-photo-gallery']
gallery_item='<button :aria-label="`Perbesar foto: ${photo.alt}`" @click="open(i)"><img :src="photo.src" :alt="photo.alt" loading="lazy" decoding="async"><span aria-hidden="true">↗</span></button>'
for i,entry in enumerate(items):
 p=base/entry['folder'];key=entry['key']
 markup='<figure v-for="(photo,i) in photos" :key="i">'+gallery_item+'<figcaption>{{ photo.alt }}</figcaption></figure>'
 if i==0:markup='<div v-for="(photo,i) in photos" :key="i" class="star-photo"><span aria-hidden="true">✧</span>'+gallery_item+'</div>'
 if i==1:markup='<article v-for="(photo,i) in photos" :key="i"><small>FRAME {{ String(i+1).padStart(2,"0") }}</small>'+gallery_item+'<p>{{ photo.alt }}</p></article>'
 if i==4:markup='<figure v-for="(photo,i) in photos" :key="i"><span class="paper-tape" aria-hidden="true"></span>'+gallery_item+'<figcaption>{{ photo.alt }}</figcaption></figure>'
 if i==5:markup='<article v-for="(photo,i) in photos" :key="i">'+gallery_item+'<div><b>STOP {{ i+1 }}</b><p>{{ photo.alt }}</p></div></article>'
 if i==6:markup='<figure v-for="(photo,i) in photos" :key="i">'+gallery_item+'<figcaption><b>{{ String(i+1).padStart(2,"0") }}</b><p>{{ photo.alt }}</p></figcaption></figure>'
 if i==8:markup='<article v-for="(photo,i) in photos" :key="i"><header>FRAME / 0{{ i+1 }}</header>'+gallery_item+'</article>'
 s='<script setup>\nimport GalleryController from "../shared/GalleryController.vue"\nimport SectionHeading from "../RomanticFloral/components/SectionHeading.vue"\n</script>\n<template><section id="gallery" class="section new-gallery"><SectionHeading title="Collected moments"/><GalleryController v-slot="{photos,open}"><div class="collection-gallery '+wrappers[i]+'">'+markup+'</div></GalleryController></section></template>\n'
 (p/'Gallery.vue').write_text(s,encoding='utf-8')
 text=p.joinpath('index.vue').read_text(encoding='utf-8').replace("import Event from './Event.vue'","import Event from './Event.vue'\nimport Gallery from './Gallery.vue'\nimport Closing from './Closing.vue'").replace('event:Event}','event:Event,gallery:Gallery,closing:Closing}')
 p.joinpath('index.vue').write_text(text,encoding='utf-8')
 name='<h2>{{ wedding.bride.shortName }} <i>&</i> {{ wedding.groom.shortName }}</h2>'
 content='<p>{{ wedding.sections.closing?.content || wedding.closingText }}</p>'
 img='<img v-if="wedding.closing" :src="wedding.closing" alt="Pasangan pengantin" loading="lazy">'
 monogram='<div class="new-closing-monogram">{{ wedding.bride.shortName[0] }} & {{ wedding.groom.shortName[0] }}</div>'
 parts=[
 '<div class="sky-speckles" aria-hidden="true"></div><span class="crescent" aria-hidden="true">☾</span><div class="sky-farewell">'+name+content+'</div><figure>'+img+'</figure>',
 '<header><small>BACK COVER</small><b>THE END.<br>THE BEGINNING.</b></header>'+img+'<div>'+content+name+'</div>',
 '<figure>'+img+'<div class="wave-line" aria-hidden="true"></div></figure><div>'+name+content+'</div>',
 monogram+'<div class="royal-farewell">'+content+name+'</div>',
 '<div class="paper-thankyou"><span class="paper-tape" aria-hidden="true"></span><small>A THANK YOU NOTE</small>'+content+name+'</div>',
 '<figure>'+img+'</figure><div class="resort-farewell"><small>UNTIL WE MEET AT THE DESTINATION</small>'+name+content+'</div>',
 '<div class="documentary-end"><small>THE FINAL FRAME</small>'+name+content+'<span>TO BE CONTINUED, TOGETHER.</span></div>',
 '<span class="falling-blossom" aria-hidden="true">✿</span><div>'+content+name+'</div><figure>'+img+'</figure>',
 '<figure>'+img+'</figure><div class="city-farewell"><small>THE NIGHT IS OURS</small>'+name+content+'</div>',
 '<div class="formal-thankyou"><span class="classic-rule" aria-hidden="true">❦</span>'+content+name+'<p>{{ wedding.date.display }}</p></div>',
 ]
 closing='<script setup>\nimport {inject} from "vue"\nconst wedding=inject("wedding")\n</script>\n<template><section id="closing" class="new-closing closing-'+key+'"><p v-if="wedding.sections.closing?.heading" class="closing-heading">{{ wedding.sections.closing.heading }}</p><p v-if="wedding.sections.closing?.subheading">{{ wedding.sections.closing.subheading }}</p>'+parts[i]+'<small>{{ wedding.socialMedia.hashtag }}</small><footer>RADINA · DIGITAL WEDDING INVITATION</footer></section></template>\n'
 p.joinpath('Closing.vue').write_text(closing,encoding='utf-8')
