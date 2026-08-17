// Configuración de API — la URL base viene siempre de VITE_API_URL (.env),
// nunca hardcodeada. Antes esta constante apuntaba fija al backend de otro
// proyecto (apipwa.sembrandodatos.com, el de PWASV) y el login del admin de
// Agricultura fallaba porque golpeaba una API que no es la suya.
const endpoints = {
  adminLogin: '/admin/login',
  authMe: '/auth/me',
  usuarios: '/usuarios',
}

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8002'

export const API_CONFIG = { baseURL, endpoints }
export const API_URL = baseURL

console.log(`🔗 API URL: ${API_URL}`)

export default API_CONFIG
