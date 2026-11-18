<script setup>
import { reactive, watch } from 'vue'
const props = defineProps({ model: { type: Object, default: null } })
const emit = defineEmits(['submit', 'cancel'])
const empty = () => ({ name: '', category: '历史人文', description: '', duration: 120, opening_hours: '09:00-17:00', latitude: 39.9, longitude: 116.4, image_path: '' })
const form = reactive(empty())
watch(() => props.model, (value) => Object.assign(form, value ? { ...value, image_path: value.image_path || '' } : empty()), { immediate: true })
function submit() { emit('submit', { ...form, duration: Number(form.duration), latitude: Number(form.latitude), longitude: Number(form.longitude), image_path: form.image_path || null }) }
</script>
<template>
  <form class="attraction-form" @submit.prevent="submit">
    <label>景点名称<input v-model.trim="form.name" required maxlength="100"></label>
    <label>类别<select v-model="form.category"><option>历史人文</option><option>自然风光</option><option>美食探店</option></select></label>
    <label class="wide">简介<textarea v-model.trim="form.description" required rows="3"></textarea></label>
    <label>建议时长（分钟）<input v-model.number="form.duration" required min="1" max="1440" type="number"></label>
    <label>开放时段<input v-model.trim="form.opening_hours" required></label>
    <label>纬度<input v-model.number="form.latitude" required min="-90" max="90" step="0.000001" type="number"></label>
    <label>经度<input v-model.number="form.longitude" required min="-180" max="180" step="0.000001" type="number"></label>
    <label class="wide">图片路径<input v-model.trim="form.image_path" placeholder="/images/attractions/11.jpg"></label>
    <div class="form-actions"><button type="submit">保存景点</button><button type="button" class="secondary" @click="$emit('cancel')">取消</button></div>
  </form>
</template>
