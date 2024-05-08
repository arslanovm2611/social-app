<script setup>
import axios from "axios";
import { ref, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";
defineProps({
  user: Object,
  posts: Array,
});

const toastStore = useToastStore();
const route = useRoute();
const router = useRouter();
const showRequest = ref(null);
const userStore = useUserStore();

function sendRequest(e) {
  axios
    .post(`api/friends/${route.params.userId}/requests/`)
    .then((response) => {
      showRequest.value = false;
      if (response.data.message === "request sent") {
        toastStore.showToast(5000, response.data.message, "bg-emerald-500");
      } else {
        toastStore.showToast(5000, response.data.message, "bg-red-300");
      }
    })
    .catch((err) => {
      console.error(err);
    });
}

function logOut() {
  userStore.removeToken();
  router.replace("/auth");
}

function getPosts() {
  axios
    .get(`api/posts/profile/${route.params.userId}/`)
    .then((res) => {
      if (route.params.userId === userStore.user.id) showRequest.value = false;
      else showRequest.value = res.data.can_send_friendship_request;
    })
    .catch((err) => console.error(err));
}

function sendMessage() {
  axios
    .get(`/api/chat/${route.params.userId}/get-or-create/`)
    .then((res) => {
      router.push("/chat");
    })
    .catch((err) => console.error(err));
}

watch(route, () => {
  getPosts();
});

onMounted(() => {
  getPosts();
});
</script>

<template>
  <div class="flex flex-col w-23-percent">
    <div class="bg-white rounded-md p-5 h-min">
      <img
        :src="user.get_avatar"
        class="m-auto mb-4 rounded-full w-[175px] h-[175px]"
        alt=""
      />
      <p class="font-bold text-center mb-6 text-lg">
        {{ user.name }}
      </p>
      <div class="flex justify-between text-slate-500 font-medium text-sm">
        <router-link :to="{ name: 'friends', params: { userId: user.id } }"
          >{{ user.friends_count }} friends</router-link
        >
        <router-link :to="{ name: 'public' }">
          {{ user.posts_count }}
          posts
        </router-link>
      </div>
      <div class="mt-6">
        <div class="flex gap-2">
          <button
            type="button"
            class="rounded-md py-4 px-3 text-center w-full bg-red-700 text-sm text-white"
            v-if="route.params.userId === userStore.user.id"
            @click="logOut"
          >
            Log out</button
          ><router-link
            type="button"
            class="rounded-md py-4 text-center px-3 w-full bg-purple-700 text-sm text-white"
            v-if="route.params.userId === userStore.user.id"
            to="/profile/edit"
          >
            Edit Profile
          </router-link>
        </div>
        <div class="flex w-full flex-cols justify-between items-center">
          <button
            type="submit"
            class="rounded-md py-4 px-3 w-full bg-purple-700 text-sm text-white"
            @click="sendRequest"
            v-if="showRequest"
          >
            Send Friendship request</button
          ><button
            type="submit"
            class="rounded-md py-4 px-3 w-full bg-purple-700 text-sm text-white"
            @click="sendMessage"
            v-if="route.params.userId !== userStore.user.id"
          >
            Send Message
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.w-23-percent {
  width: 22.5%;
}
</style>
