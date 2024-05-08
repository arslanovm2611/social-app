<script setup>
import SearchField from "../Search/SearchField.vue";
import Posts from "../layout/Posts.vue";
import SearchedUsers from "../Search/SearchedUsers.vue";
import PeopleIMayKnow from "../layout/PeopleIMayKnow.vue";
import Trends from "../layout/Trends.vue";
import axios from "axios";
import { ref } from "vue";

const posts = ref([]);
const users = ref([]);

function submitForm(query) {
  users.value = [];
  axios
    .post("api/search/", {
      query: query,
    })
    .then((res) => {
      res.data.users.forEach((user) => {
        if (user.id === localStorage.getItem("user.id")) return;
        users.value.push(user);
      });
    })
    .catch((err) => console.error(err));
}
</script>

<template>
  <div>
    <div class="w-95-percent mx-auto grid grid-cols-4 gap-4">
      <div class="col-span-3 flex gap-4 flex-col">
        <SearchField :submitForm="submitForm" />
        <SearchedUsers :users="users" />
        <Posts :posts="posts" />
      </div>
      <div class="bg-gray-100 rounded-md flex flex-col gap-4">
        <PeopleIMayKnow />
        <Trends />
      </div>
    </div>
  </div>
</template>
