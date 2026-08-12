<template>
  <AuthLayout wide max-width="520px" badge="Registro de nuevo usuario"
              desc="Crea tu cuenta para registrar actividades, asistencias y reportes desde campo."
              :features="['Alta en minutos', 'Tus datos viajan cifrados', 'Acceso inmediato tras el registro']">
    <!-- ── Encabezado con progreso ── -->
    <div class="head">
      <router-link to="/login" class="back" aria-label="Volver a iniciar sesión">
        <AuthIcon name="arrow-left" />
      </router-link>
      <div class="head-text">
        <h1>Crear cuenta</h1>
        <p>Paso {{ step }} de {{ STEPS.length }} · {{ STEPS[step - 1].label }}</p>
      </div>
    </div>

    <ol class="steps" :aria-label="`Paso ${step} de ${STEPS.length}`">
      <li v-for="(s, i) in STEPS" :key="s.label"
          :class="{ done: step > i + 1, now: step === i + 1 }">
        <span class="dot">
          <AuthIcon v-if="step > i + 1" name="check-plain" />
          <template v-else>{{ i + 1 }}</template>
        </span>
        <em>{{ s.short }}</em>
      </li>
    </ol>

    <Transition name="au-fade">
      <div v-if="message.text" class="au-alert" role="alert">
        <AuthIcon :name="isOnline ? 'alert' : 'wifi-off'" />
        <span>{{ message.text }}</span>
      </div>
    </Transition>

    <form class="au-form" novalidate @submit.prevent="onSubmit">
      <!-- ══════════ PASO 1 · Datos personales ══════════ -->
      <template v-if="step === 1">
        <div class="au-field">
          <label for="nombre">Nombre(s) <span class="au-req">*</span></label>
          <div class="au-input">
            <span class="au-ico"><AuthIcon name="user" /></span>
            <input id="nombre" v-model="form.nombre" type="text" autocomplete="given-name"
                   placeholder="NOMBRE(S)" @input="form.nombre = up(form.nombre)" />
          </div>
        </div>

        <div class="au-row">
          <div class="au-field">
            <label for="ap1">Apellido paterno <span class="au-req">*</span></label>
            <div class="au-input">
              <span class="au-ico"><AuthIcon name="user" /></span>
              <input id="ap1" v-model="form.primerApellido" type="text" autocomplete="family-name"
                     placeholder="PATERNO" @input="form.primerApellido = up(form.primerApellido)" />
            </div>
          </div>
          <div class="au-field">
            <label for="ap2">Apellido materno <span class="au-req">*</span></label>
            <div class="au-input">
              <span class="au-ico"><AuthIcon name="user" /></span>
              <input id="ap2" v-model="form.segundoApellido" type="text"
                     placeholder="MATERNO" @input="form.segundoApellido = up(form.segundoApellido)" />
            </div>
          </div>
        </div>

        <div class="au-field">
          <label for="curp">CURP <span class="au-req">*</span></label>
          <div class="au-input" :class="{ 'is-error': curpError, 'is-ok': curpValida }">
            <span class="au-ico"><AuthIcon name="id" /></span>
            <input id="curp" v-model="form.curp" type="text" maxlength="18" spellcheck="false"
                   placeholder="18 CARACTERES" class="mono" @input="formatCurp" />
            <span v-if="form.curp" class="au-count">{{ form.curp.length }}/18</span>
          </div>
          <span v-if="curpError" class="au-hint is-error"><AuthIcon name="x" />{{ curpError }}</span>
          <span v-else-if="curpValida" class="au-hint is-ok"><AuthIcon name="check" />CURP con formato válido</span>
          <span v-else class="au-hint">Clave Única de Registro de Población</span>
        </div>
      </template>

      <!-- ══════════ PASO 2 · Información laboral ══════════ -->
      <template v-else-if="step === 2">
        <div class="au-field">
          <label for="cargo">Puesto de trabajo <span class="au-req">*</span></label>
          <div class="au-input">
            <span class="au-ico"><AuthIcon name="briefcase" /></span>
            <select id="cargo" v-model="form.cargo">
              <option value="" disabled>Selecciona tu puesto</option>
              <option v-for="c in CARGOS" :key="c" :value="c">{{ c }}</option>
            </select>
            <svg class="au-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </div>
        </div>

        <div v-if="form.cargo === 'OTRO'" class="au-field">
          <label for="cargoOtro">Especifica tu puesto <span class="au-req">*</span></label>
          <div class="au-input">
            <span class="au-ico"><AuthIcon name="edit" /></span>
            <input id="cargoOtro" v-model="form.cargoOtro" type="text"
                   placeholder="NOMBRE DEL PUESTO" @input="form.cargoOtro = plain(form.cargoOtro)" />
          </div>
        </div>

        <div class="au-field">
          <label for="territorio">Territorio <span class="au-req">*</span></label>
          <div class="au-input">
            <span class="au-ico"><AuthIcon name="pin" /></span>
            <select id="territorio" v-model="form.territorio">
              <option value="" disabled>Selecciona tu territorio</option>
              <option v-for="t in TERRITORIOS" :key="t" :value="t">{{ t }}</option>
            </select>
            <svg class="au-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </div>
          <span class="au-hint">Tu área de trabajo asignada</span>
        </div>

        <!-- Técnicos: buscador de facilitador -->
        <div v-if="esTecnico" class="au-field fac">
          <label>Tu facilitador <span class="au-tag">Obligatorio</span></label>

          <div v-if="facilitadorSeleccionado" class="fac-picked">
            <span class="fac-avatar">{{ facilitadorSeleccionado.nombre_completo.charAt(0) }}</span>
            <span class="fac-info">
              <b>{{ facilitadorSeleccionado.nombre_completo }}</b>
              <em>
                {{ facilitadorSeleccionado.curp || '' }}
                <template v-if="facilitadorSeleccionado.territorio"> · {{ facilitadorSeleccionado.territorio }}</template>
              </em>
            </span>
            <button type="button" class="fac-clear" aria-label="Cambiar facilitador" @click="limpiarFacilitador">
              <AuthIcon name="x-plain" />
            </button>
          </div>

          <template v-else>
            <div class="au-input au-has-btn">
              <span class="au-ico"><AuthIcon name="search" /></span>
              <input v-model="facilitadorQuery" type="text" autocomplete="off"
                     placeholder="Busca por nombre o CURP…"
                     @input="buscarFacilitadoresRT" @focus="mostrarResultados = true" />
              <span v-if="buscandoFacilitador" class="au-input-btn"><i class="au-spin-sm"></i></span>
            </div>

            <div v-if="mostrarResultados && facilitadorQuery.trim().length >= 2" class="fac-results">
              <p v-if="buscandoFacilitador" class="fac-state">
                <i class="au-spin-sm"></i> Buscando facilitadores…
              </p>
              <p v-else-if="!facilitadoresEncontrados.length" class="fac-state">
                Sin resultados para “{{ facilitadorQuery.trim() }}”
              </p>
              <ul v-else>
                <li v-for="f in facilitadoresEncontrados" :key="f.admin_id">
                  <button type="button" @click="seleccionarFacilitador(f)">
                    <span class="fac-avatar sm">{{ f.nombre_completo.charAt(0) }}</span>
                    <span class="fac-info">
                      <b>{{ f.nombre_completo }}</b>
                      <em>
                        {{ f.curp || '' }}
                        <template v-if="f.territorio"> · {{ f.territorio }}</template>
                      </em>
                    </span>
                  </button>
                </li>
              </ul>
            </div>
            <span class="au-hint">Escribe al menos 2 caracteres para buscar</span>
          </template>
        </div>

        <!-- No técnicos: supervisor manual -->
        <div v-else class="au-field">
          <label for="supervisor">Supervisor inmediato <span class="au-req">*</span></label>
          <div class="au-input">
            <span class="au-ico"><AuthIcon name="users" /></span>
            <input id="supervisor" v-model="form.supervisor" type="text"
                   placeholder="NOMBRE DEL SUPERVISOR" @input="form.supervisor = plain(form.supervisor)" />
          </div>
          <span class="au-hint">Nombre completo de tu jefe directo</span>
        </div>
      </template>

      <!-- ══════════ PASO 3 · Contacto y acceso ══════════ -->
      <template v-else-if="step === 3">
        <div class="au-field">
          <label for="email">Correo electrónico <span class="au-req">*</span></label>
          <div class="au-input">
            <span class="au-ico"><AuthIcon name="mail" /></span>
            <input id="email" v-model.trim="form.email" type="email" inputmode="email"
                   autocomplete="email" placeholder="nombre@ejemplo.com" />
          </div>
          <span class="au-hint">Lo usarás para iniciar sesión</span>
        </div>

        <div class="au-field">
          <label for="tel">Teléfono <span class="au-req">*</span></label>
          <div class="phone">
            <div class="phone-cc" :class="{ open: showPaises }">
              <button type="button" class="phone-cc-btn" @click.stop="showPaises = !showPaises">
                <b>{{ paisActual.abrev }}</b>
                <span>{{ form.codigoPais }}</span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
                     stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              </button>
              <div v-if="showPaises" class="phone-cc-menu" @click.stop>
                <div class="au-input">
                  <span class="au-ico"><AuthIcon name="search" /></span>
                  <input v-model="paisQuery" type="text" placeholder="Buscar país…" />
                </div>
                <ul>
                  <li v-for="p in paisesFiltrados" :key="p.codigo">
                    <button type="button" @click="selectPais(p)">
                      <b>{{ p.abrev }}</b><span>{{ p.nombre }}</span><em>{{ p.codigo }}</em>
                    </button>
                  </li>
                  <li v-if="!paisesFiltrados.length" class="empty">Sin resultados</li>
                </ul>
              </div>
            </div>

            <div class="au-input phone-num">
              <span class="au-ico"><AuthIcon name="phone" /></span>
              <input id="tel" v-model="form.telefono" type="tel" inputmode="numeric" maxlength="10"
                     autocomplete="tel-national" placeholder="10 dígitos" @input="validatePhone" />
            </div>
          </div>
          <span class="au-hint">Solo los 10 dígitos, sin lada</span>
        </div>

        <div class="au-field">
          <label for="pass">Contraseña <span class="au-req">*</span></label>
          <div class="au-input au-has-btn">
            <span class="au-ico"><AuthIcon name="lock" /></span>
            <input id="pass" v-model="form.password" :type="showPass ? 'text' : 'password'"
                   autocomplete="new-password" placeholder="Mínimo 6 caracteres" />
            <button type="button" class="au-input-btn" tabindex="-1"
                    :aria-label="showPass ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                    @click="showPass = !showPass">
              <AuthIcon :name="showPass ? 'eye-off' : 'eye'" />
            </button>
          </div>
          <div v-if="form.password" class="meter">
            <span :class="['meter-bar', `lv-${fuerza.nivel}`]"><i :style="{ width: fuerza.pct + '%' }"></i></span>
            <em :class="`lv-${fuerza.nivel}`">{{ fuerza.texto }}</em>
          </div>
        </div>

        <div class="au-field">
          <label for="pass2">Confirmar contraseña <span class="au-req">*</span></label>
          <div class="au-input au-has-btn"
               :class="{ 'is-error': form.confirmPassword && !passwordsMatch, 'is-ok': form.confirmPassword && passwordsMatch }">
            <span class="au-ico"><AuthIcon name="check" /></span>
            <input id="pass2" v-model="form.confirmPassword" :type="showPass2 ? 'text' : 'password'"
                   autocomplete="new-password" placeholder="Repite tu contraseña" />
            <button type="button" class="au-input-btn" tabindex="-1"
                    :aria-label="showPass2 ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                    @click="showPass2 = !showPass2">
              <AuthIcon :name="showPass2 ? 'eye-off' : 'eye'" />
            </button>
          </div>
          <span v-if="form.confirmPassword && !passwordsMatch" class="au-hint is-error">
            <AuthIcon name="x" />Las contraseñas no coinciden
          </span>
          <span v-else-if="form.confirmPassword && passwordsMatch" class="au-hint is-ok">
            <AuthIcon name="check" />Las contraseñas coinciden
          </span>
        </div>
      </template>

      <!-- ══════════ PASO 4 · Revisión y privacidad ══════════ -->
      <template v-else>
        <div class="review">
          <h2>Revisa tus datos</h2>
          <dl>
            <div><dt>Nombre</dt><dd>{{ nombreCompleto }}</dd></div>
            <div><dt>CURP</dt><dd class="mono">{{ form.curp }}</dd></div>
            <div><dt>Puesto</dt><dd>{{ cargoFinal }}</dd></div>
            <div><dt>Territorio</dt><dd>{{ form.territorio }}</dd></div>
            <div><dt>{{ esTecnico ? 'Facilitador' : 'Supervisor' }}</dt><dd>{{ form.supervisor || '—' }}</dd></div>
            <div><dt>Correo</dt><dd>{{ form.email }}</dd></div>
            <div><dt>Teléfono</dt><dd>{{ form.codigoPais }} {{ form.telefono }}</dd></div>
          </dl>
          <button type="button" class="review-edit" @click="step = 1">
            <AuthIcon name="edit" />Corregir datos
          </button>
        </div>

        <div class="privacy">
          <div class="privacy-head">
            <AuthIcon name="shield" />
            <h3>Aviso de Privacidad</h3>
          </div>
          <div class="privacy-body">
            <p><b>AVISO DE PRIVACIDAD PARA EL REGISTRO Y USO DE INFORMACIÓN MEDIANTE LA APLICACIÓN MÓVIL DE SEGUIMIENTO</b></p>
            <p>Los datos personales que proporciones a través de esta aplicación serán tratados conforme a la normativa aplicable en materia de protección de datos personales y transparencia.</p>
            <p class="privacy-h">1. Datos que se recaban</p>
            <p>Nombre completo, CURP, número telefónico, correo electrónico, puesto y supervisor asignado, territorio, datos de localización geográfica, actividades realizadas en campo y fotografías.</p>
            <p class="privacy-h">2. Finalidades del tratamiento</p>
            <p>Los datos se utilizan exclusivamente para registrar y dar seguimiento a las actividades del personal en campo, documentar avances y elaborar reportes internos.</p>
            <p class="privacy-h">3. Derechos</p>
            <p>Puedes solicitar el acceso, rectificación, cancelación u oposición al tratamiento de tus datos personales ante el área responsable.</p>
          </div>
        </div>

        <label class="check" :class="{ 'is-error': termsError }">
          <input v-model="termsAccepted" type="checkbox" @change="termsError = ''" />
          <span class="check-box"><AuthIcon name="check-plain" /></span>
          <span class="check-text">
            He leído y acepto el Aviso de Privacidad y los Términos y Condiciones <span class="au-req">*</span>
          </span>
        </label>
        <span v-if="termsError" class="au-hint is-error"><AuthIcon name="x" />{{ termsError }}</span>
      </template>

      <!-- ── Navegación ── -->
      <div class="nav">
        <button v-if="step > 1" type="button" class="au-btn au-btn-ghost nav-back"
                :disabled="loading" @click="prev">
          <AuthIcon name="arrow-left" />Atrás
        </button>

        <button type="submit" class="au-btn au-btn-primary" :disabled="loading || (step === STEPS.length && !termsAccepted)">
          <span v-if="loading" class="au-spin"></span>
          <span>{{ loading ? 'Creando cuenta…' : (step === STEPS.length ? 'Crear mi cuenta' : 'Continuar') }}</span>
          <AuthIcon v-if="!loading" name="arrow-right" class="au-btn-arrow" />
        </button>
      </div>
    </form>

    <div class="au-links">
      <p>¿Ya tienes una cuenta? <router-link to="/login">Iniciar sesión</router-link></p>
    </div>
  </AuthLayout>

  <!-- ── Modal de éxito ── -->
  <Teleport to="body">
    <Transition name="pop">
      <div v-if="showSuccessModal" class="ok-back" @click.self="goToLogin">
        <div class="ok-card" role="dialog" aria-modal="true">
          <span class="ok-ring"><AuthIcon name="check-plain" /></span>
          <h2>¡Cuenta creada!</h2>
          <p>Tu registro se completó correctamente.</p>
          <div class="ok-bar"><i></i></div>
          <p class="ok-note">Redirigiendo al inicio de sesión…</p>
          <button class="au-btn au-btn-primary" @click="goToLogin">Continuar</button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { reactive, ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '../services/apiService.js';
import { checkInternetConnection, getOfflineMessage } from '../utils/network.js';
import AuthLayout from '../components/auth/AuthLayout.vue';
import AuthIcon from '../components/auth/AuthIcon.vue';

const router = useRouter();

const STEPS = [
  { label: 'Datos personales', short: 'Datos' },
  { label: 'Información laboral', short: 'Trabajo' },
  { label: 'Contacto y acceso', short: 'Acceso' },
  { label: 'Revisión y privacidad', short: 'Revisar' },
];

const CARGOS = [
  'TECNICO PRODUCTIVO', 'TECNICO SOCIAL', 'FACILITADOR COMUNITARIO',
  'COORDINACION TERRITORIAL C', 'COORDINACION TERRITORIAL B', 'COORDINACION TERRITORIAL A',
  'ESPECIALISTAS PRODUCTIVOS Y SOCIALES', 'SEMBRADOR', 'OTRO',
];

const TERRITORIOS = [
  'Acapulco - Centro - Norte - Tierra Caliente', 'Acayucan', 'Balancán',
  'Chihuahua / Sonora', 'Colima', 'Comalcalco', 'Córdoba', 'Costa Chica - Montaña',
  'Costa Grande - Sierra', 'Durango / Zacatecas', 'Hidalgo', 'Istmo', 'Michoacán',
  'Mixteca', 'Morelos', 'Nayarit / Jalisco', 'Ocosingo', 'Palenque', 'Papantla',
  'Pichucalco', 'Puebla', 'San Luis Potosí', 'Sinaloa', 'Tamaulipas', 'Tantoyuca',
  'Tapachula', 'Teapa', 'Tlaxcala / Estado de México', 'Tzucacab / Opb', 'Xpujil',
  'Oficinas Centrales',
];

const PAISES = [
  { codigo: '+52', nombre: 'México', abrev: 'MX' },
  { codigo: '+1', nombre: 'Estados Unidos', abrev: 'US' },
  { codigo: '+34', nombre: 'España', abrev: 'ES' },
  { codigo: '+57', nombre: 'Colombia', abrev: 'CO' },
  { codigo: '+56', nombre: 'Chile', abrev: 'CL' },
  { codigo: '+54', nombre: 'Argentina', abrev: 'AR' },
  { codigo: '+51', nombre: 'Perú', abrev: 'PE' },
  { codigo: '+591', nombre: 'Bolivia', abrev: 'BO' },
  { codigo: '+502', nombre: 'Guatemala', abrev: 'GT' },
  { codigo: '+503', nombre: 'El Salvador', abrev: 'SV' },
];

const step = ref(1);
const loading = ref(false);
const isOnline = ref(true);
const message = reactive({ text: '', type: '' });
const showSuccessModal = ref(false);

const form = reactive({
  email: '', nombre: '', primerApellido: '', segundoApellido: '',
  cargo: '', cargoOtro: '', curp: '', territorio: '', supervisor: '',
  codigoPais: '+52', telefono: '', password: '', confirmPassword: '',
});

const curpError = ref('');
const termsAccepted = ref(false);
const termsError = ref('');
const showPass = ref(false);
const showPass2 = ref(false);

/* ── Helpers de formato ── */
const up = s => (s || '').toUpperCase();
const DIACRITICOS = new RegExp('[\u0300-\u036f]', 'g');
const plain = s => up(s).normalize('NFD').replace(DIACRITICOS, '');

const esTecnico = computed(() => ['TECNICO SOCIAL', 'TECNICO PRODUCTIVO'].includes(up(form.cargo)));
const curpValida = computed(() => /^[A-Z0-9]{18}$/.test(form.curp));
const passwordsMatch = computed(() => form.password === form.confirmPassword);
const nombreCompleto = computed(() =>
  `${form.nombre} ${form.primerApellido} ${form.segundoApellido}`.replace(/\s+/g, ' ').trim());
const cargoFinal = computed(() => (form.cargo === 'OTRO' ? form.cargoOtro : form.cargo));

const fuerza = computed(() => {
  const p = form.password;
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

function formatCurp() {
  form.curp = up(form.curp);
  curpError.value = '';
  if (form.curp.length && form.curp.length < 18) {
    curpError.value = `Faltan ${18 - form.curp.length} caracteres`;
  } else if (form.curp.length === 18 && !curpValida.value) {
    curpError.value = 'Solo letras mayúsculas y números';
  }
}

function validatePhone() {
  form.telefono = form.telefono.replace(/\D/g, '').slice(0, 10);
}

/* ── Selector de país ── */
const showPaises = ref(false);
const paisQuery = ref('');
const paisActual = computed(() => PAISES.find(p => p.codigo === form.codigoPais) || PAISES[0]);
const paisesFiltrados = computed(() => {
  const q = paisQuery.value.trim().toLowerCase();
  if (!q) return PAISES;
  return PAISES.filter(p => p.nombre.toLowerCase().includes(q) || p.codigo.includes(q));
});
function selectPais(p) {
  form.codigoPais = p.codigo;
  showPaises.value = false;
  paisQuery.value = '';
}

/* ── Búsqueda de facilitador ── */
const facilitadorQuery = ref('');
const facilitadoresEncontrados = ref([]);
const facilitadorSeleccionado = ref(null);
const buscandoFacilitador = ref(false);
const mostrarResultados = ref(false);
let debounceId = null;

function buscarFacilitadoresRT() {
  facilitadorQuery.value = up(facilitadorQuery.value);
  const q = facilitadorQuery.value.trim();
  mostrarResultados.value = true;

  clearTimeout(debounceId);
  if (q.length < 2) {
    facilitadoresEncontrados.value = [];
    buscandoFacilitador.value = false;
    return;
  }

  buscandoFacilitador.value = true;
  debounceId = setTimeout(async () => {
    try {
      const resp = await apiService.buscarFacilitadores(q);
      facilitadoresEncontrados.value = resp.success ? resp.facilitadores : [];
    } catch (err) {
      console.error('Error buscando facilitadores:', err);
      facilitadoresEncontrados.value = [];
    } finally {
      buscandoFacilitador.value = false;
    }
  }, 300);
}

function seleccionarFacilitador(f) {
  facilitadorSeleccionado.value = f;
  facilitadorQuery.value = '';
  facilitadoresEncontrados.value = [];
  mostrarResultados.value = false;
  form.supervisor = f.nombre_completo;
}

function limpiarFacilitador() {
  facilitadorSeleccionado.value = null;
  facilitadorQuery.value = '';
  facilitadoresEncontrados.value = [];
  mostrarResultados.value = false;
  form.supervisor = '';
}

/* Al dejar de ser técnico se limpia el facilitador y el supervisor heredado */
watch(() => form.cargo, (nuevo, viejo) => {
  if (nuevo === viejo) return;
  if (viejo === 'OTRO' && nuevo !== 'OTRO') form.cargoOtro = '';
  if (!['TECNICO SOCIAL', 'TECNICO PRODUCTIVO'].includes(up(nuevo))) {
    limpiarFacilitador();
    form.supervisor = '';
  }
});

/* ── Validación por paso ── */
function validarPaso(n) {
  if (n === 1) {
    if (!form.nombre.trim()) return 'El nombre es obligatorio';
    if (!form.primerApellido.trim()) return 'El apellido paterno es obligatorio';
    if (!form.segundoApellido.trim()) return 'El apellido materno es obligatorio';
    if (!form.curp.trim()) return 'La CURP es obligatoria';
    if (form.curp.length !== 18) return 'La CURP debe tener 18 caracteres';
    if (!curpValida.value) return 'La CURP solo admite letras mayúsculas y números';
    return '';
  }
  if (n === 2) {
    if (!form.cargo) return 'Selecciona tu puesto de trabajo';
    if (form.cargo === 'OTRO' && !form.cargoOtro.trim()) return 'Especifica tu puesto de trabajo';
    if (!form.territorio) return 'Selecciona tu territorio';
    if (esTecnico.value && !facilitadorSeleccionado.value) return 'Debes seleccionar tu facilitador';
    if (!esTecnico.value && !form.supervisor.trim()) return 'El supervisor inmediato es obligatorio';
    return '';
  }
  if (n === 3) {
    if (!form.email.trim()) return 'El correo electrónico es obligatorio';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())) return 'Ingresa un correo electrónico válido';
    if (!form.telefono.trim()) return 'El número de teléfono es obligatorio';
    if (!/^\d{10}$/.test(form.telefono)) return 'El teléfono debe tener 10 dígitos';
    if (form.password.length < 6) return 'La contraseña debe tener al menos 6 caracteres';
    if (!passwordsMatch.value) return 'Las contraseñas no coinciden';
    return '';
  }
  if (!termsAccepted.value) return 'Debes aceptar el Aviso de Privacidad';
  return '';
}

function prev() {
  message.text = '';
  if (step.value > 1) step.value--;
}

function onSubmit() {
  const error = validarPaso(step.value);
  if (error) {
    message.text = error;
    message.type = 'error';
    if (step.value === STEPS.length) termsError.value = error;
    return;
  }

  message.text = '';
  if (step.value < STEPS.length) {
    step.value++;
    return;
  }
  register();
}

/* ── Alta en el servidor ── */
async function register() {
  if (loading.value) return;

  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
    return;
  }

  loading.value = true;
  message.text = '';

  try {
    const payload = {
      correo: form.email.trim(),
      nombre_completo: up(nombreCompleto.value),
      cargo: up(cargoFinal.value.trim()),
      supervisor: up(form.supervisor.trim()),
      contrasena: form.password,
      curp: form.curp.toUpperCase().trim(),
      telefono: `${form.codigoPais}${form.telefono.trim()}`,
      territorio: form.territorio,
    };
    if (facilitadorSeleccionado.value?.admin_id) {
      payload.facilitador_admin_id = facilitadorSeleccionado.value.admin_id;
    }

    await apiService.createUser(payload);

    showSuccessModal.value = true;
    setTimeout(goToLogin, 3000);
  } catch (error) {
    console.error('Error de registro:', error);
    if (error.response) {
      message.text = error.response.data?.detail || 'No se pudo crear la cuenta.';
    } else if (error.request) {
      message.text = 'No se pudo conectar con el servidor.';
    } else {
      message.text = 'Error al crear la cuenta: ' + error.message;
    }
    message.type = 'error';
    step.value = STEPS.length;
  } finally {
    loading.value = false;
  }
}

function goToLogin() {
  showSuccessModal.value = false;
  router.push('/login');
}

/* ── Ciclo de vida ── */
function onDocClick(e) {
  if (!e.target.closest('.phone-cc')) showPaises.value = false;
  if (!e.target.closest('.fac')) mostrarResultados.value = false;
}
function onEsc(e) {
  if (e.key !== 'Escape') return;
  showPaises.value = false;
  mostrarResultados.value = false;
}

onMounted(async () => {
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
  } else {
    try {
      await apiService.refreshApiUrl();
    } catch (error) {
      console.warn('Error inicializando servicio API:', error);
    }
  }
  document.addEventListener('click', onDocClick);
  document.addEventListener('keydown', onEsc);
});

onUnmounted(() => {
  clearTimeout(debounceId);
  document.removeEventListener('click', onDocClick);
  document.removeEventListener('keydown', onEsc);
});
</script>

<style scoped>
.mono { font-variant-numeric: tabular-nums; letter-spacing: 1px; }

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
.steps {
  list-style: none;
  display: flex;
  margin: 0 0 18px;
  padding: 0;
}
.steps li {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  position: relative;
  font-size: 10.5px;
}
/* Línea conectora entre pasos */
.steps li::before {
  content: '';
  position: absolute;
  top: 12px;
  right: 50%;
  width: 100%;
  height: 2px;
  background: #e2ece6;
}
.steps li:first-child::before { display: none; }
.steps li.done::before, .steps li.now::before { background: var(--au-green-400); }

.steps .dot {
  position: relative;
  z-index: 1;
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
.steps li.done .dot {
  background: var(--au-green-400); border-color: var(--au-green-400); color: #fff;
}
.steps li.now .dot {
  background: var(--au-green-600); border-color: var(--au-green-600); color: #fff;
  box-shadow: 0 0 0 4px rgba(22, 163, 74, 0.14);
}
.steps em {
  font-style: normal;
  font-weight: 600;
  color: var(--au-ink-faint);
}
.steps li.now em { color: var(--au-green-600); }
.steps li.done em { color: var(--au-ink-soft); }

/* ── Facilitador ── */
.fac { position: relative; }
.fac-picked {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 11px;
  border: 1.5px solid var(--au-green-400);
  background: #f0fdf4;
  border-radius: var(--au-r-md);
}
.fac-avatar {
  display: flex; align-items: center; justify-content: center;
  width: 34px; height: 34px; flex-shrink: 0;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--au-green-400), var(--au-green-600));
  color: #fff; font-weight: 700; font-size: 14px;
}
.fac-avatar.sm { width: 28px; height: 28px; font-size: 12px; }
.fac-info { display: flex; flex-direction: column; min-width: 0; flex: 1; text-align: left; }
.fac-info b {
  font-size: 13px; font-weight: 600; color: var(--au-ink);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.fac-info em {
  font-style: normal; font-size: 10.5px; color: var(--au-ink-faint);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.fac-clear {
  display: flex; flex-shrink: 0;
  width: 26px; height: 26px;
  align-items: center; justify-content: center;
  border: none; background: none; cursor: pointer;
  color: var(--au-ink-faint); border-radius: 50%;
}
.fac-clear:hover { background: rgba(0, 0, 0, 0.06); color: var(--au-danger); }
.fac-clear :deep(svg) { width: 14px; height: 14px; }

.fac-results {
  position: absolute;
  z-index: 20;
  top: 100%;
  left: 0; right: 0;
  margin-top: 5px;
  max-height: 230px;
  overflow-y: auto;
  background: #fff;
  border: 1px solid var(--au-surface-border);
  border-radius: var(--au-r-md);
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.16);
}
.fac-results ul { list-style: none; margin: 0; padding: 4px; }
.fac-results li + li { border-top: 1px solid #f1f6f3; }
.fac-results button {
  display: flex; align-items: center; gap: 10px;
  width: 100%; padding: 8px 9px;
  background: none; border: none; cursor: pointer;
  border-radius: var(--au-r-sm);
  font-family: inherit;
}
.fac-results button:hover { background: #f0fdf4; }
.fac-state {
  display: flex; align-items: center; gap: 8px;
  margin: 0; padding: 14px;
  font-size: 12px; color: var(--au-ink-faint);
}

/* ── Teléfono ── */
.phone { display: flex; gap: 8px; align-items: stretch; }
.phone-cc { position: relative; flex-shrink: 0; }
.phone-cc-btn {
  display: flex; align-items: center; gap: 6px; height: 100%;
  padding: 0 11px;
  background: var(--au-surface);
  border: 1.5px solid var(--au-surface-border);
  border-radius: var(--au-r-md);
  cursor: pointer; font-family: inherit;
  color: var(--au-ink);
  transition: border-color 0.18s, background 0.18s;
}
.phone-cc.open .phone-cc-btn { background: #fff; border-color: var(--au-green-500); }
.phone-cc-btn b { font-size: 12.5px; font-weight: 700; }
.phone-cc-btn span { font-size: 12.5px; color: var(--au-ink-soft); }
.phone-cc-btn svg { width: 13px; height: 13px; color: var(--au-ink-faint); }
.phone-num { flex: 1; min-width: 0; }

.phone-cc-menu {
  position: absolute;
  z-index: 20;
  top: calc(100% + 5px);
  left: 0;
  width: 250px;
  padding: 7px;
  background: #fff;
  border: 1px solid var(--au-surface-border);
  border-radius: var(--au-r-md);
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.16);
}
.phone-cc-menu ul { list-style: none; margin: 6px 0 0; padding: 0; max-height: 200px; overflow-y: auto; }
.phone-cc-menu button {
  display: flex; align-items: center; gap: 8px;
  width: 100%; padding: 8px 9px;
  background: none; border: none; cursor: pointer;
  border-radius: var(--au-r-sm); font-family: inherit; text-align: left;
}
.phone-cc-menu button:hover { background: #f0fdf4; }
.phone-cc-menu b { font-size: 11px; font-weight: 700; color: var(--au-green-600); width: 24px; }
.phone-cc-menu span { flex: 1; font-size: 12.5px; color: var(--au-ink); }
.phone-cc-menu em { font-style: normal; font-size: 11.5px; color: var(--au-ink-faint); }
.phone-cc-menu .empty { padding: 12px; font-size: 12px; color: var(--au-ink-faint); text-align: center; }

/* ── Medidor de contraseña ── */
.meter { display: flex; align-items: center; gap: 9px; }
.meter-bar {
  flex: 1; height: 4px; border-radius: 99px;
  background: #e6eee9; overflow: hidden;
}
.meter-bar i {
  display: block; height: 100%; border-radius: 99px;
  transition: width 0.3s ease, background 0.3s ease;
}
.meter-bar.lv-0 i, .meter-bar.lv-1 i { background: #f43f5e; }
.meter-bar.lv-2 i { background: var(--au-gold); }
.meter-bar.lv-3 i { background: var(--au-green-400); }
.meter-bar.lv-4 i { background: var(--au-green-600); }
.meter em {
  font-style: normal; font-size: 10.5px; font-weight: 600;
  white-space: nowrap;
}
.meter em.lv-0, .meter em.lv-1 { color: #e11d48; }
.meter em.lv-2 { color: var(--au-gold-deep); }
.meter em.lv-3, .meter em.lv-4 { color: var(--au-green-600); }

/* ── Revisión ── */
.review {
  background: #f6faf7;
  border: 1px solid var(--au-surface-border);
  border-radius: var(--au-r-md);
  padding: 14px;
}
.review h2 {
  margin: 0 0 10px; font-size: 13px; font-weight: 700; color: var(--au-ink);
}
.review dl { margin: 0; display: flex; flex-direction: column; gap: 7px; }
.review dl > div {
  display: flex; justify-content: space-between; gap: 14px;
  font-size: 12px; align-items: baseline;
}
.review dt { color: var(--au-ink-faint); flex-shrink: 0; }
.review dd {
  margin: 0; font-weight: 600; color: var(--au-ink);
  text-align: right; word-break: break-word;
}
.review-edit {
  display: inline-flex; align-items: center; gap: 6px;
  margin-top: 12px; padding: 6px 12px;
  background: none; border: 1px solid var(--au-green-400);
  border-radius: 99px; cursor: pointer;
  color: var(--au-green-600); font-size: 11.5px; font-weight: 600; font-family: inherit;
  transition: background 0.15s;
}
.review-edit:hover { background: rgba(22, 163, 74, 0.08); }
.review-edit :deep(svg) { width: 12px; height: 12px; }

/* ── Aviso de privacidad ── */
.privacy {
  border: 1px solid var(--au-surface-border);
  border-radius: var(--au-r-md);
  overflow: hidden;
}
.privacy-head {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 13px;
  background: #f0fdf4;
  border-bottom: 1px solid var(--au-surface-border);
  color: var(--au-green-600);
}
.privacy-head :deep(svg) { width: 15px; height: 15px; }
.privacy-head h3 { margin: 0; font-size: 12.5px; font-weight: 700; color: var(--au-ink); }
.privacy-body {
  max-height: 150px;
  overflow-y: auto;
  padding: 12px 13px;
  font-size: 11px;
  line-height: 1.55;
  color: var(--au-ink-soft);
}
.privacy-body p { margin: 0 0 8px; }
.privacy-body p:last-child { margin-bottom: 0; }
.privacy-h { font-weight: 700; color: var(--au-ink); }

/* ── Checkbox ── */
.check {
  display: flex; align-items: flex-start; gap: 10px;
  cursor: pointer; user-select: none;
}
.check input { position: absolute; opacity: 0; width: 0; height: 0; }
.check-box {
  display: flex; align-items: center; justify-content: center;
  width: 20px; height: 20px; flex-shrink: 0; margin-top: 1px;
  border: 2px solid var(--au-surface-border);
  border-radius: 6px;
  background: #fff;
  color: transparent;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}
.check-box :deep(svg) { width: 12px; height: 12px; }
.check input:checked + .check-box {
  background: var(--au-green-500);
  border-color: var(--au-green-500);
  color: #fff;
}
.check input:focus-visible + .check-box { box-shadow: 0 0 0 4px rgba(22, 163, 74, 0.18); }
.check.is-error .check-box { border-color: var(--au-danger); }
.check-text { font-size: 12px; line-height: 1.45; color: var(--au-ink-soft); }

/* ── Navegación ── */
.nav { display: flex; gap: 10px; margin-top: 6px; }
.nav-back { width: auto; flex-shrink: 0; padding-inline: 18px; }
.nav .au-btn-primary { flex: 1; }

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
