<script setup>
import HeroSection from './HeroSection.vue'
import WeddingQuote from './WeddingQuote.vue'
import CoupleSection from './CoupleSection.vue'
import CountdownSection from './CountdownSection.vue'
import LoveStory from './LoveStory.vue'
import EventSection from './EventSection.vue'
import GallerySection from './GallerySection.vue'
import VideoSection from './VideoSection.vue'
import LocationSection from './LocationSection.vue'
import RSVPSection from './RSVPSection.vue'
import WishesSection from './WishesSection.vue'
import WeddingGift from './WeddingGift.vue'
import LiveStreaming from './LiveStreaming.vue'
import ClosingSection from './ClosingSection.vue'
import { useScrollAnimation } from '../composables/useScrollAnimation'
defineProps({ guest: String })
defineEmits(['toast'])
useScrollAnimation()
</script>
<template><div class="invitation-content"><HeroSection /><WeddingQuote /><CoupleSection /><CountdownSection /><LoveStory /><EventSection /><GallerySection /><VideoSection /><LocationSection /><RSVPSection :guest="guest" /><WishesSection :guest="guest" /><WeddingGift @toast="$emit('toast', $event)" /><LiveStreaming /><ClosingSection /></div></template>
