<script setup>
const props = defineProps({
  users: Array,
});
</script>

<template>
  <div v-if="users">
    <hr class="mb-4" />
    <div class="bg-white rounded-md p-5" v-if="users.length">
      <h2 class="text-xl text-center mb-4 font-medium">Friends</h2>
      <div class="flex flex-wrap items-center justify-evenly gap-4 w-full">
        <div
          class="bg-gray-100 w-fit p-5 rounded-md text-center items-center"
          v-for="user in users"
          :key="user.id"
        >
          <img
            :src="user.get_avatar"
            class="rounded-full w-[175px] h-[175px] mb-6"
            alt=""
          />
          <strong>
            <router-link :to="{ name: 'profile', params: { userId: user.id } }">
              {{ user.name }}
            </router-link>
          </strong>
          <div
            class="flex justify-between mt-6 text-sm font-medium text-slate-500"
          >
            <router-link :to="{ name: 'friends', params: { userId: user.id } }">
              {{ user.friends_count }} <br />
              friends
            </router-link>
            <router-link :to="{ name: 'public' }">
              {{ user.posts_count }}<br />
              posts
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
