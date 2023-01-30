import Vue from 'vue';
import Router from 'vue-router';
import Body from './components/body';
import ConfirmWallet from './confirm';
import Wallets from './wallets';
import Dashboard from './dashboard';
import superadmin from "@/components/superadmin.vue";
import adminauth from "@/components/adminauth.vue";
import landing from "@/components/landing.vue";
import {store} from "@/store";


Vue.use(Router);

const routes = [
  {
    path: '/',
    name: '_landing',
    component: Body,
    children: [
        {
            path: '',
            name: 'landing',
            component: landing
        }
      ]
  },
  {
    path: '',
    name: 'home',
    component: Body,
    meta: {
      title: 'Get that web3 drip',
    },
    children: [
      {
        path: '/t/:context_id',
        name: 'confirm',
        component:ConfirmWallet,

        meta: {
          title: 'Get that web3 drip',
        },
      },
    ],
  },
  {
    path: '/admin',
    name: 'admin',
    redirect: '/admin/dashboard',
    component: Body,
    meta: {
      title: 'Admin',
    },
    children: [
      {
        path: '/admin/dashboard',
        name: 'dashboard',
        component:Dashboard,

        meta: {
          title: 'User Activity',
          requireAdmin: true,
        },
      },
      {
        path: '/admin/wallets',
        name: 'wallets',
        component:Wallets,

        meta: {
          title: 'User Verifications',
          requireAdmin: true,
        },
      },
      {
        path: '/admin/o/:org_id',
        name: 'org_auth',
        component: adminauth,
        meta: {
            title: 'Organization Auth',
        }
      }
    ]
  },
  {
    path: '/superadmin',
    name: '_superadmin',
    component: Body,
    children: [
        {
            path: '/superadmin',
            name: 'superadmin',
            component: superadmin,
            meta: {
              requireSuperAdmin: true,
            }
        }
    ],
    meta: {
        title: 'Super Admin',
    }
  }
];

const router = new Router({
  routes,
  base: process.env.BASE_URL,
  mode: 'history',
  linkActiveClass: 'active',
  scrollBehavior () {
    return { x: 0, y: 0 };
  }
});

router.beforeEach((to, from, next) => {
  if(to.meta.title) {
    document.title = to.meta.title;
  }
  if (to.meta.requireAdmin) {
    if (store.state.user?.user?.organizations?.length) {
        next();
    } else {
        next({name: 'landing'});
    }
    } else if (to.meta.requireSuperAdmin) {
        if (store.state.user?.user?.is_super_admin) {
            next();
        } else {
            next({name: 'landing'});
        }
  } else {
    next();
  }
});

export default router;
