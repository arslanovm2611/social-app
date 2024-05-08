<script setup>
import { ref } from "vue";
const props = defineProps({
  submitForm: Function,
});
const body = ref("");
const file = ref(null);
const url = ref(null);
const is_private = ref(false);

function submitForm() {
  if (!body.value.trim()) return;
  let formData = new FormData();
  formData.append("image", file.value.files[0]);
  formData.append("body", body.value);
  formData.append("is_private", is_private.value);
  props.submitForm(formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  body.value = "";
  url.value = null;
  is_private.value = false;
}

function onFileChange(e) {
  url.value = URL.createObjectURL(e.target.files[0]);
}
</script>

<template>
  <div class="bg-white rounded-md p-5 h-min">
    <form @submit.prevent="submitForm" method="post">
      <div class="h-min mb-3">
        <textarea
          v-model="body"
          placeholder="What are you thinking about?"
          class="bg-gray-100 w-full rounded-md h-24 p-5 font-medium outline-none mb-6"
        />
        <div id="preview" v-if="url">
          <img :src="url" class="w-[100px] rounded-xl my-2" />
        </div>

        <hr class="-mx-5" />
        <label for="is_private" class="flex items-center">
          <input type="checkbox" v-model="is_private" id="is_private" />
          <p class="ml-2">Private</p>
        </label>
        <div class="flex justify-between text-white font-medium mt-4">
          <label class="rounded-md py-4 px-6 bg-gray-500 cursor-pointer">
            Attach image
            <input
              type="file"
              ref="file"
              class="w-full outline-none placeholder:font-medium"
              @change="onFileChange"
            />
          </label>
          <button type="submit" class="rounded-md py-4 px-6 bg-purple-700">
            Post
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<style>
input[type="file"] {
  display: none;
}
</style>
