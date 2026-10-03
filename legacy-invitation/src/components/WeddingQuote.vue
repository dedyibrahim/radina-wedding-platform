<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { wedding } from '../data/wedding'
import BotanicalOrnament from './BotanicalOrnament.vue'
</script>
<template><section id="quote" class="section quote-section"><FlowerMotion /><BotanicalOrnament class="quote-botanical" /><div data-reveal><p class="arabic" lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</p><p class="eyebrow">IN THE NAME OF ALLAH, THE MOST MERCIFUL</p><blockquote>“{{ wedding.quote }}”</blockquote><p class="quote-source">{{ wedding.quoteSource }}</p></div></section></template>
