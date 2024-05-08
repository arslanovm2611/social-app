<script setup>
import Trends from "../layout/Trends.vue";
import PeopleIMayKnow from "../layout/PeopleIMayKnow.vue";
import Profile from "../Public/Profile.vue";
import FriendRequests from "../Friends/FriendRequests.vue";
import Friends from "../Search/SearchedUsers.vue";

import axios from "axios";
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
const route = useRoute();
const user = ref([]);
const friends = ref([]);
const requests = ref([]);
const posts = ref([]);

function getPosts(id) {
  axios
    .get(`/api/posts/profile/${id}`)
    .then((response) => {
      if (response.data.user.id === route.params.userId) {
        posts.value = response.data.posts;
      } else {
        friends.value.forEach((friend) => {
          if (response.data.posts.length) {
            if (friend.id === response.data.posts[0].created_by.id) {
              friend.posts = response.data.posts;
            }
          } else {
            friend.posts = response.data.posts;
          }
        });
      }
    })
    .catch((err) => console.error(err));
}

function getFriends() {
  user.value = [];
  requests.value = [];
  friends.value = [];
  axios
    .get(`api/friends/${route.params.userId}/`)
    .then((res) => {
      user.value = res.data.user;
      requests.value = res.data.requests;
      friends.value = res.data.friends;
      friends.value.forEach((friend) => {
        getPosts(friend.id);
      });
    })
    .catch((err) => console.error(err));
}

function handleRequest(status, pk) {
  axios
    .post(`api/friends/${pk}/${status}/`)
    .then((res) => {
      getFriends();
    })
    .catch((err) => console.error(err));
}

onMounted(() => {
  getFriends();
  getPosts(route.params.userId);
});

watch(route, () => {
  getFriends();
});
</script>

<template>
  <div>
    <div class="py-10 px-8 flex gap-4 w-95-percent m-auto">
      <Profile :user="user" :posts="posts" />
      <div class="w-1/2 flex flex-col gap-4">
        <FriendRequests
          v-if="requests.length"
          :handleRequest="handleRequest"
          :users="requests"
        />
        <Friends :users="friends" v-if="friends.length" />
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
