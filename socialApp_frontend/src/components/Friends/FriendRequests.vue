<script setup>
defineProps({
  users: Array,
  handleRequest: Function,
});
</script>

<template>
  <div>
    <hr class="mb-4" />
    <div class="bg-white rounded-md p-5" v-if="users.length">
      <h2 class="text-xl mb-6 mt-2 font-medium text-center">
        Friendship requests
      </h2>
      <div class="w-full mr-10">
        <div
          class="bg-gray-100 p-5 rounded-md text-center items-center"
          v-for="user in users"
          :key="user.id"
        >
          <img
            :src="user.created_by.get_avatar"
            class="rounded-full m-auto w-36 mb-6"
            alt=""
          />
          <strong>
            <router-link
              :to="{ name: 'profile', params: { userId: user.created_by.id } }"
            >
              {{ user.created_by.name }}
            </router-link>
          </strong>
          <div
            class="flex justify-around mt-6 text-sm font-medium text-slate-500"
          >
            <router-link
              :to="{ name: 'friends', params: { userId: user.created_by.id } }"
            >
              {{ user.created_by.friends_count }} <br />
              friends
            </router-link>
            <p>
              {{ user.created_by.posts_count }} <br />
              posts
            </p>
          </div>
          <div class="mt-6 flex justify-around">
            <button
              class="bg-purple-600 rounded-md text-base text-white px-3 py-2"
              @click="handleRequest('accepted', user.created_by.id)"
            >
              Accept
            </button>
            <button
              @click="handleRequest('rejected', user.created_by.id)"
              class="bg-red-600 rounded-md text-base text-white px-3 py-2"
            >
              Reject
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
