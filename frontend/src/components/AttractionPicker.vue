<script setup>
import { computed, ref } from 'vue'

const props = defineProps({ attractions: { type: Array, required: true }, selectedIds: { type: Array, required: true } })
const emit = defineEmits(['add'])
const selectedId = ref('')
const available = computed(() => props.attractions.filter((item) => !props.selectedIds.includes(item.attraction_id)))
function add() {
  if (selectedId.value) emit('add', Number(selectedId.value))
  selectedId.value = ''
}
</script>

<template>
  <div class="attraction-picker">
    <select v-model="selectedId" aria-label="选择要添加的景点">
      <option value="">添加一个景点…</option>
      <option v-for="item in available" :key="item.attraction_id" :value="item.attraction_id">{{ item.name }}（{{ item.category }}）</option>
    </select>
    <button type="button" :disabled="!selectedId" @click="add">添加</button>
  </div>
</template>
