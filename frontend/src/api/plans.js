import { request } from './http'
export const generatePlan = (data) => request('/plans/generate', { method: 'POST', body: JSON.stringify(data) })
export const addAttraction = (data) => request('/plans/edit/add', { method: 'POST', body: JSON.stringify(data) })
export const deleteAttraction = (data) => request('/plans/edit/delete', { method: 'POST', body: JSON.stringify(data) })
