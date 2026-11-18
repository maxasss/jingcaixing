<script setup>
defineProps({ route: { type: Object, default: null }, loading: Boolean, error: { type: String, default: '' } })
</script>

<template>
  <div class="route-info">
    <h4>路线与交通</h4>
    <p v-if="loading">正在刷新路线信息…</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <p v-else-if="!route || !route.segments.length">添加至少两个景点后显示路线。</p>
    <ol v-else>
      <li v-for="segment in route.segments" :key="`${segment.start_id}-${segment.end_id}`">
        {{ segment.distance_meters }} 米 · 约 {{ segment.estimated_minutes }} 分钟：{{ segment.traffic_info }}
      </li>
    </ol>
  </div>
</template>
