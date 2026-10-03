<script setup>
import { ref, nextTick, onUnmounted, watch } from 'vue'
import WeddingCover from './components/WeddingCover.vue'
import InvitationContent from './components/InvitationContent.vue'
import AudioPlayer from './components/AudioPlayer.vue'
import FloatingNavigation from './components/FloatingNavigation.vue'
import BaseToast from './components/BaseToast.vue'
import BotanicalOrnament from './components/BotanicalOrnament.vue'
import { useAudio } from './composables/useAudio'
import { getGuestName } from './composables/useGuest'
import { wedding } from './data/wedding'
const opened = ref(false), guest = getGuestName(), toast = ref('')
const { playing, error, play, toggle } = useAudio(wedding.music)
let toastTimeout
function showToast(message) { toast.value = message; clearTimeout(toastTimeout); toastTimeout = setTimeout(() => { toast.value = '' }, 4500) }
watch(error, value => { if (value) showToast(value) })
async function openInvitation() { play(); opened.value = true; await nextTick(); window.scrollTo({ top: 0, behavior: 'instant' }); document.getElementById('invitation')?.focus({ preventScroll: true }) }
onUnmounted(() => clearTimeout(toastTimeout))
</script>
<template>
  <div class="desktop-ambience" aria-hidden="true"><BotanicalOrnament class="ambient-left" /><BotanicalOrnament class="ambient-right" /><div class="desktop-note"><div class="desktop-monogram">A <em>&</em> R</div><div class="tiny-divider"><span></span><i>✦</i><span></span></div><p>A PROMISE<br />OF FOREVER</p><small>12 DECEMBER 2026</small></div><div class="desktop-right-note"><span>Love is a journey.</span><p>Thank you for being<br />a part of ours.</p></div></div>
  <main class="invitation-shell" id="invitation" tabindex="-1"><Transition name="cover" mode="out-in"><WeddingCover v-if="!opened" :guest="guest" @open="openInvitation" /><InvitationContent v-else :guest="guest" @toast="showToast" /></Transition></main>
  <template v-if="opened"><AudioPlayer :playing="playing" @toggle="toggle" /><FloatingNavigation /></template><BaseToast :message="toast" />
</template>
