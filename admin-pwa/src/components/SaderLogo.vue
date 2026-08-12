<template>
  <div class="sader-logo" :class="[`layout-${layout}`, { 'on-dark': dark }]">
    <span class="sader-badge" :style="{ width: size + 'px', height: size + 'px' }">
      <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" class="sader-badge-svg">
        <defs>
          <linearGradient :id="gradId" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#22c55e"/>
            <stop offset="55%" stop-color="#15803d"/>
            <stop offset="100%" stop-color="#0f4c26"/>
          </linearGradient>
          <linearGradient :id="gradId + '-accent'" x1="30" y1="70" x2="82" y2="26" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#f5c451"/>
            <stop offset="100%" stop-color="#d99a2b"/>
          </linearGradient>
        </defs>
        <rect x="1" y="1" width="98" height="98" rx="26" :fill="`url(#${gradId})`"/>
        <rect x="1" y="1" width="98" height="98" rx="26" fill="none" stroke="rgba(255,255,255,0.14)" stroke-width="1.5"/>
        <path d="M50 74c-13 0-23-10-23-23 0-12 8-22 20-24 1 12 3 20 9 27 6-9 7-18 6-29 12 3 19 13 19 26 0 13-10 23-23 23z"
          fill="#fff" opacity="0.97"/>
        <path d="M50 74V50" stroke="#0f4c26" stroke-width="3" stroke-linecap="round" opacity="0.5"/>
        <circle cx="74" cy="30" r="7" :fill="`url(#${gradId}-accent)`"/>
      </svg>
    </span>

    <span v-if="!iconOnly" class="sader-wordmark">
      <span class="sader-title">SADER</span>
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
  iconOnly: { type: Boolean, default: false },
});
const gradId = 'sader-grad-' + Math.random().toString(36).slice(2, 9);
</script>

<style scoped>
.sader-logo {
  display: flex;
  align-items: center;
  gap: 14px;
  user-select: none;
}
.layout-stack {
  flex-direction: column;
  text-align: center;
  gap: 10px;
}

.sader-badge {
  flex-shrink: 0;
  display: block;
  filter: drop-shadow(0 6px 16px rgba(15, 76, 38, 0.28));
}
.sader-badge-svg { width: 100%; height: 100%; display: block; }

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
