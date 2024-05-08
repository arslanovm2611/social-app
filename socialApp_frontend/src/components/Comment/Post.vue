<script setup>
import CommentItem from "../Comment/CommentItem.vue";

const props = defineProps({
  post: Object,
  likePost: Function,
});

function likePost(id, e) {
  props.likePost(id, e);
}
</script>

<template>
  <div>
    <li class="bg-white rounded-md p-5 flex flex-col h-min mb-4">
      <div class="flex items-center mb-6 relative">
        <img
          :src="post.created_by.get_avatar"
          class="w-12 rounded-full mr-5 w-[50px] h-[50px]"
          alt=""
        />
        <strong class="text-lg">
          <router-link
            :to="{ name: 'profile', params: { userId: post?.created_by.id } }"
          >
            {{ post.created_by.name }}
          </router-link>
        </strong>
        <p class="absolute right-0 text-gray-600 font-medium">
          {{ post.created_at_formatted }} ago
        </p>
      </div>
      <div
        class="mb-6"
        v-if="post.attachments.length"
        v-for="image in post.attachments"
        :key="image.id"
        :src="image.image"
      >
        <p><img :src="image.get_image" alt="" class="w-full rounded-md" /></p>
      </div>
      <div class="mb-6">
        <p>{{ post.body }}</p>
      </div>
      <div class="flex relative mb-8">
        <div
          class="flex mr-10 hover:cursor-pointer"
          @click="likePost(post.id, $event)"
        >
          <img src="/favorite.svg" class="mr-3" alt="" />
          <p class="text-gray-600">
            <span>{{ post.likes_count }}</span> likes
          </p>
        </div>
        <router-link
          class="flex hover:cursor-pointer"
          :to="{ name: 'postview', params: { userId: post.id } }"
        >
          <img src="/comment.svg" class="mr-3" alt="" />
          <p class="text-gray-600">{{ post.comments_count }} comments</p>
        </router-link>
        <div>
          <img
            src="/more.svg "
            alt=""
            class="absolute right-0 hover:cursor-pointer"
          />
        </div>
      </div>
      <CommentItem :comments="post.comments" />
    </li>
  </div>
</template>
