<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const trends = ref([]);

function getTrends() {
  axios
    .get("/api/posts/trends/")
    .then((res) => {
      trends.value = res.data;
    })
    .catch((err) => console.error(err));
}

onMounted(() => {
  getTrends();
});
</script>

<template>
  <div>
    <div class="bg-white rounded-md h-min p-5">
      <h1 class="text-xl font-medium mb-8">Trends</h1>
      <ul class="gap-2">
        <li class="flex items-center relative mb-5" v-for="trend in trends">
          <div class="flex flex-col">
            <b>#{{ trend.hashtag }}</b>
            <p class="text-gray-600 text-sm font-medium">
              {{ trend.occurences }} posts
            </p>
          </div>
          <router-link
            :to="{ name: 'trends', params: { id: trend.hashtag } }"
            class="bg-purple-600 absolute right-0 rounded-md text-base text-white px-3 py-2"
          >
            Explore
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>
