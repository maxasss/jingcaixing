<script setup>
import { computed, ref } from 'vue'
import html2canvas from 'html2canvas'
import { BACKEND_ORIGIN } from '../api/http'

const props = defineProps({ day: { type: Object, required: true }, details: { type: Array, required: true }, route: { type: Object, default: null } })
const open = ref(false); const exporting = ref(false); const poster = ref(null)
const totalMinutes = computed(() => props.details.reduce((sum, item) => sum + item.attraction.duration, 0))
const routeText = computed(() => props.route?.segments?.reduce((sum, item) => sum + item.distance_meters, 0) || 0)
function imageUrl(path) { return path ? `${BACKEND_ORIGIN}${path}` : '' }
async function download() {
  if (!poster.value) return
  exporting.value = true
  try {
    const canvas = await html2canvas(poster.value, { scale: 2, useCORS: true, backgroundColor: '#fffaf4', logging: false })
    const link = document.createElement('a')
    link.download = `京彩行-第${props.day.day}天.png`
    link.href = canvas.toDataURL('image/png')
    link.click()
  } finally { exporting.value = false }
}
</script>

<template>
  <div class="poster-actions"><button type="button" @click="open = true">预览导览海报</button></div>
  <div v-if="open" class="poster-modal" role="dialog" aria-modal="true">
    <div class="poster-dialog">
      <div class="poster-toolbar"><h3>第 {{ day.day }} 天导览海报</h3><button class="text-button" type="button" @click="open = false">关闭</button></div>
      <div ref="poster" class="poster-canvas">
        <header><p>京彩行 · 北京旅行导览</p><h2>第 {{ day.day }} 天 · 城市漫游</h2><span>{{ details.length }} 个景点 · 建议游览 {{ totalMinutes }} 分钟</span></header>
        <ol class="poster-stops">
          <li v-for="item in details" :key="item.attraction_id">
            <span class="poster-order">{{ item.order }}</span>
            <img v-if="item.attraction.image_path" :src="imageUrl(item.attraction.image_path)" :alt="item.attraction.name" crossorigin="anonymous">
            <div><h4>{{ item.attraction.name }}</h4><p>{{ item.attraction.category }} · {{ item.attraction.opening_hours }}</p><small>{{ item.attraction.description }}</small></div>
          </li>
        </ol>
        <footer><strong>路线总里程：{{ routeText ? `${(routeText / 1000).toFixed(1)} km` : '待生成' }}</strong><span>行程随时可调整 · 以现场开放信息为准</span></footer>
      </div>
      <button type="button" :disabled="exporting" @click="download">{{ exporting ? '正在生成 PNG…' : '下载 PNG 海报' }}</button>
    </div>
  </div>
</template>
