<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { ref, onMounted, onUnmounted } from 'vue'
import { ChevronDown } from 'lucide-vue-next'
import { wedding } from '../data/wedding'
import BotanicalOrnament from './BotanicalOrnament.vue'
const parallax = ref(0)
let frame
function updateParallax() {
  if (frame) return
  frame = requestAnimationFrame(() => { parallax.value = Math.min(window.scrollY * 0.025, 18); frame = null })
}
onMounted(() => { if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) window.addEventListener('scroll', updateParallax, { passive: true }) })
onUnmounted(() => { window.removeEventListener('scroll', updateParallax); if (frame) cancelAnimationFrame(frame) })
</script>
<template>
  <section id="home" class="hero-section"><FlowerMotion />
    <div class="hero-top"><span class="eyebrow">TOGETHER, WITH OUR FAMILIES</span><span class="small-monogram">A & R</span></div>
    <div class="hero-title" :style="{ transform: `translateY(${parallax}px)` }"><p class="eyebrow">THE WEDDING OF</p><h1>{{ wedding.bride.shortName }} <em>&</em> {{ wedding.groom.shortName }}</h1><p class="hero-date">{{ wedding.date.day }} {{ wedding.date.month }} {{ wedding.date.year }}</p></div>
    <div class="hero-image-wrap"><div class="arch-outline"></div><img :src="wedding.hero" :srcset="`${wedding.hero.replace('.webp', '-small.webp')} 400w, ${wedding.hero} 850w`" sizes="(min-width: 480px) 360px, 75vw" alt="Alya dan Rizky merayakan cinta mereka" width="800" height="1000" /><BotanicalOrnament class="hero-floral" /><span class="photo-caption">a love written in the stars</span></div>
    <p class="hero-bottom">And so, our forever begins.</p>
    <a class="scroll-indicator" href="#quote" aria-label="Gulir ke cerita kami"><ChevronDown :size="19" /></a>
  </section>
</template>
