<script setup>
import axios from "axios";
import router from "@/router";
defineProps({
  notifications: Array,
});
async function showDetail(way, id) {
  await axios
    .post(`/api/notifications/read/${id.id}/`)
    .then((res) => {
      if (way === "post") {
        router.push({ name: "postview", params: { userId: id.post_id } });
      } else {
        router.push({ name: "friends", params: { userId: id.created_for_id } });
      }
    })
    .catch((err) => console.error(err));
}
</script>

<template>
  <div v-if="notifications.length">
    <li
      v-for="notification in notifications"
      :key="notification.id"
      class="justify-end py-5 flex flex-col h-min border-b border-gray-400"
    >
      <div class="px-5">
        <span>{{ notification.body }}</span>
        <span
          v-if="
            notification.type_of_notification === 'post_like' ||
            notification.type_of_notification === 'post_unlike' ||
            notification.type_of_notification === 'post_comment'
          "
          class="ml-4 underline font-medium cursor-pointer"
          @click="showDetail('post', notification)"
          >Go to post</span
        >
        <span
          v-else
          @click="showDetail('friend', notification)"
          class="ml-4 underline font-medium cursor-pointer"
        >
          View friends
        </span>
      </div>
    </li>
  </div>
  <p v-else class="px-14">No notification received yet!</p>
</template>
