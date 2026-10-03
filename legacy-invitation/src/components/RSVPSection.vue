<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { ref } from 'vue'
import { Minus, Plus, Send, CheckCircle2 } from 'lucide-vue-next'
import { invitationRepository } from '../services/storage'
import SectionHeading from './SectionHeading.vue'
const props = defineProps({ guest: String })
const name = ref(props.guest === 'Tamu Undangan' ? '' : props.guest)
const guests = ref(1), attendance = ref(''), message = ref(''), error = ref(''), success = ref(false), pending = ref(false)
async function submit() {
  error.value = ''; success.value = false
  if (name.value.trim().length < 2 || !attendance.value) { error.value = 'Mohon isi nama dan pilih konfirmasi kehadiran.'; return }
  pending.value = true
  try { await invitationRepository.add('rsvps', { name: name.value.trim(), guests: guests.value, attendance: attendance.value, message: message.value.trim() }); success.value = true }
  catch { error.value = 'Konfirmasi belum tersimpan. Izinkan penyimpanan browser lalu coba kembali.' }
  finally { pending.value = false }
}
</script>
<template><section id="rsvp" class="section rsvp-section"><FlowerMotion /><SectionHeading eyebrow="RSVP" title="Will you attend?" subtitle="Kami menantikan kehadiran Anda di hari istimewa kami." /><form class="invitation-form" @submit.prevent="submit" data-reveal><label for="rsvp-name">Nama lengkap <span>*</span></label><input id="rsvp-name" v-model="name" required minlength="2" maxlength="120" autocomplete="name" placeholder="Tulis nama Anda" /><div class="guest-counter"><label for="guest-number">Jumlah tamu</label><div><button type="button" class="icon-button" aria-label="Kurangi jumlah tamu" :disabled="guests <= 1" @click="guests--"><Minus :size="16" /></button><output id="guest-number" aria-live="polite">{{ guests }}</output><button type="button" class="icon-button" aria-label="Tambah jumlah tamu" :disabled="guests >= 10" @click="guests++"><Plus :size="16" /></button></div></div><fieldset><legend>Konfirmasi kehadiran <span>*</span></legend><label v-for="option in ['Hadir', 'Tidak Hadir', 'Masih Ragu']" :key="option" class="radio-option"><input v-model="attendance" type="radio" name="attendance" :value="option" required /><span>{{ option }}</span></label></fieldset><label for="rsvp-message">Pesan <small>(opsional)</small></label><textarea id="rsvp-message" v-model="message" maxlength="1000" rows="3" placeholder="Tinggalkan pesan untuk kami…"></textarea><button class="button full-width" :disabled="pending"><Send :size="15" />{{ pending ? 'Menyimpan…' : 'Kirim Konfirmasi' }}</button><p v-if="error" class="form-error" role="alert">{{ error }}</p><p v-if="success" class="form-success" role="status"><CheckCircle2 :size="18" />Terkirim! Terima kasih atas konfirmasinya.</p><p class="storage-note">Konfirmasi tersimpan di perangkat ini. Versi demo belum mengirim ke pasangan.</p></form></section></template>
