<template>
  <AuthLayout badge="Panel administrativo"
              desc="Consulta el seguimiento en campo, la geolocalización de tu equipo y genera reportes."
              :features="['Seguimiento en tiempo real', 'Geolocalización precisa', 'Reportes y estadísticas']">
    <div class="au-card-head">
      <h1>Panel de Administrador</h1>
      <p>Ingresa tus credenciales para acceder</p>
    </div>

    <Transition name="au-fade">
      <div v-if="error" class="au-alert" role="alert">
        <AuthIcon name="alert" />
        <span>{{ error }}</span>
      </div>
    </Transition>

    <form class="au-form" novalidate @submit.prevent="login">
      <div class="au-field">
        <label for="username">Usuario</label>
        <div class="au-input" :class="{ 'is-error': shake }">
          <span class="au-ico"><AuthIcon name="user" /></span>
          <input
            id="username"
            v-model.trim="credentials.username"
            type="text"
            autocomplete="username"
            placeholder="Nombre de usuario"
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
            v-model="credentials.password"
            :type="showPassword ? 'text' : 'password'"
            autocomplete="current-password"
            placeholder="Tu contraseña"
            :disabled="loading"
            required
          />
          <button
            type="button"
            class="au-input-btn"
            tabindex="-1"
            :disabled="loading"
            :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
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

    <p class="au-copy card-copy">© 2026 SADER · Panel de Administración</p>
  </AuthLayout>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService'
import AuthLayout from '../components/auth/AuthLayout.vue'
import AuthIcon from '../components/auth/AuthIcon.vue'

const router = useRouter()

const credentials = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)
const shake = ref(false)

function fail(msg) {
  error.value = msg
  shake.value = true
  setTimeout(() => { shake.value = false }, 600)
}

const login = async () => {
  if (!credentials.username || !credentials.password) {
    fail('Por favor completa todos los campos')
    return
  }

  loading.value = true
  error.value = ''

  try {
    const result = await authService.login(credentials)
    if (result.success) {
      router.push('/visor-map')
    } else {
      fail('Credenciales incorrectas')
    }
  } catch (err) {
    fail(err.response?.data?.detail || 'No se pudo conectar con el servidor')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.submit { margin-top: 4px; }

/* En desktop el copyright lo pone AuthLayout bajo la tarjeta */
@media (min-width: 1000px) { .card-copy { display: none; } }
</style>
