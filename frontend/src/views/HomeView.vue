<script setup>
import { onMounted, ref } from 'vue'
import { listAttractions } from '../api/attractions'
import { addAttraction, deleteAttraction, generatePlan } from '../api/plans'
import PlanForm from '../components/PlanForm.vue'
import DayPlan from '../components/DayPlan.vue'
const itinerary = ref(null); const attractions = ref([]); const error = ref(''); const editing = ref(false)
function save(value) { itinerary.value = value; sessionStorage.setItem('itinerary', JSON.stringify(value)) }
async function submit(data) { try { error.value = ''; save(await generatePlan(data)) } catch (e) { error.value = e.message } }
async function edit(day, attractionId, operation) {
  if (!itinerary.value) return
  editing.value = true; error.value = ''
  try {
    const request = { itinerary: itinerary.value, day, attraction_id: attractionId }
    save(operation === 'add' ? await addAttraction(request) : await deleteAttraction(request))
  } catch (e) { error.value = e.message } finally { editing.value = false }
}
onMounted(async () => {
  try { attractions.value = await listAttractions(); const cached = sessionStorage.getItem('itinerary'); if (cached) itinerary.value = JSON.parse(cached) }
  catch (e) { error.value = `无法加载景点资料：${e.message}` }
})
</script>
<template>
  <main>
    <header class="hero"><p>北京旅行智能规划系统</p><h1>京彩行</h1><span>本地 Mock 行程与路线服务</span></header>
    <PlanForm @submit="submit" />
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="editing" class="notice">正在更新行程…</p>
    <div v-if="itinerary" class="itinerary-results">
      <h2>你的旅行行程</h2>
      <DayPlan v-for="day in itinerary.daily_plans" :key="day.day" :day="day" :attractions="attractions" @add="edit(day.day, $event, 'add')" @remove="edit(day.day, $event, 'delete')" />
    </div>
  </main>
</template>
