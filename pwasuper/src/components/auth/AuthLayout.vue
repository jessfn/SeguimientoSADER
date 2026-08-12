<template>
  <div class="au-root">
    <!-- Fondo compartido por las tres pantallas de autenticación -->
    <div class="au-mesh" aria-hidden="true">
      <span class="b1"></span><span class="b2"></span>
      <span class="b3"></span><span class="b4"></span>
    </div>

    <!-- Partículas ascendentes (luciérnagas) sobre el mesh -->
    <div class="au-dust" aria-hidden="true">
      <i></i><i></i><i></i><i></i><i></i>
      <i></i><i></i><i></i><i></i><i></i>
    </div>

    <div class="shell" :class="{ 'shell-wide': wide }">
      <!-- Columna de marca (solo desktop) -->
      <aside class="brand">
        <div class="brand-inner">
          <div class="brand-badge">
            <i></i>{{ badge }}
          </div>

          <span class="au-wordmark on-dark brand-mark">
            <b>SADER</b>
            <small>App de Seguimiento</small>
          </span>

          <p class="brand-desc">{{ desc }}</p>

          <ul class="brand-list">
            <li v-for="f in features" :key="f">
              <span class="brand-check">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6"
                     stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              </span>
              {{ f }}
            </li>
          </ul>
        </div>
      </aside>

      <!-- Columna del formulario -->
      <main class="pane">
        <div class="au-card" :style="{ maxWidth: maxWidth }">
          <!-- Wordmark visible solo cuando la columna de marca está oculta -->
          <span class="au-wordmark card-mark"><b>SADER</b></span>
          <slot />
        </div>

        <p class="au-copy pane-copy">© 2026 SADER · Todos los derechos reservados</p>
      </main>
    </div>
  </div>
</template>

<script setup>
defineProps({
  wide: { type: Boolean, default: false },
  maxWidth: { type: String, default: '410px' },
  badge: { type: String, default: 'Sistema Oficial de Seguimiento' },
  desc: {
    type: String,
    default: 'Plataforma de seguimiento y reporte de actividades en campo, con soporte para trabajar sin conexión.',
  },
  features: {
    type: Array,
    default: () => [
      'Geolocalización en tiempo real',
      'Registro de asistencias',
      'Funciona sin conexión',
    ],
  },
});
</script>

<style scoped>
.shell {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: clamp(28px, 5vw, 76px);
  padding: clamp(16px, 3vh, 34px) clamp(14px, 3vw, 32px);
}

/* ── Columna de marca ── */
.brand { display: none; }
.brand-inner {
  display: flex;
  flex-direction: column;
  gap: clamp(12px, 2vh, 20px);
  max-width: 360px;
  color: var(--au-on-dark);
}

.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 6px 14px;
  border-radius: 99px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(8px);
  font-size: clamp(10px, 1.3vh, 11.5px);
  font-weight: 600;
  letter-spacing: 0.4px;
}
.brand-badge i {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--au-green-300);
  box-shadow: 0 0 8px rgba(74, 222, 128, 0.85);
  animation: au-blink 2s ease-in-out infinite;
}
@keyframes au-blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }

.brand-mark { align-items: flex-start; }
.brand-mark :deep(b) { font-size: clamp(32px, 5.4vh, 48px); }
.brand-mark :deep(small) { font-size: clamp(11px, 1.5vh, 13px); }

.brand-desc {
  margin: 0;
  font-size: clamp(12px, 1.6vh, 14px);
  line-height: 1.55;
  color: var(--au-on-dark-soft);
}

.brand-list {
  list-style: none;
  margin: 0; padding: 0;
  display: flex;
  flex-direction: column;
  gap: clamp(7px, 1.3vh, 11px);
}
.brand-list li {
  display: flex;
  align-items: center;
  gap: 11px;
  font-size: clamp(11.5px, 1.5vh, 13px);
  font-weight: 500;
  color: var(--au-on-dark);
}
.brand-check {
  display: flex; align-items: center; justify-content: center;
  width: 22px; height: 22px; flex-shrink: 0;
  border-radius: 50%;
  background: rgba(74, 222, 128, 0.16);
  border: 1px solid rgba(74, 222, 128, 0.3);
  color: var(--au-green-300);
}
.brand-check svg { width: 11px; height: 11px; }

/* ── Columna del formulario ── */
.pane {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.pane > .au-card { margin: 0 auto; }
.pane-copy { display: none; }

.card-mark {
  align-self: center;
  margin-bottom: 12px;
}

/* ── Desktop ── */
@media (min-width: 1000px) {
  .shell { flex-direction: row; align-items: center; justify-content: center; }
  .brand { display: flex; }
  .pane { width: auto; }
  /* En desktop la marca vive en la columna izquierda */
  .card-mark { display: none; }
  .pane-copy { display: block; }
}

/* El registro necesita más ancho: su columna de marca aparece más tarde */
.shell-wide .brand { display: none; }
@media (min-width: 1180px) {
  .shell-wide .brand { display: flex; }
  .shell-wide .card-mark { display: none; }
}
@media (max-width: 1179px) {
  .shell-wide .card-mark { display: flex; }
}
</style>
