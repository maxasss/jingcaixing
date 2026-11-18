<script setup>
import { computed, onMounted, ref } from 'vue'
import AttractionForm from './components/AttractionForm.vue'
import { createAttraction, deleteAttraction, listAttractions, updateAttraction } from './api/attractions'

const attractions = ref([]); const keyword = ref(''); const editing = ref(null); const showForm = ref(false); const notice = ref(''); const error = ref('')
const filtered = computed(() => attractions.value.filter((item) => `${item.name}${item.category}`.includes(keyword.value.trim())))
async function load() { try { attractions.value = await listAttractions() } catch (e) { error.value = e.message } }
function create() { editing.value = null; showForm.value = true }
function edit(item) { editing.value = item; showForm.value = true }
async function save(data) { try { const result = editing.value ? await updateAttraction(editing.value.attraction_id, data) : await createAttraction(data); const index = attractions.value.findIndex((item) => item.attraction_id === result.attraction_id); if (index >= 0) attractions.value[index] = result; else attractions.value.push(result); attractions.value.sort((a, b) => a.attraction_id - b.attraction_id); notice.value = '保存成功'; showForm.value = false } catch (e) { error.value = e.message } }
async function remove(item) { if (!confirm(`确认删除“${item.name}”吗？`)) return; try { await deleteAttraction(item.attraction_id); attractions.value = attractions.value.filter((value) => value.attraction_id !== item.attraction_id); notice.value = '已删除' } catch (e) { error.value = e.message } }
onMounted(load)
</script>
<template>
  <main><header><div><p>京彩行 · 本机维护端</p><h1>景点资料管理</h1></div><button @click="create">新增景点</button></header>
  <p class="warning">当前未配置登录认证，仅用于本机课程开发。</p><p v-if="notice" class="notice">{{ notice }}</p><p v-if="error" class="error">{{ error }}</p>
  <input v-model="keyword" class="search" placeholder="按名称或类别筛选景点">
  <AttractionForm v-if="showForm" :model="editing" @submit="save" @cancel="showForm = false" />
  <p>共 {{ filtered.length }} 条景点资料</p>
  <div class="table-wrap"><table><thead><tr><th>ID</th><th>名称</th><th>类别</th><th>时长</th><th>开放时段</th><th>操作</th></tr></thead><tbody><tr v-for="item in filtered" :key="item.attraction_id"><td>{{ item.attraction_id }}</td><td><strong>{{ item.name }}</strong><small>{{ item.description }}</small></td><td>{{ item.category }}</td><td>{{ item.duration }} 分钟</td><td>{{ item.opening_hours }}</td><td><button class="link" @click="edit(item)">编辑</button><button class="link danger" @click="remove(item)">删除</button></td></tr></tbody></table></div></main>
</template>
