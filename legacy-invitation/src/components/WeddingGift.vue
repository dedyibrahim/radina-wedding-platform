<script setup>
import FlowerMotion from './FlowerMotion.vue'
import { ref } from 'vue'
import { Copy, Gift, MapPin } from 'lucide-vue-next'
import { wedding } from '../data/wedding'
import SectionHeading from './SectionHeading.vue'
import BaseModal from './BaseModal.vue'
const emit = defineEmits(['toast'])
const addressOpen = ref(false)
async function copy(number) {
  try { await navigator.clipboard.writeText(number); emit('toast', 'Nomor rekening berhasil disalin.') }
  catch { emit('toast', 'Salin secara manual: ' + number) }
}
</script>
<template><section class="section gift-section"><FlowerMotion /><SectionHeading eyebrow="WEDDING GIFT" title="A little token of love" subtitle="Doa restu Anda merupakan karunia yang sangat berarti bagi kami. Namun jika memberi adalah ungkapan tanda kasih, Anda dapat memberikan tanda kasih melalui:" /><div class="bank-list"><article v-for="account in wedding.bankAccounts" :key="account.bank" class="bank-card" data-reveal><div class="bank-header"><span>{{ account.bank }}</span><span class="bank-symbol" aria-hidden="true">✦</span></div><p class="bank-number">{{ account.number }}</p><p class="bank-owner">{{ account.owner }}</p><button class="copy-button" @click="copy(account.number)"><Copy :size="14" /> Salin Rekening</button></article></div><button class="button button-outline" @click="addressOpen = true"><Gift :size="16" /> Kirim Hadiah</button><p class="sample-note">Rekening dan alamat contoh — bukan untuk transaksi.</p><BaseModal :open="addressOpen" title="Alamat pengiriman hadiah" @close="addressOpen = false"><div class="address-modal"><MapPin :size="28" /><p class="eyebrow">A GIFT FROM THE HEART</p><h2>Alamat pengiriman</h2><p>{{ wedding.giftAddress }}</p><p class="sample-note">Alamat contoh. Konfirmasikan dengan pasangan sebelum mengirim.</p><button class="button" @click="addressOpen = false">Terima kasih</button></div></BaseModal></section></template>
