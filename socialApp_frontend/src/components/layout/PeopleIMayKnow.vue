<script setup>
import router from "@/router";
import axios from "axios";
import { ref, onMounted } from "vue";

const users = ref([]);

function getSuggestedUsers(id) {
  axios
    .get("/api/friends/suggested/")
    .then((res) => {
      users.value = res.data;
    })
    .catch((err) => console.error(err));
}

function showUser(id) {
  router.push({ name: "profile", params: { userId: id } });
}

onMounted(() => {
  getSuggestedUsers();
});
</script>

<template>
  <div>
    <div class="bg-white rounded-md h-min p-5">
      <h1 class="text-xl font-medium mb-8">People you may know</h1>
      <ul class="gap-2">
        <li
          class="flex items-center relative mb-5"
          v-if="users.length"
          v-for="user in users"
        >
          <img
            :src="user.get_avatar"
            alt=""
            class="w-12 rounded-full w-[75px] h-[75px]"
          />
          <b>{{ user.name }}</b>
          <button
            class="bg-purple-600 absolute right-0 rounded-md text-base text-white px-3 py-2"
            @click="showUser(user.id)"
          >
            Show
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>
