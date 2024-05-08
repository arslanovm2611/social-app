<script setup>
import axios from "axios";
import Header from "./components/Header.vue";
import { useUserStore } from "@/stores/user";
import { onMounted, ref, watch } from "vue";
const userStore = useUserStore();
const user = ref({});
const useravatar = ref("");
async function getUser() {
  if (!userStore.user.id) return;

  await axios
    .get(`/api/friends/${userStore.user.id}/`)
    .then((res) => {
      useravatar.value = res.data.user.get_avatar;
    })
    .catch((err) => console.error(err));
}
onMounted(() => {
  userStore.initStore();

  const token = userStore.user.access;

  if (token) {
    axios.defaults.headers.common["Authorization"] = "Bearer " + token;
  } else {
    axios.defaults.headers.common["Authorization"] = "";
  }
});

watch(userStore, () => {
  user.value = userStore.user;
  getUser();
});
</script>

<template>
  <Header :user="user" :useravatar="useravatar" />
  <main class="py-8 bg-gray-100">
    <routerView v-slot="{ Component }">
      <transition>
        <component :is="Component"></component>
      </transition>
    </routerView>
  </main>
</template>

<style>
.v-enter-from,
.v-leave-to {
  opacity: 0;
}

.v-enter-active {
  transition: all 0.2s ease-in;
}

.v-leave-active {
  transition: all 0.2s ease-out;
}

v-enter-to,
.v-leave-from {
  opacity: 1;
}
</style>
