<script setup>
import { ref } from 'vue'
import { generatePlan } from '../api/plans'
import PlanForm from '../components/PlanForm.vue'
import DayPlan from '../components/DayPlan.vue'
const itinerary = ref(null); const error = ref('')
async function submit(data) { try { error.value = ''; itinerary.value = await generatePlan(data); sessionStorage.setItem('itinerary', JSON.stringify(itinerary.value)) } catch (e) { error.value = e.message } }
</script>
<template><main><h1>京彩行</h1><p>北京旅行智能规划系统（本地 Mock 模式）</p><PlanForm @submit="submit" /><p v-if="error" class="error">{{ error }}</p><div v-if="itinerary"><DayPlan v-for="day in itinerary.daily_plans" :key="day.day" :day="day" /></div></main></template>
