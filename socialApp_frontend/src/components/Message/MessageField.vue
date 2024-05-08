<script setup>
import { ref } from "vue";
const props = defineProps({
  sendMessage: Function,
});

const messageField = ref("");
const sendMessage = function (message) {
  if (message.trim() === "") return;
  props.sendMessage(message);
  messageField.value = "";
};
</script>

<template>
  <div>
    <div class="bg-white rounded-md p-5">
      <textarea
        class="w-full min-h-20 bg-gray-100 rounded-md outline-none p-5 text-sm placeholder:font-medium placeholder:text-sm mb-5"
        placeholde
        r="What do you want to say?"
        v-model="messageField"
      ></textarea>
      <hr class="-mx-5" />
      <button
        class="bg-purple-600 border rounded-md py-4 px-6 mb-4 mt-3 text-white"
        @click="sendMessage(messageField)"
      >
        Send
      </button>
    </div>
  </div>
</template>
