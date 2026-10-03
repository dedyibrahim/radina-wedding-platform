from pathlib import Path
root = Path(__file__).resolve().parents[1]
def read(path): return (root / path).read_text(encoding='utf-8')
def write(path, value): (root / path).write_text(value, encoding='utf-8')
designs = [('RomanticFloral','amore','floral','Amore Bloom'), ('ElegantLuxury','noir','luxury','Noir Élégance'), ('MinimalistWhite','pure','minimal','Pure'), ('NusantaraHeritage','nusantara','heritage','Nusantara'), ('GardenDream','garden','garden','Verdant Vows'), ('ClassicVintage','letters','vintage','Heritage Letters'), ('MidnightRomance','dark','midnight','After Dark'), ('Sakinah','sakinah','sakinah','Sakinah'), ('EternalStory','cinema','cinematic','Frame by Frame'), ('Blush','daydream','blush','Daydream')]
for folder, design, theme, label in designs:
    write(f'frontend/src/templates/{folder}/index.vue', f'''<script setup>
import WeddingExperience from '../shared/WeddingExperience.vue'
import '../../assets/styles/experiences.css'
defineProps({{ wedding: Object, preview: Boolean }})
</script>
<template><WeddingExperience :wedding="wedding" :preview="preview" theme="{theme}" design="{design}" /></template>
''')
path='frontend/src/templates/templateRegistry.js'
s=read(path)
old=['Romantic Floral','Elegant Luxury','Minimalist White','Nusantara Heritage','Garden Dream','Classic Vintage','Midnight Romance','Sakinah','Eternal Story','Blush']
for before, (_, _, _, after) in zip(old, designs): s=s.replace("label: '"+before+"'", "label: '"+after+"'")
write(path,s)
path='frontend/src/templates/shared/WeddingExperience.vue'; s=read(path)
s=s.replace("import WeddingCover from '../RomanticFloral/components/WeddingCover.vue'", "import WeddingCover from './DesignCover.vue'")
s=s.replace("import InvitationContent from '../RomanticFloral/components/InvitationContent.vue'", "import InvitationContent from './DesignContent.vue'")
s=s.replace("theme: { type: String, default: 'floral' },", "theme: { type: String, default: 'floral' },\n  design: { type: String, default: 'amore' },")
s=s.replace(':class="`theme-${theme}`"', ':class="[`theme-${theme}`, `design-${design}`]"')
s=s.replace(':guest="guest" @open="openInvitation"', ':guest="guest" :design="design" @open="openInvitation"')
s=s.replace('v-else\n          :guest="guest"', 'v-else\n          :design="design" :guest="guest"')
write(path,s)
path='frontend/src/utils/weddingView.js'; s=read(path)
s="import { presetFor } from '../templates/contentPresets'\n"+s
s=s.replace("const events =", "const preset = presetFor(data.template?.template_key)\n  const sections = Object.fromEntries(Object.entries(preset.sections).map(([key, value]) => [key, { ...value, ...(data.section_content?.[key] || {}) }]))\n  const events =",1)
s=s.replace('id: data.id,','id: data.id,\n    sections,\n    sectionOrder: data.section_order?.length ? data.section_order : preset.order,',1)
s=s.replace('openingText: data.opening_text,','openingText: data.opening_text ?? preset.opening_text,')
s=s.replace('music: data.music?.music_url,', 'music: data.music?.playlist?.[0]?.url || data.music?.music_url,')
write(path,s)
path='frontend/src/templates/RomanticFloral/components/SectionHeading.vue'; s=read(path)
s=s.replace("defineProps({ eyebrow: String, title: String, subtitle: String })", "import { inject } from 'vue'\nconst content = inject('sectionContent', null)\ndefineProps({ section: String, eyebrow: String, title: String, subtitle: String })")
s=s.replace('{{ title }}','{{ content?.heading || title }}').replace('v-if="subtitle"','v-if="content?.subheading || subtitle"').replace('{{ subtitle }}','{{ content?.subheading || subtitle }}')
s=s.replace('</header>', '<p v-if="content?.content" class="section-subtitle">{{ content.content }}</p>\n  </header>')
write(path,s)
