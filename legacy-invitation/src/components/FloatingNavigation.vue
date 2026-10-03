<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { House, Heart, CalendarDays, Images, MailCheck } from 'lucide-vue-next'
const items = [ { id: 'home', label: 'Home', icon: House }, { id: 'couple', label: 'Couple', icon: Heart }, { id: 'date', label: 'Date', icon: CalendarDays }, { id: 'gallery', label: 'Gallery', icon: Images }, { id: 'rsvp', label: 'RSVP', icon: MailCheck } ]
const active = ref('home')
let observer, mutationObserver, frame
function updateActive() {
  let current = 'home'
  items.forEach(item => { const el = document.getElementById(item.id); if (el && el.getBoundingClientRect().top <= window.innerHeight * 0.4) current = item.id })
  active.value = current
}
function onScroll() {
  if (frame) return
  frame = requestAnimationFrame(() => { updateActive(); frame = null })
}
onMounted(() => {
  observer = new IntersectionObserver(updateActive, { rootMargin: '-10% 0px -55% 0px', threshold: 0 })
  window.addEventListener('scroll', onScroll, { passive: true })
  const observeSections = () => {
    let found = 0
    items.forEach(item => { const el = document.getElementById(item.id); if (el) { observer.observe(el); found++ } })
    if (found === items.length) mutationObserver?.disconnect()
  }
  mutationObserver = new MutationObserver(observeSections)
  mutationObserver.observe(document.getElementById('invitation'), { childList: true, subtree: true })
  observeSections()
})
onUnmounted(() => { observer?.disconnect(); mutationObserver?.disconnect(); window.removeEventListener('scroll', onScroll); if (frame) cancelAnimationFrame(frame) })
</script>
<template><nav class="floating-nav" aria-label="Navigasi undangan"><a v-for="item in items" :key="item.id" :href="`#${item.id}`" :class="{ active: active === item.id }" :aria-current="active === item.id ? 'location' : undefined" @click="active = item.id"><component :is="item.icon" :size="18" /><span>{{ item.label }}</span></a></nav></template>
