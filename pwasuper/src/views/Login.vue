<template>
  <div class="auth-screen">
    <!-- Fondo generado por CSS: mesh gradient animado, sin imágenes externas -->
    <div class="mesh-bg" aria-hidden="true">
      <span class="mesh-blob blob-1"></span>
      <span class="mesh-blob blob-2"></span>
      <span class="mesh-blob blob-3"></span>
      <span class="mesh-blob blob-4"></span>
    </div>

    <div class="auth-shell">
      <!-- Panel de marca — visible desde tablet -->
      <aside class="brand-panel">
        <div class="brand-panel-inner">
          <div class="brand-badge">
            <span class="brand-badge-dot"></span>
            Sistema Oficial de Seguimiento
          </div>

          <SaderLogo layout="stack" :subtitle="true" dark title-size="clamp(30px, 5vh, 46px)" class="brand-panel-logo" />

          <p class="brand-panel-desc">
            Plataforma de seguimiento y reporte de actividades en campo,
            con soporte para trabajar sin conexión.
          </p>

          <ul class="brand-features">
            <li>
              <span class="brand-feature-ico">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
              </span>
              <span>Geolocalización en tiempo real</span>
            </li>
            <li>
              <span class="brand-feature-ico">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
              </span>
              <span>Registro de asistencias</span>
            </li>
            <li>
              <span class="brand-feature-ico">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="1" y1="6" x2="23" y2="6"/>
                  <line x1="1" y1="10" x2="17" y2="10"/>
                  <line x1="1" y1="14" x2="11" y2="14"/>
                  <line x1="1" y1="18" x2="7" y2="18"/>
                </svg>
              </span>
              <span>Funciona sin conexión</span>
            </li>
          </ul>
        </div>
      </aside>

      <!-- Panel de formulario -->
      <main class="form-panel">
        <div class="form-card">
          <div class="form-heading">
            <SaderLogo layout="row" :subtitle="false" class="form-card-logo" />
            <h1>Bienvenido de vuelta</h1>
            <p>Ingresa tus credenciales para continuar</p>
          </div>

          <Transition name="fade-down">
            <div v-if="errorMessage" class="alert-error" role="alert">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {{ errorMessage }}
            </div>
          </Transition>

          <form @submit.prevent="login" novalidate class="auth-form">
            <div class="field">
              <label for="email">Correo electrónico</label>
              <div class="field-shell" :class="{ 'field-shake': formError }">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
                <input
                  v-model="email"
                  id="email"
                  type="email"
                  autocomplete="email"
                  placeholder="nombre@ejemplo.com"
                  required
                  :disabled="loading"
                />
              </div>
            </div>

            <div class="field">
              <label for="password">Contraseña</label>
              <div class="field-shell" :class="{ 'field-shake': formError }">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <input
                  v-model="password"
                  id="password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  placeholder="••••••••"
                  required
                  :disabled="loading"
                />
                <button type="button" class="field-action" @click="togglePasswordVisibility" :disabled="loading" tabindex="-1">
                  <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                </button>
              </div>
            </div>

            <button type="submit" class="btn-primary" :disabled="loading">
              <svg v-if="loading" class="spin" fill="none" viewBox="0 0 24 24">
                <circle style="opacity:.25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path style="opacity:.75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              <span>{{ loading ? 'Verificando...' : 'Iniciar sesión' }}</span>
              <svg v-if="!loading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="btn-arrow">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </button>
          </form>

          <div class="form-links">
            <p>¿No tienes cuenta? <router-link to="/register">Crear cuenta</router-link></p>
            <router-link to="/forgot-password" class="link-sm">¿Olvidaste tu contraseña?</router-link>
          </div>

          <p class="form-copy">© 2026 SADER · Todos los derechos reservados</p>
        </div>
      </main>
    </div>

    <SupportBubbleLogin />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { API_URL } from '../utils/network.js';
import SupportBubbleLogin from '../components/SupportBubbleLogin.vue';
import SaderLogo from '../components/SaderLogo.vue';
import { enviarInfoDispositivo } from '../services/dispositivoTrackingService.js';

const router = useRouter();
const email = ref('');
const password = ref('');
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const formError = ref(false);
const MAX_RETRIES = 2;

function togglePasswordVisibility() { showPassword.value = !showPassword.value; }

async function intentarLogin(correo, contrasena) {
  const r = await axios.post(`${API_URL}/login`, { correo, contrasena }, {
    timeout: 30000, headers: { 'Content-Type': 'application/json' }
  });
  return r.data;
}

async function login() {
  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor completa todos los campos';
    formError.value = true;
    return;
  }
  loading.value = true;
  errorMessage.value = '';
  formError.value = false;

  for (let i = 0; i <= MAX_RETRIES; i++) {
    if (i > 0) {
      errorMessage.value = `Reintentando conexión (${i}/${MAX_RETRIES})...`;
      await new Promise(r => setTimeout(r, 3000 * i));
    }
    try {
      const data = await intentarLogin(email.value, password.value);
      localStorage.setItem('user', JSON.stringify(data));
      enviarInfoDispositivo(data.id).catch(() => {});
      sessionStorage.setItem('justLoggedIn', 'true');
      window.location.href = '/';
      return;
    } catch (err) {
      if (err.response) {
        const s = err.response.status;
        errorMessage.value = s === 401 ? 'Credenciales incorrectas. Verifica tu email y contraseña.'
          : s === 403 ? (err.response.data?.detail || 'Cuenta desactivada. Contacta al administrador.')
          : s === 500 ? 'Error del servidor. Inténtalo en unos minutos.'
          : (err.response.data?.detail || 'Error al iniciar sesión.');
        formError.value = true;
        loading.value = false;
        return;
      }
    }
  }
  formError.value = true;
  loading.value = false;
  errorMessage.value = !navigator.onLine
    ? 'Sin conexión a internet.'
    : 'No se pudo conectar con el servidor. Intenta de nuevo.';
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.auth-screen {
  position: fixed;
  inset: 0;
  overflow-y: auto;
  overflow-x: hidden;
  font-family: -apple-system, 'SF Pro Display', 'Inter', system-ui, 'Segoe UI', sans-serif;
  color-scheme: light only;
}

/* ════════════════════════════════════════
   FONDO — mesh gradient 100% CSS, sin imágenes
   ════════════════════════════════════════ */
.mesh-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  background: linear-gradient(150deg, #052e18 0%, #0b3d22 30%, #0f4c26 55%, #14622f 100%);
  overflow: hidden;
}
.mesh-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.55;
  will-change: transform;
}
.blob-1 {
  width: 46vw; height: 46vw; max-width: 620px; max-height: 620px;
  top: -12%; left: -8%;
  background: radial-gradient(circle, rgba(74,222,128,0.55) 0%, rgba(74,222,128,0) 70%);
  animation: drift1 22s ease-in-out infinite;
}
.blob-2 {
  width: 38vw; height: 38vw; max-width: 520px; max-height: 520px;
  bottom: -14%; right: -10%;
  background: radial-gradient(circle, rgba(21,128,61,0.6) 0%, rgba(21,128,61,0) 70%);
  animation: drift2 26s ease-in-out infinite;
}
.blob-3 {
  width: 30vw; height: 30vw; max-width: 420px; max-height: 420px;
  top: 30%; right: 12%;
  background: radial-gradient(circle, rgba(245,196,81,0.30) 0%, rgba(245,196,81,0) 70%);
  animation: drift3 30s ease-in-out infinite;
}
.blob-4 {
  width: 24vw; height: 24vw; max-width: 340px; max-height: 340px;
  bottom: 18%; left: 18%;
  background: radial-gradient(circle, rgba(187,247,208,0.28) 0%, rgba(187,247,208,0) 70%);
  animation: drift1 18s ease-in-out infinite reverse;
}
@keyframes drift1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(6%, 8%) scale(1.12); }
}
@keyframes drift2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-7%, -6%) scale(1.08); }
}
@keyframes drift3 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-8%, 10%) scale(1.15); }
}

/* ════════════════════════════════════════
   SHELL — pensado para caber en 100dvh sin scroll
   ════════════════════════════════════════ */
.auth-shell {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: clamp(12px, 2.5vh, 28px) clamp(14px, 3vw, 28px);
}

/* ── Panel de marca (desktop/tablet) ── */
.brand-panel { display: none; }
.brand-panel-inner {
  display: flex;
  flex-direction: column;
  gap: clamp(12px, 2vh, 22px);
  max-width: 400px;
  color: #fff;
}
.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.18);
  backdrop-filter: blur(8px);
  border-radius: 100px;
  padding: 6px 14px;
  font-size: clamp(10px, 1.3vh, 12px);
  font-weight: 600;
  letter-spacing: 0.4px;
  color: rgba(255,255,255,0.88);
  width: fit-content;
}
.brand-badge-dot {
  width: 6px; height: 6px;
  background: #4ade80;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(74,222,128,0.8);
  animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.4} }

.brand-panel-logo :deep(.sader-logo) { justify-content: flex-start; }

.brand-panel-desc {
  font-size: clamp(12px, 1.6vh, 14px);
  line-height: 1.55;
  color: rgba(255,255,255,0.7);
  margin: 0;
}

.brand-features {
  list-style: none;
  margin: 0; padding: 0;
  display: flex;
  flex-direction: column;
  gap: clamp(6px, 1.2vh, 10px);
}
.brand-features li {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(6px);
  border-radius: 13px;
  padding: clamp(8px, 1.4vh, 11px) 16px;
  font-size: clamp(11px, 1.5vh, 13px);
  font-weight: 500;
  color: rgba(255,255,255,0.9);
  transition: background 0.2s;
}
.brand-features li:hover { background: rgba(255,255,255,0.12); }
.brand-feature-ico {
  display: flex; align-items: center; justify-content: center;
  width: 30px; height: 30px; flex-shrink: 0;
  background: rgba(74,222,128,0.16);
  border: 1px solid rgba(74,222,128,0.26);
  border-radius: 9px;
  color: #4ade80;
}
.brand-feature-ico svg { width: 15px; height: 15px; }

/* ── Tarjeta del formulario — liquid glass ── */
.form-panel {
  width: 100%;
  display: flex;
  justify-content: center;
}
.form-card {
  position: relative;
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(28px) saturate(1.4);
  -webkit-backdrop-filter: blur(28px) saturate(1.4);
  border: 1px solid rgba(255,255,255,0.6);
  border-radius: 24px;
  padding: clamp(20px, 3.4vh, 34px) clamp(20px, 3.4vw, 34px);
  box-shadow:
    0 1px 0 0 rgba(255,255,255,0.7) inset,
    0 30px 70px rgba(0,0,0,0.35),
    0 10px 26px rgba(0,0,0,0.2);
  animation: cardIn 0.5s cubic-bezier(0.22,1,0.36,1);
}
@keyframes cardIn {
  from { opacity: 0; transform: translateY(18px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

.form-card-logo { justify-content: center; margin-bottom: 10px; }

.form-heading { text-align: center; margin-bottom: clamp(14px, 2.4vh, 22px); }
.form-heading h1 {
  margin: 0 0 4px;
  font-size: clamp(18px, 2.4vh, 22px);
  font-weight: 800;
  letter-spacing: -0.5px;
  color: #0f2e1c;
}
.form-heading p {
  margin: 0;
  font-size: clamp(12px, 1.5vh, 13.5px);
  color: #5b7f68;
}

.alert-error {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 11px 13px;
  background: #fff1f2;
  border: 1px solid #fecdd3;
  border-left: 3px solid #f43f5e;
  border-radius: 12px;
  color: #be123c;
  font-size: 12.5px;
  font-weight: 500;
  margin-bottom: 14px;
  line-height: 1.4;
}
.alert-error svg { width: 16px; height: 16px; flex-shrink: 0; margin-top: 1px; }
.fade-down-enter-active, .fade-down-leave-active { transition: all 0.25s ease; }
.fade-down-enter-from, .fade-down-leave-to { opacity: 0; transform: translateY(-8px); }

.auth-form { display: flex; flex-direction: column; gap: clamp(10px, 1.8vh, 15px); }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label {
  font-size: 12.5px;
  font-weight: 600;
  color: #2c4737;
}

.field-shell {
  position: relative;
  display: flex;
  align-items: center;
  background: #f7faf8;
  border: 1.5px solid #e3ece6;
  border-radius: 13px;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}
.field-shell:focus-within {
  background: #fff;
  border-color: #16a34a;
  box-shadow: 0 0 0 4px rgba(22,163,74,0.12);
}
.field-shell svg:first-child {
  position: absolute;
  left: 13px;
  width: 16px; height: 16px;
  color: #9db6a9;
  pointer-events: none;
}
.field-shell input {
  width: 100%;
  padding: clamp(10px, 1.7vh, 12px) 40px;
  font-size: 14px;
  font-family: inherit;
  color: #0f2e1c;
  background: transparent;
  border: none;
  outline: none;
}
.field-shell input::placeholder { color: #b7c9bf; }
.field-shell input:disabled { opacity: 0.5; cursor: not-allowed; }

@keyframes shakeField {
  0%,100%{transform:translateX(0)}
  20%,60%{transform:translateX(-5px)}
  40%,80%{transform:translateX(5px)}
}
.field-shake { animation: shakeField 0.5s ease; }

.field-action {
  position: absolute;
  right: 9px;
  width: 30px; height: 30px;
  display: flex; align-items: center; justify-content: center;
  background: none; border: none; cursor: pointer;
  color: #9db6a9; border-radius: 8px;
  transition: color 0.15s, background 0.15s;
}
.field-action:hover:not(:disabled) { color: #16a34a; background: rgba(22,163,74,0.08); }
.field-action:disabled { opacity: 0.4; cursor: not-allowed; }
.field-action svg { width: 17px; height: 17px; }

.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: clamp(11px, 1.9vh, 13px) 24px;
  margin-top: 2px;
  font-size: 14.5px;
  font-weight: 700;
  font-family: inherit;
  color: #fff;
  background: linear-gradient(135deg, #16a34a 0%, #0f4c26 100%);
  border: none;
  border-radius: 13px;
  cursor: pointer;
  box-shadow: 0 6px 18px rgba(15,76,38,0.35), inset 0 1px 0 rgba(255,255,255,0.15);
  transition: all 0.2s ease;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 26px rgba(15,76,38,0.42), inset 0 1px 0 rgba(255,255,255,0.2);
}
.btn-primary:active:not(:disabled) { transform: translateY(0); }
.btn-primary:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }
.btn-arrow { width: 16px; height: 16px; transition: transform 0.2s; }
.btn-primary:hover:not(:disabled) .btn-arrow { transform: translateX(3px); }
.spin { width: 17px; height: 17px; animation: rot 0.75s linear infinite; }
@keyframes rot { to { transform: rotate(360deg); } }

.form-links {
  text-align: center;
  margin-top: clamp(12px, 2vh, 18px);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.form-links p { font-size: 12.5px; color: #3f5f4c; margin: 0; }
.form-links a {
  color: #16a34a;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.15s;
}
.form-links a:hover { color: #0f4c26; }
.link-sm { font-size: 12px; color: #4b7a5a; font-weight: 600; }

.form-copy {
  text-align: center;
  font-size: 10.5px;
  color: #6b8b78;
  margin: clamp(14px, 2vh, 20px) 0 0;
  letter-spacing: 0.2px;
}

/* ════════════════════════════════════════
   TABLET / DESKTOP ≥ 900px — split layout
   ════════════════════════════════════════ */
@media (min-width: 900px) {
  .auth-shell {
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: clamp(30px, 5vw, 80px);
  }
  .brand-panel { display: flex; }
  .form-card-logo { display: none; } /* ya se muestra en el panel izquierdo */
}

/* ════════════════════════════════════════
   MÓVIL < 900px
   ════════════════════════════════════════ */
@media (max-width: 899px) {
  .field-shell input { font-size: 16px; } /* evita zoom auto en iOS */
}

@media (max-width: 380px) {
  .form-card { padding: 18px 16px; border-radius: 20px; }
}

@media (prefers-reduced-motion: reduce) {
  .mesh-blob, .brand-badge-dot { animation: none; }
}
</style>
