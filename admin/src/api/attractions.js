const BASE_URL = 'http://127.0.0.1:8000/api/admin/attractions'
async function request(path = '', options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options })
  const body = await response.json()
  if (!response.ok) throw new Error(body.message || '请求失败')
  return body.data
}
export const listAttractions = () => request()
export const createAttraction = (data) => request('', { method: 'POST', body: JSON.stringify(data) })
export const updateAttraction = (id, data) => request(`/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const deleteAttraction = (id) => request(`/${id}`, { method: 'DELETE' })
