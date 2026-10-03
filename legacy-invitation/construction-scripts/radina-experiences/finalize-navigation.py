from pathlib import Path
p=Path(__file__).resolve().parents[1]/'frontend/src/templates/RomanticFloral/components/FloatingNavigation.vue'
s=p.read_text(encoding='utf-8').replace('ref, inject, onMounted','ref, computed, inject, onMounted')
s=s.replace('const items = [','const items = computed(() => [',1)
s=s.replace("].filter((item) =>\n", "].filter((item) => wedding.sections[item.id]?.enabled !== false && (\n",1)
s=s.replace('        : true,\n)', '        : true\n)))',1)
s=s.replace('items.forEach(', 'items.value.forEach(').replace('items.length','items.value.length')
s=s.replace('v-if="wedding.settings.enable_story && wedding.loveStory.length"','v-if="wedding.settings.enable_story && wedding.loveStory.length && wedding.sections.story?.enabled !== false"')
s=s.replace('v-if="wedding.settings.enable_rsvp"','v-if="wedding.settings.enable_rsvp && wedding.sections.rsvp?.enabled !== false"').replace('v-if="wedding.settings.enable_wishes"','v-if="wedding.settings.enable_wishes && wedding.sections.wishes?.enabled !== false"')
p.write_text(s,encoding='utf-8')
