import Vue from 'vue'
import Router from 'vue-router'

const Login = () => import('../view/login/login')
const Admin = () => import('../view/admin/admin')
const manageUser = () => import('../view/admin/manage-user')
const ModelStatistics = () => import('../view/admin/model-statistics')
const ModelValidation = () => import('../view/admin/model-validation')
const User = () => import('../view/user/user')
const fileList = () => import('../view/fileList/fileList')

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
      redirect: '/admin/manage-user',
      children: [
        { path: 'manage-user', component: manageUser, name: 'manage-user' },
        { path: 'model-statistics', component: ModelStatistics, name: 'model-statistics' },
        { path: 'model-validation', component: ModelValidation, name: 'model-validation' }
      ]
    },
    {
      path: '/user',
      name: 'user',
      component: User
    },
    {
      path: '/filelist/:id',
      name: 'fileList',
      component: fileList
    },
    {
      path: '*',
      redirect: '/login'
    }
  ]
})
