from pathlib import Path
root=Path(__file__).resolve().parents[1]/'frontend/src'
def read(path):return(root/path).read_text(encoding='utf-8')
def write(path,value):(root/path).write_text(value,encoding='utf-8')
base='templates/RomanticFloral/components/'
path=base+'RSVPSection.vue';s=read(path);start=s.index("const context = inject('weddingContext')");end=s.index('</script>');body=s[start:end].replace('props.guest','guest')
write('composables/useRSVP.js',"import { ref, inject } from 'vue'\nimport { api, errorMessage } from '../services/api'\nexport function useRSVP(guest) {\n"+body+"return { name, guests, attendance, message, error, success, pending, submit }\n}\n")
s=s[:start]+"const { name, guests, attendance, message, error, success, pending, submit } = useRSVP(props.guest)\n"+s[end:]
s=s.replace("import { ref, inject } from 'vue'", "import { useRSVP } from '../../../composables/useRSVP'").replace("import { api, errorMessage } from '../../../services/api'\n",'');write(path,s)
path=base+'WishesSection.vue';s=read(path);start=s.index('const props = defineProps');end=s.index('</script>');body=s[start:end];body=body[body.index('const name ='):]
body=body.replace('props.guest','guest')
write('composables/useWishes.js',"import { ref, inject, onMounted } from 'vue'\nimport { api, errorMessage } from '../services/api'\nexport function useWishes(guest) {\nconst context = inject('weddingContext')\n"+body+"return { name, message, error, pending, wishes, next, load, submit, relative }\n}\n")
s=s[:start]+"const props = defineProps({ guest: String })\nconst { name, message, error, pending, wishes, next, load, submit, relative } = useWishes(props.guest)\n"+s[end:];s=s.replace("import { ref, inject, onMounted } from 'vue'", "import { useWishes } from '../../../composables/useWishes'").replace("import { api, errorMessage } from '../../../services/api'\n",'').replace('<section class="section wishes-section">','<section id="wishes" class="section wishes-section">');write(path,s)
path=base+'WeddingGift.vue';s=read(path);start=s.index("const wedding = inject('wedding')");end=s.index('</script>');body=s[start:end];body=body[body.index('const active ='):].replace("emit('toast', ", 'notify(')
write('composables/useGift.js',"import { ref, computed, inject, watch } from 'vue'\nexport function useGift(notify) {\nconst wedding = inject('wedding')\n"+body+"return { wedding, active, address, downloading, tabs, methods, copy, download }\n}\n")
s=s[:start]+"const emit = defineEmits(['toast'])\nconst { wedding, active, address, downloading, tabs, methods, copy, download } = useGift(message => emit('toast', message))\n"+s[end:];s=s.replace("import { ref, computed, inject, watch } from 'vue'", "import { useGift } from '../../../composables/useGift'");write(path,s)
path=base+'GallerySection.vue';s=read(path);start=s.index('const active =');end=s.index('</script>');body=s[start:end].replace('let touchStart = 0','const touchStart = ref(0)').replace('clientX - touchStart','clientX - touchStart.value')
write('composables/useGallery.js',"import { ref, inject } from 'vue'\nexport function useGallery() {\nconst wedding = inject('wedding')\n"+body+"function onTouchStart(event) { touchStart.value = event.touches[0].clientX }\nreturn { wedding, active, move, onKey, onTouchEnd, onTouchStart }\n}\n")
s=s[:start]+"const { wedding, active, move, onKey, onTouchEnd, onTouchStart } = useGallery()\n"+s[end:];s=s.replace("import { ref } from 'vue'", "import { useGallery } from '../../../composables/useGallery'").replace("import { inject } from 'vue'\nconst wedding = inject('wedding')\n",'').replace('@touchstart="touchStart = $event.touches[0].clientX"','@touchstart="onTouchStart"');write(path,s)
