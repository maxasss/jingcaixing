<script setup>defineProps({ day: { type: Object, required: true } })</script>
<template><section><h3>第 {{ day.day }} 天</h3><ol><li v-for="item in day.attractions" :key="item.attraction_id">景点编号：{{ item.attraction_id }}</li></ol></section></template>
