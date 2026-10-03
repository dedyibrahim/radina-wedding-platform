import {readFileSync,writeFileSync} from 'node:fs'
const folders=['RomanticFloral','ElegantLuxury','MinimalistWhite','NusantaraHeritage','GardenDream','ClassicVintage','MidnightRomance','Sakinah','EternalStory','Blush']
for(const folder of folders){
 for(const name of ['Opening','Hero']){
  const path=`frontend/src/templates/${folder}/${name}.vue`
  let s=readFileSync(path,'utf8')
  s=s.replace(':class="`cover-${design}`"', ':class="`cover-${design}`" :style="nameStyle"').replace(':class="`hero-${design}`"', ':class="`hero-${design}`" :style="nameStyle"')
  s=s.replace("import { inject } from 'vue'","import { inject, computed } from 'vue'")
  s=s.replace('</script>',"const nameStyle = computed(() => ({ '--name-scale': `${Math.min(20,115 / Math.max(wedding.bride.shortName.length,wedding.groom.shortName.length,1))}vw` }))\n</script>")
  s=s.replace('{{ wedding.openingText }}','{{ wedding.sections.home?.content || wedding.openingText }}')
  if(name==='Hero')s=s.replace('<div class="hero-copy">','<div class="hero-copy"><p v-if="wedding.sections.home?.subheading" class="hero-kicker">{{ wedding.sections.home.subheading }}</p>')
  writeFileSync(path,s)
 }
}
