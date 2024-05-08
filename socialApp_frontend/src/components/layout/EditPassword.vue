<template>
  <div>
    <div class="w-1/2 mx-auto px-6 m-auto">
      <div class="bg-white m-3 rounded-md px-10 py-12">
        <p class="text-2xl font-medium mb-5">Change Passwod</p>
        <form @submit.prevent="submitForm">
          <div class="mb-6 relative">
            <p class="mb-2 font-medium text-lg">Old Password</p>
            <img
              src="/unvisibile.svg"
              class="absolute right-5 top-[55px] cursor-pointer"
              alt=""
              @click="showPassword($event, 'old')"
              v-if="!showPass3"
            />
            <img
              src="/visibile.svg"
              class="absolute right-5 top-[55px] cursor-pointer"
              v-if="showPass3"
              alt=""
              @click="hidePassword($event, 'old')"
            />
            <input
              v-model="form.old_password"
              type="password"
              class="py-4 px-6 w-full border-2 rounded-md border-slate-200 outline-none placeholder:font-medium"
              placeholder="Your old password"
            />
          </div>
          <div class="mb-6 relative">
            <p class="mb-2 font-medium text-lg">New Password</p>
            <img
              src="/unvisibile.svg"
              class="absolute right-5 top-[55px] cursor-pointer"
              alt=""
              @click="showPassword($event)"
              v-if="!showPass1"
            />
            <img
              src="/visibile.svg"
              class="absolute right-5 top-[55px] cursor-pointer"
              v-if="showPass1"
              alt=""
              @click="hidePassword($event)"
            />

            <input
              v-model="form.new_password1"
              type="password"
              class="py-4 px-6 w-full border-2 rounded-md border-slate-200 outline-none placeholder:font-medium pr-14"
              placeholder="Your new password"
            />
          </div>
          <div class="mb-6 relative">
            <p class="mb-2 font-medium text-lg">Repeat password</p>
            <img
              src="/unvisibile.svg"
              class="absolute right-5 top-[55px] cursor-pointer"
              alt=""
              @click="showPassword($event, 'repeat')"
              v-if="!showPass2"
            />
            <img
              src="/visibile.svg"
              class="absolute right-5 top-[55px] cursor-pointer"
              v-if="showPass2"
              alt=""
              @click="hidePassword($event, 'repeat')"
            />

            <input
              v-model="form.new_password2"
              type="password"
              class="py-4 px-6 w-full border-2 rounded-md border-slate-200 outline-none placeholder:font-medium pr-14"
              placeholder="Your repeated password"
            />
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
              Change Password
            </button>
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
        old_password: "",
        new_password1: "",
        new_password2: "",
      },
      showPass1: false,
      showPass2: false,
      showPass3: false,
    };
  },
  methods: {
    showPassword(e, a = "first") {
      if (a === "repeat") this.showPass2 = true;
      else if (a === "old") this.showPass3 = true;
      else this.showPass1 = true;
      e.target.nextElementSibling.type = "text";
    },

    hidePassword(e, a = "first") {
      if (a === "repeat") this.showPass2 = false;
      else if (a === "old") this.showPass3 = false;
      else this.showPass1 = false;
      e.target.nextElementSibling.type = "password";
    },
    async submitForm() {
      this.errors = [];
      if (this.new_password1 === "") {
        this.errors.push("Please, insert password");
      }
      if (this.new_password2 !== this.new_password1) {
        this.errors.push("Password does not match");
      }
      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("old_password", this.form.old_password);
        formData.append("new_password1", this.form.new_password1);
        formData.append("new_password2", this.form.new_password2);

        await axios
          .post("/api/editpassword/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            if (response.data.message === "success") {
              this.toastStore.showToast(
                5000,
                "Successfully updated!",
                "bg-emerald-500"
              );

              this.$router.push(`/profile/${this.userStore.user.id}`);
            } else {
              for (const key in response.data.message) {
                this.errors.unshift(response.data.message[key][0]);
              }
            }
          })
          .catch((error) => console.error(error));
      }
    },
  },
};
</script>
