<template lang="pug">
  .admin
    .admin-header
      el-row.logo-login-out
        el-col(:span="6")
          i.el-icon-MV-model
          span 模型验证
        el-col.text-right(:span="3" :offset="15")
          el-tooltip(class="item" effect="light" content="登出" placement="left")
            i.el-icon-MV-exit(@click="logout")
      el-row
        el-menu.el-menu-demo(theme="dark" :default-active="activeTab" mode="horizontal")
          router-link(:to="'/admin/manage-user'")
            el-menu-item(index="/admin/manage-user")
              i.el-icon-MV-userManagement
              span 用户管理
          router-link(:to="'/admin/model-statistics'")    
            el-menu-item(index="/admin/model-statistics") 
              i.el-icon-MV-statistical
              span 模型统计
          router-link(:to="'/admin/model-validation'")     
            el-menu-item(index="/admin/model-validation")
              i.el-icon-MV-verify
              span 模型验证  
    .admin-main                        
      router-view
</template>

<script>
import userService from '@/api/user'

export default {
  name: 'admin',
  components: {
  },
  data () {
    return {
      activeTab: '/admin/manage-user',
      avatar: '12321'
    }
  },
  computed: {

  },
  methods: {
    toggleSideBar () {
      
    },
    logout () {
      var data = {
        data : {
          email: 'company@qq.com',
          password: 123456,
          languge: 'zh_CN'
        }
      }
      userService.addUser(data)
        .then(function(response) {
          console.log(response)

        })
    }
  },
  beforeRouteEnter (to, from, next) {
    // 在渲染该组件的对应路由被 confirm 前调用
    // 不！能！获取组件实例 `this`
    // 因为当钩子执行前，组件实例还没被创建
    next(vm => {
      // 通过 `vm` 访问组件实例
      vm.activeTab = to.path
    })
  },
  watch: {
    '$route' (to, from) {
      this.activeTab = to.path
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
	.admin{
    height: 100%;
    width: 100%;
    position: relative;
    .admin-header{
      background-color: #303847;
      color: #ffffff;
      padding: 5px 10px 0 10px;
      height: 86px;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      .el-icon-MV-model{
        font-size: 36px;
      }
      .logo-login-out{
        margin-bottom: 5px;
        span{
          font-size: 24px;
          position: relative;
          margin-left: 5px;
        }
      }
      .el-icon-MV-exit{
        font-size: 30px;
        cursor: pointer;
        &:hover{
          color: #20a0ff;
        }
      }
      .el-menu--dark{
        background-color: #303847;
      }
      .text-right{
        text-align: right;
      }
      .el-menu-item.is-active{
        background-color: #ffffff;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
      }
      .el-menu--horizontal .el-menu-item{
        height: 40px;
        line-height: 40px;
        border-bottom: none;
      }
      .el-menu--horizontal>.el-menu-item:hover, .el-menu--horizontal>.el-submenu.is-active .el-submenu__title, .el-menu--horizontal>.el-submenu:hover .el-submenu__title{
        border-bottom: none;
        color: #20a0ff;
      }
    }
    .admin-main{
      height: 100%;
      width: 100%;
      padding-top: 86px;
      background-color: #f6f5f6;
      padding-left: 10px;
      padding-right: 10px;
    }
  }
</style>
