<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { wedding } from '../data/wedding'
import SectionHeading from './SectionHeading.vue'
</script>
<template><section class="section story-section"><FlowerMotion /><SectionHeading eyebrow="OUR LOVE STORY" title="Every love has a story" subtitle="Ini adalah beberapa halaman dari cerita kami." /><div class="story-photo" data-reveal><img :src="wedding.gallery[3].src" :alt="wedding.gallery[3].alt" loading="lazy" width="800" height="500" /><span>It was always you.</span></div><div class="timeline"><article v-for="story in wedding.loveStory" :key="story.year" data-reveal><span class="timeline-dot"></span><p class="eyebrow">{{ story.year }}</p><h3>{{ story.title }}</h3><p>{{ story.text }}</p></article></div></section></template>
