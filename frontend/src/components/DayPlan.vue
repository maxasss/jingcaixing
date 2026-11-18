<script setup>
import { computed, ref, watch } from 'vue'
import AttractionCard from './AttractionCard.vue'
import AttractionPicker from './AttractionPicker.vue'
import RouteInfo from './RouteInfo.vue'
import PosterPreview from './PosterPreview.vue'
import { queryRoute } from '../api/routes'

const props = defineProps({ day: { type: Object, required: true }, attractions: { type: Array, required: true } })
const emit = defineEmits(['add', 'remove'])
const route = ref(null); const routeError = ref(''); const loadingRoute = ref(false)
const details = computed(() => props.day.attractions.map((item) => ({ ...item, attraction: props.attractions.find((value) => value.attraction_id === item.attraction_id) })).filter((item) => item.attraction))
const selectedIds = computed(() => props.day.attractions.map((item) => item.attraction_id))

async function refreshRoute() {
  const ids = selectedIds.value
  route.value = null; routeError.value = ''
  if (ids.length < 2) return
  loadingRoute.value = true
  try { route.value = await queryRoute({ attraction_ids: ids, travel_mode: 'driving' }) }
  catch (error) { routeError.value = error.message }
  finally { loadingRoute.value = false }
}
watch(selectedIds, refreshRoute, { immediate: true })
</script>

<template>
  <section class="day-plan">
    <header><h3>第 {{ day.day }} 天</h3><span>{{ day.attractions.length }} 个景点</span></header>
    <AttractionPicker :attractions="attractions" :selected-ids="selectedIds" @add="emit('add', $event)" />
    <p v-if="!details.length" class="empty">暂未安排景点。</p>
    <div class="attraction-list">
      <AttractionCard v-for="item in details" :key="item.attraction_id" :attraction="item.attraction" :order="item.order" @remove="emit('remove', $event)" />
    </div>
    <RouteInfo :route="route" :loading="loadingRoute" :error="routeError" />
    <PosterPreview :day="day" :details="details" :route="route" />
  </section>
</template>
