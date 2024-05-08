<script setup>
import { ref } from "vue";
const props = defineProps({
  submitForm: Function,
});

const query = ref("");
function submitForm() {
  if (query.value !== "") props.submitForm(query.value);
  query.value = "";
}
</script>

<template>
  <form
    class="bg-white p-5 rounded-md flex gap-4 items-center"
    @submit.prevent="submitForm"
  >
    <input
      type="search"
      v-model="query"
      class="bg-gray-100 rounded-md w-full px-4 py-4 text-base font-medium outline-blue-800"
      placeholder="What are you looking for?"
    />
    <button
      class="bg-purple-600 border rounded-md text-base py-4 px-6 h-14 text-white"
    >
      <img src="/search.svg" alt="" class="hover:cursor-pointer" />
    </button>
  </form>
</template>

<style scoped>
.w-95-percent {
  width: 95%;
}
</style>
