import { ref, onUnmounted } from 'vue'
export function useAudio(src) {
  const playing = ref(false)
  const error = ref('')
  let audio
  async function play() {
    if (!audio) {
      audio = new Audio(src)
      audio.loop = true
      audio.volume = 0.4
      audio.preload = 'none'
    }
    try { await audio.play(); playing.value = true; error.value = '' }
    catch { playing.value = false; error.value = 'Musik belum dapat diputar. Tekan tombol musik untuk mencoba kembali.' }
  }
  function pause() { audio?.pause(); playing.value = false }
  function toggle() { if (playing.value) pause(); else play() }
  onUnmounted(() => { audio?.pause(); if (audio) audio.src = '' })
  return { playing, error, play, pause, toggle }
}
