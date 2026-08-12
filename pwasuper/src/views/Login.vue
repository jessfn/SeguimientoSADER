<!--
  Raíz única obligatoria: App.vue envuelve el <router-view> en
  <transition mode="out-in">, y <Transition> de Vue 3 no puede animar un
  componente con varios nodos raíz — al navegar renderizaría en blanco.
-->
<template>
  <div class="auth-page">
    <AuthLayout>
    <div class="au-card-head">
      <h1>Bienvenido de vuelta</h1>
      <p>Ingresa tus credenciales para continuar</p>
    </div>

    <Transition name="au-fade">
      <div v-if="errorMessage" class="au-alert" role="alert">
        <AuthIcon :name="offline ? 'wifi-off' : 'alert'" />
        <span>{{ errorMessage }}</span>
      </div>
    </Transition>

    <form class="au-form" novalidate @submit.prevent="login">
      <div class="au-field">
        <label for="email">Correo electrónico</label>
        <div class="au-input" :class="{ 'is-error': shake }">
          <span class="au-ico"><AuthIcon name="mail" /></span>
          <input
            id="email"
            v-model.trim="email"
            type="email"
            inputmode="email"
            autocomplete="email"
            placeholder="nombre@ejemplo.com"
            :disabled="loading"
            required
          />
        </div>
      </div>

      <div class="au-field">
        <label for="password">Contraseña</label>
        <div class="au-input au-has-btn" :class="{ 'is-error': shake }">
          <span class="au-ico"><AuthIcon name="lock" /></span>
          <input
            id="password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            autocomplete="current-password"
            placeholder="Tu contraseña"
            :disabled="loading"
            required
          />
          <button
            type="button"
            class="au-input-btn"
            :disabled="loading"
            :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
            tabindex="-1"
            @click="showPassword = !showPassword"
          >
            <AuthIcon :name="showPassword ? 'eye-off' : 'eye'" />
          </button>
        </div>
      </div>

      <button type="submit" class="au-btn au-btn-primary submit" :disabled="loading">
        <span v-if="loading" class="au-spin"></span>
        <span>{{ loading ? 'Verificando…' : 'Iniciar sesión' }}</span>
        <AuthIcon v-if="!loading" name="arrow-right" class="au-btn-arrow" />
      </button>
    </form>

    <div class="au-links">
      <p>¿No tienes cuenta? <router-link to="/register">Crear cuenta</router-link></p>
      <router-link to="/forgot-password" class="link-sm">¿Olvidaste tu contraseña?</router-link>
    </div>

    <p class="au-copy card-copy">© 2026 SADER · Todos los derechos reservados</p>
    </AuthLayout>

    <SupportBubbleLogin />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { API_URL } from '../utils/network.js';
import AuthLayout from '../components/auth/AuthLayout.vue';
import AuthIcon from '../components/auth/AuthIcon.vue';
import SupportBubbleLogin from '../components/SupportBubbleLogin.vue';
import { enviarInfoDispositivo } from '../services/dispositivoTrackingService.js';

const MAX_RETRIES = 2;

const email = ref('');
const password = ref('');
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const offline = ref(false);
const shake = ref(false);

function fail(msg, isOffline = false) {
  errorMessage.value = msg;
  offline.value = isOffline;
  shake.value = true;
  setTimeout(() => { shake.value = false; }, 600);
}

async function login() {
  if (!email.value || !password.value) {
    fail('Por favor completa todos los campos');
    return;
  }

  loading.value = true;
  errorMessage.value = '';
  offline.value = false;

  for (let intento = 0; intento <= MAX_RETRIES; intento++) {
    if (intento > 0) {
      errorMessage.value = `Reintentando conexión (${intento}/${MAX_RETRIES})…`;
      await new Promise(r => setTimeout(r, 3000 * intento));
    }

    try {
      const { data } = await axios.post(
        `${API_URL}/login`,
        { correo: email.value, contrasena: password.value },
        { timeout: 30000, headers: { 'Content-Type': 'application/json' } }
      );

      localStorage.setItem('user', JSON.stringify(data));
      enviarInfoDispositivo(data.id).catch(() => {});
      sessionStorage.setItem('justLoggedIn', 'true');
      window.location.href = '/';
      return;
    } catch (err) {
      // Un error con respuesta del servidor es definitivo: no tiene sentido reintentar.
      if (err.response) {
        const s = err.response.status;
        const detail = err.response.data?.detail;
        loading.value = false;
        fail(
          s === 401 ? 'Credenciales incorrectas. Verifica tu correo y contraseña.'
          : s === 403 ? (detail || 'Cuenta desactivada. Contacta al administrador.')
          : s === 500 ? 'Error del servidor. Inténtalo en unos minutos.'
          : (detail || 'No se pudo iniciar sesión.')
        );
        return;
      }
    }
  }

  loading.value = false;
  const sinRed = !navigator.onLine;
  fail(
    sinRed ? 'Sin conexión a internet. Revisa tu red e inténtalo de nuevo.'
           : 'No se pudo conectar con el servidor. Intenta de nuevo.',
    sinRed
  );
}
</script>

<style scoped>
.submit { margin-top: 4px; }
.link-sm { font-size: 12px; color: var(--au-ink-soft); font-weight: 600; }

/* En desktop el copyright vive bajo la tarjeta (lo pone AuthLayout) */
@media (min-width: 1000px) { .card-copy { display: none; } }
</style>
