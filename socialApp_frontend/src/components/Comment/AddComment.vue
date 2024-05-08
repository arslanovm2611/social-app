<script setup>
import { ref } from "vue";

const props = defineProps({
  submitForm: Function,
});

const comment = ref("");
function submitForm(body) {
  if (body.trim() === "") return;
  props.submitForm(body);
  comment.value = "";
}
</script>

<template>
  <div class="bg-white rounded-md p-5 h-min">
    <form @submit.prevent="submitForm(comment)">
      <div class="h-min flex gap-4">
        <textarea
          v-model="comment"
          placeholder="What are you thinking about?"
          class="bg-gray-100 w-full rounded-md max-h-[75px] min-h-[75px] p-5 font-medium outline-none"
        />
        <button
          class="rounded-md h-[75px] text-white font-medium py-4 px-6 bg-purple-700"
        >
          Post
        </button>
      </div>
    </form>
  </div>
</template>
