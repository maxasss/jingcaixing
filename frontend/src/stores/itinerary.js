import { ref } from 'vue'
export const itinerary = ref(JSON.parse(sessionStorage.getItem('itinerary') || 'null'))
export function saveItinerary(value) { itinerary.value = value; sessionStorage.setItem('itinerary', JSON.stringify(value)) }
