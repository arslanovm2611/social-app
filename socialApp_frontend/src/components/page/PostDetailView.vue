<script setup>
import Post from "../Comment/Post.vue";
import Trends from "../layout/Trends.vue";
import PeopleIMayKnow from "../layout/PeopleIMayKnow.vue";
import AddComment from "../Comment/AddComment.vue";

import axios from "axios";
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";

const route = useRoute();
const post = ref({
  id: null,
  comments: [],
});
function getPost() {
  axios
    .get(`/api/posts/${route.params.userId}/`)
    .then((response) => {
      post.value = response.data.post;
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

function submitForm(body) {
  axios
    .post(`/api/posts/${route.params.userId}/comment/`, {
      body,
    })
    .then((res) => {
      post.value.comments.push(res.data);
      post.value.comments_count += 1;
    })
    .catch((err) => console.error(err));
}
onMounted(() => {
  getPost();
});
</script>

<template>
  <div>
    <div class="py-10 px-8 flex gap-4 w-95-percent m-auto">
      <div class="w-1/2 flex w-full flex-col gap-4">
        <ul>
          <Post :post="post" v-if="post.id" :likePost="likePost" />
        </ul>
        <AddComment :submitForm="submitForm" />
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
