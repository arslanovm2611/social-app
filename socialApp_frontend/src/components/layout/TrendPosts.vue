<script setup>
import Posts from "../layout/Posts.vue";
import Trends from "../layout/Trends.vue";
import PeopleIMayKnow from "../layout/PeopleIMayKnow.vue";

import axios from "axios";
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const posts = ref([]);
function getPosts() {
  axios
    .get(`/api/posts/?trend=${route.params.id}`)
    .then((response) => {
      posts.value = response.data;
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

onMounted(() => {
  getPosts();
});

watch(route, () => {
  getPosts();
});
</script>

<template>
  <div>
    <div class="bg-white rounded-md p-5 flex flex-col h-min mx-16">
      <h2 class="text-xl font-medium">Trend: #{{ route.params.id }}</h2>
    </div>
    <div class="py-10 px-8 flex gap-4 w-95-percent m-auto">
      <div class="w-1/2 flex w-full flex-col gap-4">
        <ul>
          <Posts :likePost="likePost" :posts="posts" />
        </ul>
      </div>
      <div class="flex flex-col gap-4 w-[40%]">
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
