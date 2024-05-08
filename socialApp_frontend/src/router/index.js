import { createRouter, createWebHistory } from 'vue-router'
import Auth from "../components/page/Auth.vue";
import Public from "../components/page/Public.vue";
import Search from "../components/page/Search.vue";
import Message from "../components/page/Message.vue";
import Notifications from "../components/page/Notifications.vue";
import ProfilePage from "../components/page/ProfilePage.vue"
import Friends from '../components/page/Friends.vue'
import PostDetailView from '../components/page/PostDetailView.vue'
import TrendPosts from '../components/layout/TrendPosts.vue'
import EditProfile from '../components/layout/EditProfile.vue'
import EditPassword from '../components/layout/EditPassword.vue'


const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/public' },
    {
      name: 'auth',
      path: '/auth',
      redirect: to => {
        const queryType = to.query.type;
        if (!queryType) {
          return {
            name: 'login',
            query: { type: 'Log in' }
          }
        } else if (queryType === 'Log in') {
          return {
            name: 'login',
            query: { type: 'Log in' }
          }
        } else {
          return {
            name: 'signup',
            query: { type: "Sign up" }
          }
        }

      },
    },
    {
      path: '/login',
      name: 'login',
      component: Auth
    }, {
      path: '/signup',
      name: 'signup',
      component: Auth
    },
    {
      name: 'public',
      path: '/public',
      component: Public, meta: { requiresAuth: true }
    }, {
      name: 'search',
      path: '/search',
      component: Search, meta: { requiresAuth: true }
    }, {
      name: 'chat',
      path: '/chat',
      component: Message, meta: { requiresAuth: true }
    }, {
      name: 'notifications',
      path: '/notifications',
      component: Notifications, meta: { requiresAuth: true }
    }, {
      name: 'profile',
      path: '/profile/:userId',
      component: ProfilePage, meta: { requiresAuth: true }
    }, {
      name: 'editprofile',
      path: '/profile/edit',
      component: EditProfile
    }, {
      name: 'editpassword',
      path: '/profile/edit/password',
      component: EditPassword
    }, {
      name: 'friends',
      path: '/profile/:userId/friends',
      component: Friends
    }, {
      name: 'trends',
      path: '/trends/:id',
      component: TrendPosts
    }, {
      name: 'postview',
      path: '/:userId',
      component: PostDetailView
    }, {
      path: '/:notFound(.*)',
      component: Public
    },

  ]
})


router.beforeEach(function (to, _, next) {
  if (to.meta.requiresAuth && !localStorage.getItem('user.isAuthenticated')) {
    next('/auth');
  } else {
    next();
  }
});

export default router
