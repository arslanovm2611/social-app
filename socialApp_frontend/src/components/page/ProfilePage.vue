<script setup>
import Posts from "../layout/Posts.vue";
import Trends from "../layout/Trends.vue";
import PeopleIMayKnow from "../layout/PeopleIMayKnow.vue";
import AddPost from "../Public/AddPost.vue";
import Profile from "../Public/Profile.vue";

import axios from "axios";
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores/user";
const route = useRoute();
const posts = ref([]);
const user = ref([]);
const userStore = useUserStore();
function getPosts() {
  axios
    .get(`/api/posts/profile/${route.params.userId}`)
    .then((response) => {
      posts.value = response.data.posts;
      user.value = response.data.user;
    })
    .catch((err) => console.error(err));
}

function deletePost(id) {
  axios
    .delete(`/api/posts/${id}/delete/`)
    .then((res) => {
      console.log(res);
      getPosts();
    })
    .catch((err) => console.error(err));
}
function likePost(id, e) {
  axios
    .post(`api/posts/${id}/like/`)
    .then((res) => {
      if (res.data.like === "liked") {
        e.target.closest(".flex").children[1].children[0].innerText =
          +e.target.closest(".flex").children[1].children[0].innerText + 1;
      } else {
        e.target.closest(".flex").children[1].children[0].innerText =
          +e.target.closest(".flex").children[1].children[0].innerText - 1;
      }
    })
    .catch((err) => console.error(err));
}

function submitForm(body, header) {
  axios
    .post("/api/posts/create/", body, header)
    .then((res) => {
      posts.value.unshift(res.data);
      getPosts();
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
  <div>
    <div class="py-10 px-8 flex gap-4 w-95-percent m-auto">
      <Profile :user="user" />
      <div class="w-1/2 flex flex-col gap-4">
        <AddPost
          :submitForm="submitForm"
          v-if="user.id === userStore.user.id"
        />
        <ul>
          <Posts :likePost="likePost" :deletePost="deletePost" :posts="posts" />
        </ul>
      </div>
      <div class="flex flex-col gap-4 w-23-percent">
        <PeopleIMayKnow />
        <Trends />
      </div>
    </div>
  </div>
</template>

<style scoped>
.w-95-percent {
  width: 95%;
}
</style>
