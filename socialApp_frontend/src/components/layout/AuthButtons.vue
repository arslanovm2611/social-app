<template>
  <div>
    <router-link
      class="bg-gray-700 border rounded-md py-4 px-6 text-white font-medium mr-2 cursor-pointer"
      :to="{ name: 'auth', query: { type: 'Log in' } }"
    >
      Log in
    </router-link>
    <router-link
      class="bg-purple-600 border rounded-md py-4 px-6 text-white font-medium cursor-pointer"
      :to="{ name: 'auth', query: { type: 'Sign up' } }"
    >
      Sign up
    </router-link>
  </div>
</template>
