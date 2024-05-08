<script setup>
import router from "@/router";
import AuthButtons from "./layout/AuthButtons.vue";
const props = defineProps({
  user: Object,
  useravatar: String,
});

function goPublic() {
  router.push("/public");
}
</script>

<template>
  <nav class="py-10 px-8 border-b border-gray-200">
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center">
        <div class="menu-left">
          <p @click="goPublic" class="text-xl cursor-pointer">Shareme</p>
        </div>
        <!-- {{ user }} -->
        <div class="menu-center flex space-x-12" v-if="user.id">
          <router-link :to="{ name: 'public' }"
            ><img src="/home.svg" alt="" class="hover:cursor-pointer" />
          </router-link>
          <router-link to="/notifications">
            <img src="/notifications.svg" alt="" class="hover:cursor-pointer"
          /></router-link>
          <router-link :to="{ name: 'chat' }"
            ><img src="/sms.svg" alt="" class="hover:cursor-pointer" />
          </router-link>
          <router-link :to="{ name: 'search' }">
            <img src="/search.svg" alt="" class="hover:cursor-pointer"
          /></router-link>
        </div>
        <div>
          <router-link
            v-if="user.id"
            :to="{ name: 'profile', params: { userId: user.id } }"
          >
            <img
              :src="useravatar"
              alt=""
              class="w-14 rounded-full w-[75px] h-[75px]"
            />
          </router-link>
          <div v-else>
            <auth-buttons />
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.router-link-active {
  border-bottom: solid 2px black;
}
</style>
