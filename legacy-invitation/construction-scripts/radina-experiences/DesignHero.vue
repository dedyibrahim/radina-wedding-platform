<script setup>
import { inject } from 'vue'
import { scrollToSection } from '../../composables/useSectionNavigation'
defineProps({ design: String })
const wedding = inject('wedding')
</script>
<template>
  <section id="home" class="design-hero" :class="`hero-${design}`">
    <template v-if="design === 'amore' || design === 'daydream'"
      ><div class="editorial-collage">
        <img class="collage-main" :src="wedding.hero || wedding.cover" alt="Momen pasangan" /><img
          v-if="wedding.gallery[0]"
          class="collage-small one"
          :src="wedding.gallery[0].src"
          alt="Kenangan pasangan"
          loading="lazy"
        /><img
          v-if="wedding.gallery[1]"
          class="collage-small two"
          :src="wedding.gallery[1].src"
          alt="Kenangan pasangan"
          loading="lazy"
        /><span class="collage-note">{{
          design === 'amore' ? 'a love in bloom' : 'our happy little world ♡'
        }}</span>
      </div>
      <div class="hero-copy">
        <small>TOGETHER, FOREVER</small>
        <h1>{{ wedding.bride.shortName }} <i>&</i> {{ wedding.groom.shortName }}</h1>
        <p>{{ wedding.openingText }}</p>
      </div></template
    >
    <template v-else-if="design === 'letters'"
      ><div class="invitation-letter">
        <span class="letter-stamp">SAVE THE DATE</span><small>DEAREST FAMILY & FRIENDS</small>
        <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
        <p>{{ wedding.openingText }}</p>
        <img :src="wedding.hero || wedding.cover" alt="Kenangan pasangan" loading="lazy" />
        <p>{{ wedding.date.display }}</p>
        <span class="handwritten">With love, always</span>
      </div></template
    >
    <template v-else-if="design === 'noir'"
      ><img class="hero-full-photo" :src="wedding.hero || wedding.cover" alt="Potret pasangan" />
      <div class="fashion-masthead">THE WEDDING EDITION</div>
      <div class="hero-copy">
        <small>AN EVERLASTING PROMISE</small>
        <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
        <p>{{ wedding.openingText }}</p>
      </div>
      <span class="edition-label">{{ wedding.date.year }} — EXCLUSIVE ISSUE</span></template
    >
    <template v-else-if="design === 'pure'"
      ><header class="pure-hero-header">
        <small>{{ wedding.date.display }}</small>
        <h1>{{ wedding.bride.shortName }} & {{ wedding.groom.shortName }}</h1>
      </header>
      <img class="pure-hero-photo" :src="wedding.hero || wedding.cover" alt="Potret pasangan" />
      <p class="pure-hero-caption">{{ wedding.openingText }}</p></template
    >
    <template v-else-if="design === 'sakinah' || design === 'nusantara'"
      ><small>{{ design === 'sakinah' ? 'بِسْمِ اللَّهِ' : 'DENGAN PENUH RASA SYUKUR' }}</small>
      <div class="framed-hero-photo">
        <img :src="wedding.hero || wedding.cover" alt="Potret pasangan" />
      </div>
      <div class="hero-copy">
        <h1>{{ wedding.bride.shortName }} <i>&</i> {{ wedding.groom.shortName }}</h1>
        <p>{{ wedding.openingText }}</p>
      </div></template
    >
    <template v-else
      ><img class="hero-full-photo" :src="wedding.hero || wedding.cover" alt="Potret pasangan" />
      <div class="hero-copy">
        <small>{{
          design === 'cinema'
            ? 'A STORY BY TWO HEARTS'
            : design === 'garden'
              ? 'BENEATH THE OPEN SKY'
              : 'LOVE, AFTER DARK'
        }}</small>
        <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
        <p>{{ wedding.openingText }}</p>
      </div></template
    >
    <button
      class="hero-scroll"
      @click="scrollToSection(design === 'cinema' ? 'story' : 'couple')"
      aria-label="Lanjutkan cerita"
    >
      ↓
    </button>
  </section>
</template>
