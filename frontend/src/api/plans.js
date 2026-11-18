import { request } from './http'
export const generatePlan = (data) => request('/plans/generate', { method: 'POST', body: JSON.stringify(data) })
