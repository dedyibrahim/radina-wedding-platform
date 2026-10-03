<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { ref } from 'vue'
import { MapPin, ArrowUpRight } from 'lucide-vue-next'
import { wedding } from '../data/wedding'
import SectionHeading from './SectionHeading.vue'
const mapLoaded = ref(false)
</script>
<template><section class="section location-section"><FlowerMotion /><SectionHeading eyebrow="LOCATION" title="Meet us here" /><div class="map-wrap" data-reveal><iframe v-if="mapLoaded" :src="wedding.location.embed" title="Peta lokasi Grand Ballroom Jakarta" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe><button v-else class="map-preview" @click="mapLoaded = true" aria-label="Muat peta interaktif"><div class="map-streets" aria-hidden="true"></div><span class="map-pin"><MapPin :size="26" /></span><strong>{{ wedding.location.name }}</strong><span class="map-load">Sentuh untuk memuat peta</span></button></div><div class="location-info" data-reveal><h3>{{ wedding.location.name }}</h3><p>{{ wedding.location.address }}</p><a class="button" :href="wedding.location.maps" target="_blank" rel="noopener noreferrer"><MapPin :size="16" /> Buka Google Maps <ArrowUpRight :size="15" /></a><p class="sample-note">Lokasi contoh — detail venue akan dikonfirmasi.</p></div></section></template>
