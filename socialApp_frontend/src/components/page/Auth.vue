<script setup>
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";
import { ref, reactive, onMounted, onUpdated, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

const toastStore = useToastStore();
const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const auth = ref("Log in");
const showSignUp = ref(false);
const showPass1 = ref(false);
const showPass2 = ref(false);
const errors = ref([]);
const form = reactive({
  name: "",
  email: "",
  password1: "",
  password2: "",
});

async function submitForm() {
  if (route.query.type === "Sign up") {
    errors.value = [];
    if (form.name === "") errors.value.push("Please, input your name");
    if (!form.email.includes("@"))
      errors.value.push("Please, input your email");
    if (form.password1.trim() === "")
      errors.value.push("Please, input your password");
    if (form.password2 === +form.password1)
      errors.value.push("Password does not match");
    if (errors.value.length === 0) {
      await axios
        .post("/api/signup/", form)
        .then((response) => {
          if (response.data.message === "success") {
            toastStore.showToast(
              5000,
              "The user is registered. Please log in!",
              "bg-emerald-500"
            );
            form.name = "";
            form.email = "";
            form.password1 = "";
            form.password2 = "";
            router.push({ name: "auth", query: { type: "Log in" } });
          } else {
            for (const key in response.data.message) {
              errors.value.unshift(response.data.message[key][0]);
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
    }
  } else if (route.query.type === "Log in") {
    errors.value = [];
    const loginForm = {
      email: form.email,
      password: form.password1,
    };

    if (!loginForm.email.includes("@")) {
      errors.value.push("Please, input email");
    } else if (loginForm.password.trim() === "") {
      errors.value.push("Please, input password");
    }

    if (errors.value.length === 0) {
      await axios
        .post("/api/login/", loginForm)
        .then((response) => {
          userStore.setToken(response.data);

          axios.defaults.headers.common["Authorization"] =
            "Bearer " + response.data.access;
        })
        .catch((error) => {
          errors.value.push(error.response.data.detail);
        });
      await axios
        .get("/api/me/")
        .then((response) => {
          userStore.setUserInfo(response.data);

          router.push({ name: "public" });
        })
        .catch((error) => console.error(error));
    }
  }
}

function toggleAuht() {
  if (auth.value === "Log in") {
    auth.value = "Sign up";
  } else if (auth.value === "Sign up") {
    auth.value = "Log in";
  }
}

function changeQueryParams(auth) {
  const url = new URL(window.location.href);
  url.searchParams.set("type", auth.value);
  window.history.pushState({}, "", url);
}

function showPassword(e, a = "first") {
  if (a !== "repeat") showPass1.value = true;
  else showPass2.value = true;
  e.target.nextElementSibling.type = "text";
}

function hidePassword(e, a = "first") {
  if (a !== "repeat") showPass1.value = false;
  else showPass2.value = false;
  e.target.nextElementSibling.type = "password";
}

onMounted(() => {
  auth.value = route.query.type ? route.query.type : "Log in";
});

onUpdated(() => {
  auth.value = route.query.type;
});

watch(auth, () => {
  if (auth.value === "Log in") {
    showSignUp.value = false;
    route.query.type = "Log in";
    changeQueryParams(auth);
  } else if (auth.value === "Sign up") {
    showSignUp.value = true;
    route.query.type = "Sign up";
    changeQueryParams(auth);
  }
});
</script>

<template>
  <div>
    <div class="w-1/2 mx-auto px-6 m-auto">
      <div class="bg-white m-3 rounded-md px-10 py-12">
        <p class="text-2xl font-medium mb-5">{{ auth }}</p>
        <form @submit.prevent="submitForm">
          <div class="mb-6" v-if="showSignUp">
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
          <div class="mb-6 relative">
            <p class="mb-2 font-medium text-lg">Password</p>
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
              v-model="form.password1"
              type="password"
              class="py-4 px-6 w-full border-2 rounded-md border-slate-200 outline-none placeholder:font-medium pr-14"
              placeholder="Your password"
            />
          </div>
          <div class="mb-6 relative" v-if="showSignUp">
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
              v-model="form.password2"
              type="password"
              class="py-4 px-6 w-full border-2 rounded-md border-slate-200 outline-none placeholder:font-medium pr-14"
              placeholder="Repeat your password"
            />
          </div>
          <div class="grid grid-row">
            <template v-if="errors.length">
              <div class="bg-red-500 rounded-lg text-white p-6">
                <p v-for="error in errors" :key="error">{{ error }}</p>
              </div>
            </template>
            <button
              type="submit"
              class="bg-purple-600 border rounded-md py-4 px-6 mb-4 text-white font-medium"
            >
              {{ auth }}
            </button>
            <div>
              <p class="font-bold text-center" v-if="!showSignUp">
                Don't have an account?
                <span class="underline hover:cursor-pointer" @click="toggleAuht"
                  >Click here</span
                >
                to create one!
              </p>
              <p class="font-bold text-center" v-else>
                Already have an account?
                <span class="underline hover:cursor-pointer" @click="toggleAuht"
                  >Click here</span
                >
                to log in!
              </p>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
