<script setup>
import { inject } from 'vue'
defineProps({ design: String, guest: String })
defineEmits(['open'])
const wedding = inject('wedding')
</script>
<template>
  <section class="design-cover" :class="`cover-${design}`" aria-label="Opening invitation">
    <template v-if="design === 'noir'"
      ><div class="noir-title">
        <small>THE WEDDING ISSUE</small>
        <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
        <span>NO. 01 / {{ wedding.date.year }}</span>
      </div>
      <img class="cover-photo" :src="wedding.cover" alt="Foto pasangan" fetchpriority="high"
    /></template>
    <template v-else-if="design === 'pure'"
      ><small>THE WEDDING OF</small>
      <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
      <div class="pure-rule"></div>
      <p>{{ wedding.openingText }}</p></template
    >
    <template v-else-if="design === 'letters'"
      ><div class="envelope-flap"></div>
      <div class="letter-sheet">
        <small>A LETTER FOR YOU</small>
        <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
        <p>{{ wedding.openingText }}</p>
        <span class="letter-stamp">WITH LOVE<br />{{ wedding.date.year }}</span>
      </div></template
    >
    <template v-else-if="design === 'nusantara'"
      ><div class="gate gate-left"></div>
      <div class="gate gate-right"></div>
      <img class="cover-photo" :src="wedding.cover" alt="Foto pasangan" fetchpriority="high" />
      <div class="cover-title">
        <small>UNDANGAN PERNIKAHAN</small>
        <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
      </div></template
    >
    <template v-else-if="design === 'sakinah'"
      ><div class="sakinah-arch">
        <span class="bismillah" lang="ar">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</span
        ><img :src="wedding.cover" alt="Foto pasangan" fetchpriority="high" />
        <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
      </div></template
    >
    <template v-else-if="design === 'daydream'"
      ><span class="pastel-blob blob-one"></span><span class="pastel-blob blob-two"></span
      ><img class="daydream-photo" :src="wedding.cover" alt="Foto pasangan" fetchpriority="high" />
      <div class="cover-title">
        <small>WE'RE GETTING MARRIED!</small>
        <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
      </div>
      <span class="doodle-heart" aria-hidden="true">♡</span></template
    >
    <template v-else
      ><img class="cover-photo" :src="wedding.cover" alt="Foto pasangan" fetchpriority="high" />
      <div v-if="design === 'garden'" class="garden-arch" aria-hidden="true">❧</div>
      <div v-if="design === 'amore'" class="floral-corner" aria-hidden="true">✿<span>❧</span></div>
      <div class="cover-title">
        <small>{{ design === 'cinema' ? 'EVERY STORY HAS A BEGINNING' : 'THE WEDDING OF' }}</small>
        <h1>{{ wedding.bride.shortName }}<i>&</i>{{ wedding.groom.shortName }}</h1>
        <p v-if="design === 'cinema'">This is ours.</p>
      </div></template
    >
    <div class="cover-invitation">
      <p class="cover-date">{{ wedding.date.display }}</p>
      <small>Kepada Yth. Bapak/Ibu/Saudara/i</small><strong class="cover-guest">{{ guest }}</strong
      ><button class="button" aria-label="Buka Undangan" @click="$emit('open')">
        {{
          design === 'letters'
            ? 'Open Letter'
            : design === 'cinema'
              ? 'Begin Our Story'
              : design === 'amore'
                ? 'Open Our Invitation'
                : 'Buka Undangan'
        }}
        <span aria-hidden="true">↗</span>
      </button>
    </div>
  </section>
</template>
