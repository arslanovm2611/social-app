<script setup>
import { ref, onMounted } from "vue";

import MessageField from "../Message/MessageField.vue";
import MessageList from "../Message/MessageList.vue";
import MessagePage from "../Message/MessagePage.vue";
import axios from "axios";

const conversations = ref([]);
const activeConversation = ref([]);

function getConversation() {
  axios
    .get("api/chat/")
    .then((res) => {
      if (!res.data.length) return;
      conversations.value = res.data;
      if (conversations.value.length) {
        activeConversation.value = conversations.value[0].id;
      }
      getMessages(activeConversation.value);
    })
    .catch((err) => console.error(err));
}

function getMessages(id) {
  axios
    .get(`/api/chat/${id}/`)
    .then((res) => {
      activeConversation.value = res.data;
    })
    .catch((err) => console.error(err));
}

function sendMessage(message) {
  axios
    .post(`/api/chat/${activeConversation.value.id}/send/`, {
      body: message,
    })
    .then((res) => {
      activeConversation.value.messages.push(res.data);
    })
    .catch((err) => console.error(err));
}

function setMessageField(id) {
  getMessages(id);
}

onMounted(() => {
  getConversation();
});
</script>

<template>
  <div>
    <div class="grid gap-4 w-95-percent grid-cols-4 m-auto">
      <div class="bg-white rounded-md h-min p-5">
        <ul class="gap-2 text-center">
          <MessageList
            :conversations="conversations"
            :setMessageField="setMessageField"
          />
        </ul>
      </div>
      <div class="bg-gray-100 rounded-md col-span-3 h-min mt-[-16px]">
        <ul class="bg-white w-full rounded-md mb-4">
          <MessagePage
            v-if="activeConversation.messages"
            :activeConversation="activeConversation"
          />
        </ul>
        <MessageField :sendMessage="sendMessage" />
      </div>
    </div>
  </div>
</template>

<style setup>
.w-95-percent {
  width: 95%;
}
</style>
