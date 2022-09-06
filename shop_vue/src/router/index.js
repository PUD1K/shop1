import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import HomeView from '../views/HomeView.vue'

import Product from '../views/Product.vue'
import Category from '../views/CategoryView.vue'
import Search from '../views/SearchView.vue'
import Cart from '../views/Cart.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import MyAcc from '../views/MyAcc.vue'
import Checkout from '../views/Checkout.vue'
import Success from '../views/Success.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart
  },
  {
    path: '/cart/success',
    name: 'Success',
    component: Success
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/myacc',
    name: 'MyAcc',
    component: MyAcc,
    //защита  
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/cart/checkout',
    name: 'Checkout',
    component: Checkout,
    //защита  
    meta: {
      requireLogin: true
    }
  },
  {
    path:'/:category_slug/:product_slug',
    name: 'Product',
    component: Product
  },
  {
    path:'/:category_slug',
    name: 'Category',
    component: Category
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  //  проверяем соответствие каждой записи маршрута      И   если отсутствует токен аутентификации
  if(to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthentificated){
    next({name: 'LogIn', query: { to: to.path } });
  }
  else{
    next()
  }
})

export default router
