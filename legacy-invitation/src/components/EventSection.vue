<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { CalendarDays, Clock3, MapPin, ArrowUpRight } from 'lucide-vue-next'
import { wedding } from '../data/wedding'
import SectionHeading from './SectionHeading.vue'
</script>
<template><section class="section event-section"><FlowerMotion /><SectionHeading eyebrow="WEDDING EVENT" title="Celebrate with us" subtitle="Kehadiran dan doa restu Anda akan menjadikan hari kami semakin berarti." /><article v-for="(event, i) in [wedding.akad, wedding.reception]" :key="event.title" class="event-card" data-reveal><div class="event-number">0{{ i + 1 }}</div><h3>{{ event.title }}</h3><div class="event-detail"><CalendarDays :size="16" /><span>{{ wedding.date.weekday }}, {{ wedding.date.display }}</span></div><div class="event-detail"><Clock3 :size="16" /><span>{{ event.time }} {{ wedding.date.timezone }}</span></div><div class="event-venue"><MapPin :size="18" /><strong>{{ wedding.location.name }}</strong><span>{{ wedding.location.city }}</span></div><a class="button button-outline" :href="wedding.location.maps" target="_blank" rel="noopener noreferrer">Lihat Lokasi <ArrowUpRight :size="15" /></a></article><p class="event-note">A little love, a little laughter, a happily ever after.</p></section></template>
