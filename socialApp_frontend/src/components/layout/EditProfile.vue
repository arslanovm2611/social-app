<template>
  <div>
    <div class="w-1/2 mx-auto px-6 m-auto">
      <div class="bg-white m-3 rounded-md px-10 py-12">
        <p class="text-2xl font-medium mb-5">Edit Profile</p>
        <form @submit.prevent="submitForm">
          <div class="mb-6">
            <p class="mb-2 font-medium text-lg">Name</p>
            <input
              v-model="form.name"
              type="text"
              class="py-4 px-6 w-full border-2 rounded-md border-slate-200 outline-none placeholder:font-medium"
              placeholder="Your full name"
            />
          </div>
          <div class="mb-6">
            <p class="mb-2 font-medium text-lg">E-mail</p>
            <input
              v-model="form.email"
              type="text"
              class="py-4 px-6 w-full border-2 rounded-md border-slate-200 outline-none placeholder:font-medium"
              placeholder="Your e-mail address"
            />
          </div>
          <div class="mb-6">
            <label class="mb-2 font-medium text-lg cursor-pointer"
              >Change avatar

              <input
                type="file"
                ref="file"
                class="w-full outline-none placeholder:font-medium"
              />
            </label>
          </div>

          <div class="grid grid-row">
            <template v-if="errors.length">
              <div class="bg-red-500 rounded-lg text-white p-6">
                <p v-for="error in errors" :key="error">{{ error }}</p>
              </div>
            </template>
            <button
              class="bg-purple-600 border rounded-md py-4 px-6 mb-4 text-white font-medium"
            >
              Updata changes
            </button>
            <router-link
              to="/profile/edit/password"
              class="underline font-medium"
              >Change Password</router-link
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";

export default {
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();

    return {
      toastStore,
      userStore,
    };
  },
  data() {
    return {
      errors: [],
      form: {
        name: this.userStore.user.name,
        email: this.userStore.user.email,
        avatar: null,
      },
    };
  },
  methods: {
    async submitForm() {
      this.errors = [];
      if (this.form.name === "") this.errors.push("Please, input your name");
      if (!this.form.email.includes("@"))
        this.errors.push("Please, input your email");
      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("avatar", this.$refs.file.files[0]);
        formData.append("name", this.form.name);
        formData.append("email", this.form.email);

        await axios
          .post("/api/editprofile/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            if (response.data.message === "changes updated") {
              this.toastStore.showToast(
                5000,
                "Successfully updated!",
                "bg-emerald-500"
              );
              this.userStore.setUserInfo({
                id: this.userStore.user.id,
                name: this.form.name,
                email: this.form.email,
              });

              this.$router.back();
            } else {
              this.toastStore.showToast(
                5000,
                response.data.message,
                "bg-red-300"
              );
            }
          })
          .catch((error) => console.error(error));
      }
    },
  },
};
</script>
