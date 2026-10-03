<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { ref } from 'vue'
import { ChevronLeft, ChevronRight, Expand } from 'lucide-vue-next'
import { wedding } from '../data/wedding'
import SectionHeading from './SectionHeading.vue'
import BaseModal from './BaseModal.vue'
const active = ref(-1)
let touchStart = 0
function move(direction) { active.value = (active.value + direction + wedding.gallery.length) % wedding.gallery.length }
function onKey(event) { if (event.key === 'ArrowRight') { event.preventDefault(); move(1) } if (event.key === 'ArrowLeft') { event.preventDefault(); move(-1) } }
function onTouchEnd(event) { const delta = event.changedTouches[0].clientX - touchStart; if (Math.abs(delta) > 45) move(delta < 0 ? 1 : -1) }
</script>
<template>
  <section id="gallery" class="section gallery-section"><FlowerMotion />
    <SectionHeading eyebrow="OUR MOMENTS" title="A glimpse of our love" subtitle="Hal-hal sederhana, kenangan yang selamanya." />
    <div class="gallery-grid">
      <button v-for="(photo, i) in wedding.gallery" :key="photo.src" :class="`gallery-item gallery-item-${i}`" :aria-label="`Perbesar foto: ${photo.alt}`" @click="active = i" data-reveal>
        <img :src="photo.src" :srcset="`${photo.src.replace('.webp', '-small.webp')} 320w, ${photo.src} 650w`" sizes="(min-width: 600px) 170px, (min-width: 480px) 28vw, 45vw" :alt="photo.alt" width="600" height="800" loading="lazy" decoding="async" /><span><Expand :size="19" /></span>
      </button>
    </div>
    <p class="gallery-hint">Sentuh sebuah foto untuk melihat lebih dekat.</p>
    <BaseModal :open="active >= 0" title="Galeri momen pernikahan" wide @keydown="onKey" @close="active = -1">
      <div v-if="active >= 0" class="lightbox" @touchstart="touchStart = $event.touches[0].clientX" @touchend="onTouchEnd">
        <img :src="wedding.gallery[active].src" :alt="wedding.gallery[active].alt" />
        <div class="lightbox-controls">
          <button class="icon-button" aria-label="Foto sebelumnya" @click="move(-1)"><ChevronLeft /></button><span>{{ active + 1 }} / {{ wedding.gallery.length }}</span><button class="icon-button" aria-label="Foto berikutnya" @click="move(1)"><ChevronRight /></button>
        </div>
        <p>{{ wedding.gallery[active].alt }}</p>
      </div>
    </BaseModal>
  </section>
</template>
