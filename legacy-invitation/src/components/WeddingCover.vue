<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { MailOpen, ArrowUpRight } from 'lucide-vue-next'
import { wedding } from '../data/wedding'
import BotanicalOrnament from './BotanicalOrnament.vue'
defineProps({ guest: String })
defineEmits(['open'])
</script>
<template>
  <section class="wedding-cover" aria-label="Sampul undangan"><FlowerMotion />
    <img class="cover-photo" :src="wedding.cover" :srcset="`${wedding.cover.replace('.webp', '-small.webp')} 600w, ${wedding.cover} 1000w`" sizes="(min-width: 600px) 600px, 100vw" alt="Pasangan pengantin dalam suasana romantis" fetchpriority="high" width="1000" height="1500" />
    <div class="cover-shade"></div><div class="cover-frame"></div>
    <BotanicalOrnament class="cover-floral floral-left" /><BotanicalOrnament class="cover-floral floral-right" />
    <div class="petals" aria-hidden="true"><span v-for="i in 5" :key="i" :style="{ '--i': i }"></span></div>
    <div class="cover-top"><span class="monogram">A<span>&</span>R</span><span class="eyebrow">A PROMISE OF FOREVER</span></div>
    <div class="cover-content">
      <p class="eyebrow cover-kicker">THE WEDDING OF</p>
      <h1 class="couple-names"><span>{{ wedding.bride.shortName }}</span><em>&</em><span>{{ wedding.groom.shortName }}</span></h1>
      <div class="cover-date"><span></span>{{ wedding.date.day }} . {{ wedding.date.monthNumber }} . {{ wedding.date.year }}<span></span></div>
      <p class="cover-note">Two hearts. One beautiful beginning.</p>
    </div>
    <div class="cover-invite">
      <p>Kepada Yth. Bapak/Ibu/Saudara/i</p><h2 class="guest-name">{{ guest }}</h2>
      <button class="button button-light" @click="$emit('open')"><MailOpen :size="17" /> Buka Undangan <ArrowUpRight :size="16" /></button>
      <p class="cover-footnote">Dengan cinta, kami mengundang Anda.</p>
    </div>
  </section>
</template>
