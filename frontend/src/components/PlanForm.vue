<script setup>
import { reactive } from 'vue'
const emit = defineEmits(['submit'])
const form = reactive({ days: 1, interests: ['历史人文'], pace: '适中' })
const choices = ['历史人文', '自然风光', '美食探店']
function submit() { emit('submit', { ...form, interests: [...form.interests] }) }
</script>
<template>
  <form @submit.prevent="submit">
    <label>游玩天数 <input v-model.number="form.days" type="number" min="1" max="7"></label>
    <fieldset><legend>兴趣偏好</legend><label v-for="item in choices" :key="item"><input v-model="form.interests" type="checkbox" :value="item">{{ item }}</label></fieldset>
    <label>游览节奏 <select v-model="form.pace"><option>轻松</option><option>适中</option><option>紧凑</option></select></label>
    <button :disabled="!form.interests.length">生成 Mock 行程</button>
  </form>
</template>
