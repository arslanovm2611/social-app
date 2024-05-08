<script>
import axios from "axios";

export default {
  props: ["posts", "likePost", "deletePost"],
  data() {
    return {
      showExtra: false,
    };
  },
  methods: {
    likePosts(id, e) {
      this.likePost(id, e);
    },
    toggleExtra(id) {
      if (this.showExtra !== id) this.showExtra = id;
      else this.showExtra = "no";
    },

    reportPost(id) {
      axios
        .post(`/api/posts/${id}/report/`)
        .then((res) => console.log(res))
        .catch((err) => console.error(err));
    },
  },
};
</script>

<template>
  <div>
    <div>
      <li
        v-for="post in posts"
        :key="post.id"
        class="bg-white rounded-md p-5 flex flex-col h-min mb-4"
      >
        <div class="flex items-center mb-6 relative">
          <img
            :src="post.created_by.get_avatar"
            class="w-12 rounded-full mr-5 w-[50px] h-[50px]"
            alt=""
          />
          <div class="flex justify-between items-center gap-4 w-full">
            <strong class="text-lg">
              <router-link
                :to="{
                  name: 'profile',
                  params: { userId: post.created_by.id },
                }"
              >
                {{ post.created_by.name }}
              </router-link>
            </strong>
            <p class="text-gray-600 font-medium">
              {{ post.created_at_formatted }} ago
            </p>
          </div>
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
            @click="likePosts(post.id, $event)"
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
          <p v-if="post.is_private" class="text-gray-600 ml-6">private</p>
          <div @click="toggleExtra(post.id)">
            <img
              src="/more.svg "
              alt=""
              class="absolute right-0 hover:cursor-pointer"
            />
          </div>
        </div>
        <div
          v-if="showExtra === post.id"
          class="flex items-center justify-between w-[30%]"
        >
          <p class="text-red-500 cursor-pointer" @click="deletePost(post.id)">
            Delete
          </p>
          <p
            class="text-orange-500 cursor-pointer"
            @click="reportPost(post.id)"
          >
            Report
          </p>
        </div>
      </li>
    </div>
  </div>
</template>
