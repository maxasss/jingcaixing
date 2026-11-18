import { request } from './http'

export const listAttractions = () => request('/attractions')
