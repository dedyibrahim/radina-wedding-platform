<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { Instagram } from 'lucide-vue-next'
import { wedding } from '../data/wedding'
import SectionHeading from './SectionHeading.vue'
import BotanicalOrnament from './BotanicalOrnament.vue'
</script>
<template>
  <section id="couple" class="section couple-section"><FlowerMotion /><SectionHeading eyebrow="THE BRIDE & GROOM" title="Two souls, one love" subtitle="Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan pernikahan kami." />
    <div class="couple-grid"><article v-for="(person, i) in [wedding.bride, wedding.groom]" :key="person.name" class="person" data-reveal>
      <div class="portrait-wrap"><img :src="person.photo" :alt="person.name" width="400" height="520" loading="lazy" /><BotanicalOrnament /></div>
      <p class="eyebrow person-label">{{ i === 0 ? 'THE BRIDE' : 'THE GROOM' }}</p><h3>{{ person.name }}</h3><p>{{ person.order }}<br /><strong>{{ person.father }}</strong><br />& <strong>{{ person.mother }}</strong></p>
      <a :href="`https://www.instagram.com/${person.instagram}/`" target="_blank" rel="noopener noreferrer" class="social-link"><Instagram :size="14" /> @{{ person.instagram }}</a>
    </article></div><div class="couple-and" aria-hidden="true">&</div>
  </section>
</template>
