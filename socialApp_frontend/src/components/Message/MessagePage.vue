<script setup>
import { useUserStore } from "@/stores/user";
const userStore = useUserStore();

defineProps({
  activeConversation: Object,
});
</script>

<template>
  <div>
    <!-- {{ activeConversation }} -->
    <li v-for="mes in activeConversation.messages">
      <div class="flex p-5">
        <div v-if="mes.created_by.id === userStore.user.id" class="w-full">
          <div
            class="flex justify-end items-start text-white font-medium text-sm"
          >
            <div class="text-wrap">
              <p class="bg-blue-600 max-w-md text-wrap rounded-rt p-3 mb-1">
                {{ mes.body }}
              </p>
              <p class="text-xs text-slate-600 font-medium">
                {{ mes.created_at_formatted }}
              </p>
            </div>
            <img
              :src="mes.created_by.get_avatar"
              class="w-12 ml-5 rounded-full"
              alt=""
            />
          </div>
        </div>
        <div v-else>
          <div class="flex items-start text-black font-medium text-sm">
            <img
              :src="mes.created_by.get_avatar"
              class="w-12 mr-5 rounded-full"
              alt=""
            />
            <div class="">
              <p class="bg-gray-200 rounded-lt max-w-md p-3 text-wrap mb-1">
                {{ mes.body }}
              </p>
              <p class="text-xs text-slate-600 font-medium">
                {{ mes.created_at_formatted }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </li>
  </div>
</template>

<style scoped>
.rounded-rt {
  border-radius: 6px 0 6px 6px;
}
.rounded-lt {
  border-radius: 0 6px 6px 6px;
}
</style>
