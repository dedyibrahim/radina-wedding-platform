<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { ref, onMounted, onUnmounted } from 'vue'
import { Send } from 'lucide-vue-next'
import SectionHeading from './SectionHeading.vue'
import { invitationRepository } from '../services/storage'
const props = defineProps({ guest: String })
const name = ref(props.guest === 'Tamu Undangan' ? '' : props.guest), message = ref(''), error = ref(''), pending = ref(false)
const seed = { id: 'sample', name: 'Andi', message: 'Selamat menempuh hidup baru. Semoga menjadi keluarga yang selalu diberikan kebahagiaan.', createdAt: new Date().toISOString(), sample: true }
const wishes = ref([seed]), now = ref(Date.now())
let interval
onMounted(() => { wishes.value = [...invitationRepository.read('wishes').filter(x => typeof x.name === 'string' && typeof x.message === 'string'), seed]; interval = setInterval(() => { now.value = Date.now() }, 60000) })
onUnmounted(() => clearInterval(interval))
function relative(wish) { if (wish.sample) return 'Contoh ucapan'; const minutes = Math.max(0, Math.floor((now.value - new Date(wish.createdAt).getTime()) / 60000)); if (minutes < 1) return 'Baru saja'; if (minutes < 60) return `${minutes} menit lalu`; if (minutes < 1440) return `${Math.floor(minutes / 60)} jam lalu`; return `${Math.floor(minutes / 1440)} hari lalu` }
async function submit() {
  error.value = ''
  if (name.value.trim().length < 2 || message.value.trim().length < 5) { error.value = 'Mohon isi nama dan ucapan minimal 5 karakter.'; return }
  pending.value = true
  try { const wish = await invitationRepository.add('wishes', { name: name.value.trim(), message: message.value.trim() }); wishes.value.unshift(wish); message.value = ''; now.value = Date.now() }
  catch { error.value = 'Ucapan belum tersimpan. Periksa izin penyimpanan browser Anda.' }
  finally { pending.value = false }
}
</script>
<template><section class="section wishes-section"><FlowerMotion /><SectionHeading eyebrow="WEDDING WISHES" title="Words from the heart" subtitle="Sebuah doa kecil dari Anda, kebahagiaan besar untuk kami." /><form class="invitation-form" @submit.prevent="submit" data-reveal><label for="wish-name">Nama</label><input id="wish-name" v-model="name" required minlength="2" maxlength="120" autocomplete="name" placeholder="Nama Anda" /><label for="wish-message">Ucapan & doa</label><textarea id="wish-message" v-model="message" required minlength="5" maxlength="1000" rows="3" placeholder="Tuliskan doa terbaik Anda…"></textarea><button class="button full-width" :disabled="pending"><Send :size="15" /> {{ pending ? 'Menyimpan…' : 'Kirim Ucapan' }}</button><p v-if="error" class="form-error" role="alert">{{ error }}</p><p class="storage-note">Ucapan tersimpan dan terlihat di perangkat ini.</p></form><div class="wishes-list" aria-live="polite"><article v-for="wish in wishes" :key="wish.id" class="wish"><div class="wish-avatar">{{ Array.from(wish.name)[0]?.toUpperCase() }}</div><div><h3>{{ wish.name }}</h3><p>{{ wish.message }}</p><time>{{ relative(wish) }}</time></div></article></div></section></template>
