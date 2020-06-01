import Vue from 'vue/dist/vue.js'
import VueMathPlugin from './VueMathPlugin.js'
import Vuex from "vuex"

Vue.use(VueMathPlugin)
Vue.use(Vuex)

new Vue({
    el:'#app',
    data:{
        item:30
    },
    store:Store
})

var store = new Vuex.store({
    state:{message: 'Hello'},
    mutations:{},
    actions:{},
    getters:{}
})

