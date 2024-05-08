<script setup>
const props = defineProps({
  conversations: Array,
  setMessageField: Function,
});

function setMessageField(id) {
  props.setMessageField(id);
}

import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
</script>

<template>
  <div v-if="conversations.length">
    <li
      class="mb-5 hover:cursor-pointer w-full"
      v-for="conversation in conversations"
      :key="conversation.id"
      @click="setMessageField(conversation.id)"
    >
      <div
        v-for="user in conversation.users"
        :key="user.id"
        class="flex items-center justify-between w-full"
      >
        <img
          v-if="user.id !== userStore.user.id"
          :src="user.get_avatar"
          alt=""
          class="w-12 rounded-full"
        />
        <p v-if="user.id !== userStore.user.id" class="font-bold">
          {{ user.name }}
        </p>
        <p
          class="font-medium text-gray-600"
          v-if="user.id !== userStore.user.id"
        >
          {{ conversation.modified_at_formatted }} ago
        </p>
      </div>
    </li>
  </div>
  <div v-else class="font-medium">No chat History</div>
</template>
