<script setup>defineProps({ eyebrow: String, title: String, subtitle: String })</script>
<template><header class="section-heading" data-reveal><p class="eyebrow">{{ eyebrow }}</p><h2>{{ title }}</h2><div class="tiny-divider"><span></span><i>✦</i><span></span></div><p v-if="subtitle" class="section-subtitle">{{ subtitle }}</p></header></template>
