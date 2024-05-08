<script setup>
const props = defineProps({
  comments: Array,
});
</script>

<template>
  <div
    class="border rounded-md bg-slate-200 w-[90%] m-auto mr-[-20px] mb-[-20px]"
  >
    <li
      v-for="comment in comments"
      :key="comment.id"
      class="justify-end p-3 flex flex-col h-min border-b border-gray-400"
    >
      <div class="flex items-start mb-4">
        <img
          :src="comment.created_by.get_avatar"
          class="w-12 rounded-full mr-5"
          alt=""
        />
        <div class="flex justify-between items-center w-full">
          <strong class="text-lg">
            <router-link
              :to="{
                name: 'profile',
                params: { userId: comment.created_by.id },
              }"
            >
              {{ comment.created_by.name }}
            </router-link>
          </strong>
          <p class="text-gray-600 font-medium ml-auto">
            {{ comment.created_at_formatted }} ago
          </p>
        </div>
      </div>
      <div class="">
        <p>{{ comment.body }}</p>
      </div>
    </li>
  </div>
</template>

<style scoped>
.border {
  border-radius: 6px 0 6px 0;
}
</style>
