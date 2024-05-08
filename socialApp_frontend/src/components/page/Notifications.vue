<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";

import NotificationField from "../layout/NotificationField.vue";

const notifications = ref([]);
function getNotifications() {
  axios
    .get("/api/notifications/")
    .then((res) => {
      notifications.value = res.data;
    })
    .catch((err) => console.error(err));
}

onMounted(() => {
  getNotifications();
});
</script>
<template><NotificationField :notifications="notifications" /></template>
