<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { CalendarPlus } from 'lucide-vue-next'
import { wedding } from '../data/wedding'
import { downloadCalendar } from '../utils/calendar'
import Countdown from './Countdown.vue'
import BotanicalOrnament from './BotanicalOrnament.vue'
</script>
<template><section id="date" class="section date-section"><FlowerMotion /><BotanicalOrnament class="date-floral" /><div data-reveal><p class="eyebrow">SAVE THE DATE</p><h2>A day to remember</h2><div class="big-date"><span>{{ wedding.date.day }}</span><div>{{ wedding.date.month }}<br /><small>{{ wedding.date.year }}</small></div></div><p class="date-intro">Menghitung hari menuju awal selamanya.</p><Countdown :date="wedding.date.iso" /><button class="button button-outline" @click="downloadCalendar"><CalendarPlus :size="16" /> Simpan Tanggal</button></div></section></template>
