<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { ref } from 'vue'
import { Play } from 'lucide-vue-next'
import { wedding } from '../data/wedding'
import SectionHeading from './SectionHeading.vue'
const loaded = ref(false)
</script>
<template><section v-if="wedding.video.enabled" class="section video-section"><FlowerMotion /><SectionHeading eyebrow="OUR STORY" title="Love, in motion" /><div class="video-frame" data-reveal><video v-if="loaded" controls playsinline preload="metadata" :poster="wedding.video.poster" :src="wedding.video.src" aria-label="Video cerita cinta" /><button v-else class="video-poster" aria-label="Muat video cerita cinta" @click="loaded = true"><img :src="wedding.video.poster" alt="Pratinjau video cerita cinta" loading="lazy" /><span><Play :size="22" fill="currentColor" /></span><small>PLAY OUR FILM</small></button></div><p class="gallery-hint">A collection of moments, a lifetime of love.</p></section></template>
