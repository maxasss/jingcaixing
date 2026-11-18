<script setup>
import { BACKEND_ORIGIN } from '../api/http'
defineProps({ attraction: { type: Object, required: true }, order: { type: Number, required: true } })
defineEmits(['remove'])
function imageUrl(path) { return path ? `${BACKEND_ORIGIN}${path}` : '' }
</script>

<template>
  <article class="attraction-card">
    <img v-if="attraction.image_path" :src="imageUrl(attraction.image_path)" :alt="attraction.name" @error="$event.target.style.display = 'none'">
    <div class="card-content">
      <span class="order">{{ order }}</span>
      <div>
        <h4>{{ attraction.name }}</h4>
        <p class="category">{{ attraction.category }} · 建议 {{ attraction.duration }} 分钟</p>
      </div>
      <button class="text-button" type="button" @click="$emit('remove', attraction.attraction_id)">删除</button>
      <p class="description">{{ attraction.description }}</p>
      <p class="hours">开放时间：{{ attraction.opening_hours }}</p>
    </div>
  </article>
</template>
