import { request } from './http'

export const queryRoute = (data) => request('/routes/query', { method: 'POST', body: JSON.stringify(data) })
