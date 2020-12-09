import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import finall from '@/components/finall'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },  
    {
      path: '/finall',
      name: 'finall',
      component: finall
    },
  ]
})
