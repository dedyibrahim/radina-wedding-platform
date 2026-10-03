import { readFileSync, writeFileSync } from 'node:fs'
import postcss from 'postcss'
const designs = [['RomanticFloral','amore'],['ElegantLuxury','noir'],['MinimalistWhite','pure'],['NusantaraHeritage','nusantara'],['GardenDream','garden'],['ClassicVintage','letters'],['MidnightRomance','dark'],['Sakinah','sakinah'],['EternalStory','cinema'],['Blush','daydream']]
const cover = readFileSync('frontend/src/templates/shared/DesignCover.vue','utf8')
const hero = readFileSync('frontend/src/templates/shared/DesignHero.vue','utf8')
function branch(source, design) {
  const branches = [...source.matchAll(/<template (v-if|v-else-if|v-else)(?:="([^"]+)")?>([\s\S]*?)<\/template>/g)]
  const selected = branches.find(([,kind,condition]) => kind === 'v-else' || new Function('design', `return ${condition}`)(design))
  const begin = source.indexOf('<template>')
  const outer = source.slice(begin + '<template>'.length)
  const first = outer.indexOf('<template ')
  const last = outer.lastIndexOf('</template>')
  const branchEnd = outer.lastIndexOf('</template>', last - 1) + '</template>'.length
  return '<template>' + outer.slice(0, first) + selected[3] + outer.slice(branchEnd)
}
for (const [folder,design] of designs) {
  for (const [name,source] of [['Opening',cover],['Hero',hero]]) {
    let script=source.slice(0,source.indexOf('<template>')).replace("defineProps({ design: String, guest: String })", "defineProps({ guest: String })").replace("defineProps({ design: String })",'')
    script=script.replace("from '../../composables/", "from '../../composables/").replace('</script>',`const design = '${design}'\n</script>`)
    writeFileSync(`frontend/src/templates/${folder}/${name}.vue`,script+branch(source,design))
  }
  const path=`frontend/src/templates/${folder}/index.vue`
  let source=readFileSync(path,'utf8').replace("import '../../assets/styles/experiences.css'", "import '../shared/experience-base.css'\nimport './presentation.css'\nimport Opening from './Opening.vue'\nimport Hero from './Hero.vue'")
  source=source.replace(':wedding="wedding"', ':cover-component="Opening" :hero-component="Hero" :wedding="wedding"')
  writeFileSync(path,source)
}
const css = postcss.parse(readFileSync('frontend/src/assets/styles/experiences.css','utf8'))
function matches(selector, design) { return new RegExp(`\\.(?:design|cover|hero|couple|story|closing)-${design}(?![\\w-])`).test(selector) }
function filter(node, design) {
  const copy=node.clone()
  if (node.type==='rule') {
    const selectors=node.selectors.filter(selector => design ? matches(selector,design) : !designs.some(([,d])=>matches(selector,d)))
    if(!selectors.length)return null
    copy.selectors=selectors
  } else if (node.type==='atrule' && node.nodes && !node.name.includes('keyframes')) {
    copy.removeAll();node.nodes.forEach(child=>{const kept=filter(child,design);if(kept)copy.append(kept)})
    if(!copy.nodes.length)return null
  } else if(design)return null
  return copy
}
for(const [folder,design] of [['shared',null],...designs]) {
 const result=postcss.root();css.nodes.forEach(node=>{const kept=filter(node,design);if(kept)result.append(kept)})
 writeFileSync(`frontend/src/templates/${folder}/${design ? 'presentation.css' : 'experience-base.css'}`,result.toString())
}
