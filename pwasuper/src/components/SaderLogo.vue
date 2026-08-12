<template>
  <div class="sader-logo" :class="[`layout-${layout}`, { 'on-dark': dark }]">
    <span class="sader-wordmark">
      <span class="sader-title" :style="{ fontSize: titleSize }">SADER</span>
      <span v-if="subtitle" class="sader-subtitle">App de Seguimiento</span>
    </span>
  </div>
</template>

<script setup>
defineProps({
  size: { type: Number, default: 56 },
  subtitle: { type: Boolean, default: true },
  layout: { type: String, default: 'row' }, // 'row' | 'stack'
  dark: { type: Boolean, default: false },
  titleSize: { type: String, default: null },
});
</script>

<style scoped>
.sader-logo {
  display: flex;
  align-items: center;
  user-select: none;
}
.layout-stack {
  flex-direction: column;
  text-align: center;
}

.sader-wordmark {
  display: flex;
  flex-direction: column;
  line-height: 1.05;
}
.layout-stack .sader-wordmark { align-items: center; }

.sader-title {
  font-family: -apple-system, 'SF Pro Display', 'Inter', system-ui, sans-serif;
  font-weight: 800;
  font-size: clamp(20px, 3.2vh, 30px);
  letter-spacing: 0.5px;
  background: linear-gradient(120deg, #15803d 0%, #16a34a 55%, #d99a2b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.on-dark .sader-title {
  background: linear-gradient(120deg, #bbf7d0 0%, #4ade80 55%, #f5c451 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sader-subtitle {
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 500;
  font-size: clamp(10px, 1.4vh, 12.5px);
  letter-spacing: 0.3px;
  color: #5b7f68;
  margin-top: 2px;
}
.on-dark .sader-subtitle { color: rgba(255,255,255,0.62); }
</style>
