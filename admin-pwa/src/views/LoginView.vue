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
      <aside class="brand-panel">
        <div class="brand-panel-inner">
          <SaderLogo :size="72" layout="stack" :subtitle="false" dark class="brand-panel-logo" />

          <h1 class="brand-title">Panel de Administrador</h1>
          <p class="brand-subtitle">Subsecretaría de Inclusión Productiva<br>y Desarrollo Rural</p>

          <div class="brand-divider"></div>

          <p class="brand-tagline">App de Seguimiento</p>

          <ul class="brand-stats">
            <li>
              <span class="stat-ico">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                </svg>
              </span>
              <span>Seguimiento en tiempo real</span>
            </li>
            <li>
              <span class="stat-ico">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
              </span>
              <span>Geolocalización precisa</span>
            </li>
            <li>
              <span class="stat-ico">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="20" x2="18" y2="10"/>
                  <line x1="12" y1="20" x2="12" y2="4"/>
                  <line x1="6" y1="20" x2="6" y2="14"/>
                </svg>
              </span>
              <span>Reportes y estadísticas</span>
            </li>
          </ul>
        </div>
      </aside>

      <main class="form-panel">
        <div class="form-card">
          <div class="form-header">
            <h2 class="form-title">Iniciar sesión</h2>
            <p class="form-desc">Ingresa tus credenciales para acceder al panel</p>
          </div>

          <form @submit.prevent="login" class="login-form" novalidate>
            <div class="form-group">
              <label for="username" class="form-label">Usuario</label>
              <div class="input-wrap">
                <span class="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                </span>
                <input
                  v-model="credentials.username"
                  type="text"
                  id="username"
                  placeholder="Nombre de usuario"
                  autocomplete="username"
                  required
                  :disabled="loading"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="password" class="form-label">Contraseña</label>
              <div class="input-wrap">
                <span class="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                </span>
                <input
                  v-model="credentials.password"
                  :type="showPassword ? 'text' : 'password'"
                  id="password"
                  placeholder="••••••••"
                  autocomplete="current-password"
                  required
                  :disabled="loading"
                />
                <button
                  type="button"
                  class="eye-btn"
                  @click="showPassword = !showPassword"
                  :disabled="loading"
                  :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                >
                  <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading">
              <span v-if="!loading" class="btn-inner">
                Iniciar sesión
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon">
                  <line x1="5" y1="12" x2="19" y2="12"/>
                  <polyline points="12 5 19 12 12 19"/>
                </svg>
              </span>
              <span v-else class="btn-inner">
                <span class="spinner"></span>
                Verificando
              </span>
            </button>

            <transition name="err">
              <div v-if="error" class="error-box" role="alert">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="err-icon">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12"/>
                  <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                {{ error }}
              </div>
            </transition>
          </form>

          <div class="footer-brand"><SaderLogo :size="26" layout="row" :subtitle="false" dark /></div>
          <p class="footer-copy">© 2026 SADER · Panel de Administración</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService'
import SaderLogo from '../components/SaderLogo.vue'

const router = useRouter()

const credentials = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

const login = async () => {
  if (!credentials.username || !credentials.password) {
    error.value = 'Por favor completa todos los campos'
    return
  }
  loading.value = true
  error.value = ''
  try {
    const result = await authService.login(credentials)
    if (result.success) {
      router.push('/visor-map')
    } else {
      error.value = 'Credenciales incorrectas'
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'No se pudo conectar con el servidor'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; }

.auth-screen {
  position: relative;
  min-height: 100vh;
  width: 100%;
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
  background: linear-gradient(160deg, #041f10 0%, #0a2e1a 30%, #0f3d22 60%, #12472a 100%);
  overflow: hidden;
}
.mesh-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(75px);
  opacity: 0.55;
  will-change: transform;
}
.blob-1 {
  width: 50vw; height: 50vw; max-width: 680px; max-height: 680px;
  top: -16%; right: -12%;
  background: radial-gradient(circle, rgba(74,222,128,0.30) 0%, rgba(74,222,128,0) 70%);
  animation: driftA 20s ease-in-out infinite;
}
.blob-2 {
  width: 42vw; height: 42vw; max-width: 560px; max-height: 560px;
  bottom: -16%; left: -10%;
  background: radial-gradient(circle, rgba(21,128,61,0.42) 0%, rgba(21,128,61,0) 70%);
  animation: driftB 24s ease-in-out infinite;
}
.blob-3 {
  width: 28vw; height: 28vw; max-width: 400px; max-height: 400px;
  top: 20%; left: 20%;
  background: radial-gradient(circle, rgba(245,196,81,0.20) 0%, rgba(245,196,81,0) 70%);
  animation: driftA 28s ease-in-out infinite reverse;
}
.blob-4 {
  width: 22vw; height: 22vw; max-width: 320px; max-height: 320px;
  bottom: 22%; right: 18%;
  background: radial-gradient(circle, rgba(187,247,208,0.22) 0%, rgba(187,247,208,0) 70%);
  animation: driftB 16s ease-in-out infinite reverse;
}
@keyframes driftA {
  0%, 100% { transform: translate(0,0) scale(1); }
  50% { transform: translate(6%, 8%) scale(1.1); }
}
@keyframes driftB {
  0%, 100% { transform: translate(0,0) scale(1); }
  50% { transform: translate(-6%, -8%) scale(1.08); }
}

.auth-shell {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* ── Panel de marca ── */
.brand-panel { display: none; }
.brand-panel-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 380px;
  color: #fff;
}
.brand-panel-logo { margin-bottom: 20px; }

.brand-title {
  font-size: clamp(26px, 3.4vw, 38px);
  font-weight: 800;
  letter-spacing: -1px;
  margin: 0 0 10px;
  background: linear-gradient(120deg, #bbf7d0 0%, #4ade80 50%, #f5c451 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.brand-subtitle {
  font-size: 13px;
  color: rgba(255,255,255,0.65);
  line-height: 1.6;
  margin: 0 0 20px;
}
.brand-divider {
  width: 44px; height: 2.5px;
  background: linear-gradient(90deg, #4ade80, #f5c451);
  border-radius: 99px;
  margin: 0 0 20px;
}
.brand-tagline {
  font-size: 14.5px;
  font-weight: 600;
  color: rgba(255,255,255,0.9);
  margin: 0 0 30px;
}

.brand-stats {
  list-style: none;
  margin: 0; padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  max-width: 270px;
}
.brand-stats li {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 12px;
  padding: 10px 14px;
  text-align: left;
  font-size: 12.5px;
  font-weight: 500;
  color: rgba(255,255,255,0.9);
  transition: background 0.2s, transform 0.2s;
}
.brand-stats li:hover { background: rgba(255,255,255,0.13); transform: translateX(2px); }
.stat-ico {
  display: flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; flex-shrink: 0;
  background: rgba(74,222,128,0.16);
  border-radius: 8px;
  color: #86efac;
}
.stat-ico svg { width: 55%; height: 55%; }

/* ── Tarjeta del formulario ── */
.form-panel {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 24px 18px;
}
.form-card {
  position: relative;
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  background: linear-gradient(155deg, #1b7a3d 0%, #166534 55%, #124d29 100%);
  border-radius: 24px;
  padding: clamp(24px, 4vh, 40px) clamp(20px, 3.5vw, 36px);
  border: 1px solid rgba(255,255,255,0.12);
  box-shadow:
    0 1px 0 0 rgba(255,255,255,0.16) inset,
    0 30px 70px rgba(0,0,0,0.5),
    0 10px 28px rgba(0,0,0,0.35);
  animation: slideUp 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.form-header { margin-bottom: 24px; }
.form-title {
  font-size: clamp(19px, 3vh, 26px);
  font-weight: 700;
  color: #fff;
  margin: 0 0 6px;
  letter-spacing: -0.6px;
}
.form-desc {
  font-size: 13.5px;
  font-weight: 400;
  color: #bcdec9;
  margin: 0;
}

.login-form { display: flex; flex-direction: column; gap: 18px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-label {
  font-size: 12.5px;
  font-weight: 600;
  color: #d7ecdf;
}

.input-wrap { position: relative; display: flex; align-items: center; }
.input-icon {
  position: absolute;
  left: 14px;
  color: #7fae8e;
  display: flex;
  align-items: center;
  pointer-events: none;
}
.input-icon svg { width: 17px; height: 17px; }

.input-wrap input {
  width: 100%;
  padding: 13px 44px;
  font-size: 14.5px;
  font-family: inherit;
  color: #0b1120;
  background: rgba(255,255,255,0.92);
  border: 1.5px solid rgba(255,255,255,0.15);
  border-radius: 13px;
  outline: none;
  transition: border-color 0.25s, box-shadow 0.25s, background 0.25s;
}
.input-wrap input::placeholder { color: #9aa8a1; }
.input-wrap input:focus {
  background: #fff;
  border-color: #4ade80;
  box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.22);
}
.input-wrap input:disabled { opacity: 0.55; cursor: not-allowed; }

.eye-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #7fae8e;
  display: flex;
  align-items: center;
  padding: 4px;
  border-radius: 7px;
  transition: color 0.2s, background 0.2s;
}
.eye-btn:hover:not(:disabled) { color: #16a34a; background: rgba(22,163,74,0.1); }
.eye-btn:disabled { cursor: not-allowed; opacity: 0.5; }
.eye-btn svg { width: 18px; height: 18px; }

.submit-btn {
  width: 100%;
  padding: 14px 24px;
  margin-top: 4px;
  font-size: 15px;
  font-weight: 700;
  font-family: inherit;
  color: #14532d;
  background: #ffffff;
  border: none;
  border-radius: 13px;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1), 0 10px 24px rgba(0,0,0,0.22);
}
.submit-btn:hover:not(:disabled) {
  background: #f0fdf4;
  transform: translateY(-1px);
  box-shadow: 0 1px 2px rgba(0,0,0,0.12), 0 14px 30px rgba(0,0,0,0.28);
}
.submit-btn:active:not(:disabled) { transform: translateY(0) scale(0.99); }
.submit-btn:disabled {
  background: rgba(255,255,255,0.35);
  color: rgba(20,83,45,0.5);
  box-shadow: none;
  cursor: not-allowed;
}

.btn-inner { display: flex; align-items: center; justify-content: center; gap: 8px; }
.btn-icon { width: 17px; height: 17px; transition: transform 0.2s; }
.submit-btn:hover:not(:disabled) .btn-icon { transform: translateX(3px); }

.spinner {
  width: 15px; height: 15px;
  border: 2px solid rgba(255,255,255,0.35);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.error-box {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 11px 14px;
  background: rgba(254,242,242,0.95);
  border: 1px solid #fecaca;
  border-radius: 11px;
  color: #dc2626;
  font-size: 13px;
  font-weight: 500;
}
.err-icon { width: 16px; height: 16px; flex-shrink: 0; }
.err-enter-active, .err-leave-active { transition: all 0.25s ease; }
.err-enter-from, .err-leave-to { opacity: 0; transform: translateY(-6px); }

.footer-brand {
  display: flex;
  justify-content: center;
  margin: 22px 0 6px;
}
.footer-copy {
  text-align: center;
  font-size: 11px;
  color: #8fbb9e;
  margin: 0;
}

/* ════════════════════════════════════════
   DESKTOP ≥ 1024px — split layout
   ════════════════════════════════════════ */
@media (min-width: 1024px) {
  .auth-shell {
    flex-direction: row;
    gap: clamp(50px, 7vw, 120px);
    padding: 32px;
  }
  .brand-panel { display: flex; }
  .form-panel { width: auto; padding: 0; }
}

@media (max-width: 1023px) {
  .form-panel { min-height: 100vh; align-items: center; }
  .input-wrap input { font-size: 16px; }
}

@media (max-width: 380px) {
  .form-card { padding: 22px 16px; }
}
</style>
