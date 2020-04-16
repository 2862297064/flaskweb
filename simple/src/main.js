import Vue from 'vue'
import VueRouter from 'vue-router'
import IndexPage from './pages/index.vue'
import Layout from './Layout.vue'
import mock from 'mock/mock.js'

Vue.use(VueRouter)
let router = new VueRouter({
  mode:'history',
  routes: [
    { path:'/',component:IndexPage },
  ]
})


new Vue({
  el: '#app',
  router,
  // render: h => h(App),
  components:{
    Layout
  },
  template:'<Layout/>'
})
