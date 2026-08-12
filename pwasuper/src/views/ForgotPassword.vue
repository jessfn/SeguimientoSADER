<template>
  <AuthLayout badge="Recuperación de acceso"
              desc="Verifica tu correo registrado y define una nueva contraseña para volver a entrar."
              :features="['Verificación en dos pasos', 'Tu cuenta no se bloquea', 'Acceso inmediato al terminar']">
    <div class="head">
      <router-link to="/login" class="back" aria-label="Volver a iniciar sesión">
        <AuthIcon name="arrow-left" />
      </router-link>
      <div class="head-text">
        <h1>Recuperar contraseña</h1>
        <p>Paso {{ emailVerified ? 2 : 1 }} de 2 · {{ emailVerified ? 'Nueva contraseña' : 'Verificar correo' }}</p>
      </div>
    </div>

    <ol class="steps">
      <li :class="{ done: emailVerified, now: !emailVerified }">
        <span class="dot">
          <AuthIcon v-if="emailVerified" name="check-plain" />
          <template v-else>1</template>
        </span>
        <em>Verificar correo</em>
      </li>
      <li :class="{ now: emailVerified }">
        <span class="dot">2</span>
        <em>Nueva contraseña</em>
      </li>
    </ol>

    <Transition name="au-fade">
      <div v-if="errorMessage" class="au-alert" role="alert">
        <AuthIcon :name="offline ? 'wifi-off' : 'alert'" />
        <span>{{ errorMessage }}</span>
      </div>
    </Transition>

    <!-- ══════════ PASO 1 · Verificar correo ══════════ -->
    <form v-if="!emailVerified" class="au-form" novalidate @submit.prevent="verifyEmail">
      <div class="au-field">
        <label for="email">Tu correo registrado</label>
        <div class="au-input" :class="{ 'is-error': shake }">
          <span class="au-ico"><AuthIcon name="mail" /></span>
          <input id="email" v-model.trim="email" type="email" inputmode="email"
                 autocomplete="email" placeholder="nombre@ejemplo.com" :disabled="verifying" />
        </div>
        <span class="au-hint">Comprobaremos que exista una cuenta con este correo</span>
      </div>

      <button type="submit" class="au-btn au-btn-primary" :disabled="verifying || !emailValido">
        <span v-if="verifying" class="au-spin"></span>
        <span>{{ verifying ? 'Verificando…' : 'Verificar correo' }}</span>
        <AuthIcon v-if="!verifying" name="arrow-right" class="au-btn-arrow" />
      </button>
    </form>

    <!-- ══════════ PASO 2 · Nueva contraseña ══════════ -->
    <form v-else class="au-form" novalidate @submit.prevent="resetPassword">
      <div class="found">
        <span class="found-ico"><AuthIcon name="check" /></span>
        <span class="found-info">
          <b>{{ email }}</b>
          <em>{{ foundUser?.nombre_completo }}</em>
        </span>
        <button type="button" class="found-change" :disabled="loading" @click="resetFlow">Cambiar</button>
      </div>

      <div class="au-field">
        <label for="pass">Nueva contraseña</label>
        <div class="au-input au-has-btn">
          <span class="au-ico"><AuthIcon name="lock" /></span>
          <input id="pass" v-model="newPassword" :type="showPass ? 'text' : 'password'"
                 autocomplete="new-password" placeholder="Mínimo 6 caracteres" :disabled="loading" />
          <button type="button" class="au-input-btn" tabindex="-1" :disabled="loading"
                  :aria-label="showPass ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                  @click="showPass = !showPass">
            <AuthIcon :name="showPass ? 'eye-off' : 'eye'" />
          </button>
        </div>
        <div v-if="newPassword" class="meter">
          <span :class="['meter-bar', `lv-${fuerza.nivel}`]"><i :style="{ width: fuerza.pct + '%' }"></i></span>
          <em :class="`lv-${fuerza.nivel}`">{{ fuerza.texto }}</em>
        </div>
      </div>

      <div class="au-field">
        <label for="pass2">Confirmar nueva contraseña</label>
        <div class="au-input au-has-btn"
             :class="{ 'is-error': confirmPassword && !passwordsMatch, 'is-ok': confirmPassword && passwordsMatch }">
          <span class="au-ico"><AuthIcon name="check" /></span>
          <input id="pass2" v-model="confirmPassword" :type="showPass2 ? 'text' : 'password'"
                 autocomplete="new-password" placeholder="Repite tu contraseña" :disabled="loading" />
          <button type="button" class="au-input-btn" tabindex="-1" :disabled="loading"
                  :aria-label="showPass2 ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                  @click="showPass2 = !showPass2">
            <AuthIcon :name="showPass2 ? 'eye-off' : 'eye'" />
          </button>
        </div>
        <span v-if="confirmPassword && !passwordsMatch" class="au-hint is-error">
          <AuthIcon name="x" />Las contraseñas no coinciden
        </span>
        <span v-else-if="confirmPassword && passwordsMatch" class="au-hint is-ok">
          <AuthIcon name="check" />Las contraseñas coinciden
        </span>
      </div>

      <button type="submit" class="au-btn au-btn-primary" :disabled="loading || !puedeGuardar">
        <span v-if="loading" class="au-spin"></span>
        <span>{{ loading ? 'Guardando…' : 'Cambiar contraseña' }}</span>
        <AuthIcon v-if="!loading" name="arrow-right" class="au-btn-arrow" />
      </button>
    </form>

    <div class="au-links">
      <p>¿Recordaste tu contraseña? <router-link to="/login">Iniciar sesión</router-link></p>
    </div>
  </AuthLayout>

  <!-- ── Modal de éxito ── -->
  <Teleport to="body">
    <Transition name="pop">
      <div v-if="showSuccessModal" class="ok-back" @click.self="goToLogin">
        <div class="ok-card" role="dialog" aria-modal="true">
          <span class="ok-ring"><AuthIcon name="check-plain" /></span>
          <h2>Contraseña actualizada</h2>
          <p>Ya puedes entrar con tu nueva contraseña.</p>
          <div class="ok-bar"><i></i></div>
          <p class="ok-note">Redirigiendo al inicio de sesión…</p>
          <button class="au-btn au-btn-primary" @click="goToLogin">Continuar</button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { getBestApiUrl, checkInternetConnection, getOfflineMessage } from '../utils/network.js';
import AuthLayout from '../components/auth/AuthLayout.vue';
import AuthIcon from '../components/auth/AuthIcon.vue';

const router = useRouter();

const email = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const showPass = ref(false);
const showPass2 = ref(false);
const loading = ref(false);
const verifying = ref(false);
const errorMessage = ref('');
const offline = ref(false);
const shake = ref(false);
const emailVerified = ref(false);
const foundUser = ref(null);
const showSuccessModal = ref(false);

const emailValido = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim()));
const passwordsMatch = computed(() => newPassword.value === confirmPassword.value);
const puedeGuardar = computed(() =>
  newPassword.value.length >= 6 && confirmPassword.value.length > 0 && passwordsMatch.value);

const fuerza = computed(() => {
  const p = newPassword.value;
  let n = 0;
  if (p.length >= 6) n++;
  if (p.length >= 10) n++;
  if (/[A-Z]/.test(p) && /[a-z]/.test(p)) n++;
  if (/\d/.test(p) && /[^A-Za-z0-9]/.test(p)) n++;
  if (p.length < 6) return { nivel: 0, pct: 20, texto: 'Muy corta (mínimo 6)' };
  return [
    { nivel: 1, pct: 35, texto: 'Débil' },
    { nivel: 2, pct: 60, texto: 'Aceptable' },
    { nivel: 3, pct: 80, texto: 'Buena' },
    { nivel: 4, pct: 100, texto: 'Excelente' },
  ][n - 1];
});

function fail(msg, isOffline = false) {
  errorMessage.value = msg;
  offline.value = isOffline;
  shake.value = true;
  setTimeout(() => { shake.value = false; }, 600);
}

function resetFlow() {
  emailVerified.value = false;
  foundUser.value = null;
  errorMessage.value = '';
  newPassword.value = '';
  confirmPassword.value = '';
}

async function verifyEmail() {
  if (!emailValido.value) {
    fail('Ingresa un correo electrónico válido');
    return;
  }

  verifying.value = true;
  errorMessage.value = '';
  offline.value = false;

  if (!(await checkInternetConnection())) {
    verifying.value = false;
    fail(getOfflineMessage(), true);
    return;
  }

  try {
    const apiUrl = await getBestApiUrl();
    const { data } = await axios.get(`${apiUrl}/usuarios`, {
      timeout: 10000,
      headers: { 'Content-Type': 'application/json' },
    });

    const usuario = (data.usuarios || []).find(
      u => u.correo?.toLowerCase() === email.value.toLowerCase()
    );

    if (!usuario) {
      fail('No se encontró una cuenta registrada con ese correo electrónico');
      return;
    }

    foundUser.value = usuario;
    emailVerified.value = true;
  } catch (error) {
    console.error('Error al verificar correo:', error);
    if (error.code === 'ECONNABORTED') {
      fail('La conexión tardó demasiado. Verifica tu internet.');
    } else if (error.request) {
      fail('No se pudo conectar con el servidor.');
    } else {
      fail('Error al verificar el correo: ' + error.message);
    }
  } finally {
    verifying.value = false;
  }
}

async function resetPassword() {
  if (!foundUser.value) {
    fail('Primero debes verificar tu correo electrónico');
    return;
  }
  if (newPassword.value.length < 6) {
    fail('La nueva contraseña debe tener al menos 6 caracteres');
    return;
  }
  if (!passwordsMatch.value) {
    fail('Las contraseñas no coinciden');
    return;
  }

  loading.value = true;
  errorMessage.value = '';
  offline.value = false;

  if (!(await checkInternetConnection())) {
    loading.value = false;
    fail(getOfflineMessage(), true);
    return;
  }

  try {
    const apiUrl = await getBestApiUrl();
    const u = foundUser.value;

    await axios.put(
      `${apiUrl}/usuarios/${u.id}`,
      {
        correo: u.correo,
        nombre_completo: u.nombre_completo,
        cargo: u.cargo,
        supervisor: u.supervisor,
        contrasena: newPassword.value,
        curp: u.curp,
        telefono: u.telefono,
      },
      { timeout: 10000, headers: { 'Content-Type': 'application/json' } }
    );

    showSuccessModal.value = true;
    setTimeout(goToLogin, 3000);
  } catch (error) {
    console.error('Error al cambiar contraseña:', error);
    if (error.response) {
      const s = error.response.status;
      fail(
        s === 404 ? 'No se encontró la cuenta asociada a ese correo.'
        : s === 500 ? 'Error del servidor. Inténtalo en unos minutos.'
        : (error.response.data?.detail || 'No se pudo cambiar la contraseña.')
      );
    } else if (error.code === 'ECONNABORTED') {
      fail('La conexión tardó demasiado. Verifica tu internet.');
    } else if (error.request) {
      fail('No se pudo conectar con el servidor.');
    } else {
      fail('Error al cambiar la contraseña: ' + error.message);
    }
  } finally {
    loading.value = false;
  }
}

function goToLogin() {
  showSuccessModal.value = false;
  router.push('/login');
}
</script>

<style scoped>
/* ── Encabezado ── */
.head { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.back {
  display: flex; align-items: center; justify-content: center;
  width: 34px; height: 34px; flex-shrink: 0;
  border-radius: 50%;
  background: rgba(22, 163, 74, 0.09);
  color: var(--au-green-600);
  transition: background 0.15s, transform 0.15s;
}
.back:hover { background: rgba(22, 163, 74, 0.16); transform: translateX(-2px); }
.back :deep(svg) { width: 16px; height: 16px; }
.head-text h1 {
  margin: 0; font-size: clamp(18px, 2.5vh, 22px); font-weight: 800;
  letter-spacing: -0.5px; color: var(--au-ink);
}
.head-text p { margin: 2px 0 0; font-size: 12px; color: var(--au-ink-soft); }

/* ── Barra de pasos ── */
.steps { list-style: none; display: flex; margin: 0 0 18px; padding: 0; }
.steps li {
  flex: 1;
  display: flex; flex-direction: column; align-items: center; gap: 5px;
  position: relative; font-size: 10.5px;
}
.steps li::before {
  content: '';
  position: absolute; top: 12px; right: 50%;
  width: 100%; height: 2px;
  background: #e2ece6;
}
.steps li:first-child::before { display: none; }
.steps li.done::before, .steps li.now::before { background: var(--au-green-400); }
.steps .dot {
  position: relative; z-index: 1;
  display: flex; align-items: center; justify-content: center;
  width: 25px; height: 25px;
  border-radius: 50%;
  background: #eef4f0;
  color: var(--au-ink-faint);
  font-size: 11px; font-weight: 700;
  border: 2px solid #e2ece6;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}
.steps .dot :deep(svg) { width: 12px; height: 12px; }
.steps li.done .dot { background: var(--au-green-400); border-color: var(--au-green-400); color: #fff; }
.steps li.now .dot {
  background: var(--au-green-600); border-color: var(--au-green-600); color: #fff;
  box-shadow: 0 0 0 4px rgba(22, 163, 74, 0.14);
}
.steps em { font-style: normal; font-weight: 600; color: var(--au-ink-faint); }
.steps li.now em { color: var(--au-green-600); }
.steps li.done em { color: var(--au-ink-soft); }

/* ── Cuenta encontrada ── */
.found {
  display: flex; align-items: center; gap: 10px;
  padding: 11px;
  background: #f0fdf4;
  border: 1.5px solid var(--au-green-400);
  border-radius: var(--au-r-md);
}
.found-ico {
  display: flex; flex-shrink: 0;
  width: 22px; height: 22px;
  color: var(--au-green-500);
}
.found-ico :deep(svg) { width: 100%; height: 100%; }
.found-info { display: flex; flex-direction: column; min-width: 0; flex: 1; }
.found-info b {
  font-size: 13px; font-weight: 600; color: var(--au-ink);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.found-info em {
  font-style: normal; font-size: 10.5px; color: var(--au-ink-faint);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.found-change {
  flex-shrink: 0;
  padding: 6px 13px;
  background: none;
  border: 1px solid var(--au-green-400);
  border-radius: 99px;
  color: var(--au-green-600);
  font-size: 11.5px; font-weight: 600; font-family: inherit;
  cursor: pointer;
  transition: background 0.15s;
}
.found-change:hover:not(:disabled) { background: rgba(22, 163, 74, 0.1); }
.found-change:disabled { opacity: 0.5; cursor: not-allowed; }

/* ── Medidor de contraseña ── */
.meter { display: flex; align-items: center; gap: 9px; }
.meter-bar { flex: 1; height: 4px; border-radius: 99px; background: #e6eee9; overflow: hidden; }
.meter-bar i { display: block; height: 100%; border-radius: 99px; transition: width 0.3s ease, background 0.3s ease; }
.meter-bar.lv-0 i, .meter-bar.lv-1 i { background: #f43f5e; }
.meter-bar.lv-2 i { background: var(--au-gold); }
.meter-bar.lv-3 i { background: var(--au-green-400); }
.meter-bar.lv-4 i { background: var(--au-green-600); }
.meter em { font-style: normal; font-size: 10.5px; font-weight: 600; white-space: nowrap; }
.meter em.lv-0, .meter em.lv-1 { color: #e11d48; }
.meter em.lv-2 { color: var(--au-gold-deep); }
.meter em.lv-3, .meter em.lv-4 { color: var(--au-green-600); }

/* ── Modal de éxito ── */
.ok-back {
  position: fixed; inset: 0; z-index: 1000;
  display: flex; align-items: center; justify-content: center;
  padding: 20px;
  background: rgba(4, 28, 14, 0.62);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}
.ok-card {
  width: 100%; max-width: 340px;
  padding: 30px 26px;
  text-align: center;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
  font-family: var(--au-font);
}
.ok-ring {
  display: flex; align-items: center; justify-content: center;
  width: 62px; height: 62px; margin: 0 auto 16px;
  border-radius: 50%;
  background: #f0fdf4;
  border: 2.5px solid var(--au-green-400);
  color: var(--au-green-500);
  animation: ok-pop 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.ok-ring :deep(svg) { width: 28px; height: 28px; }
@keyframes ok-pop { from { transform: scale(0.6); opacity: 0; } to { transform: scale(1); opacity: 1; } }
.ok-card h2 { margin: 0 0 6px; font-size: 19px; font-weight: 800; color: var(--au-ink); }
.ok-card > p { margin: 0 0 18px; font-size: 13px; color: var(--au-ink-soft); }
.ok-bar { height: 4px; border-radius: 99px; background: #eef4f0; overflow: hidden; }
.ok-bar i {
  display: block; height: 100%;
  background: linear-gradient(90deg, var(--au-green-400), var(--au-green-600));
  animation: ok-fill 3s linear forwards;
}
@keyframes ok-fill { from { width: 0; } to { width: 100%; } }
.ok-note { margin: 8px 0 18px; font-size: 11.5px; color: var(--au-green-600); font-weight: 600; }

.pop-enter-active { transition: opacity 0.25s; }
.pop-leave-active { transition: opacity 0.2s; }
.pop-enter-from, .pop-leave-to { opacity: 0; }
</style>
