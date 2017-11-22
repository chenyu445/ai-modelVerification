<template lang="pug">
  .manage-user
    .search-bar
      el-button.margin-right-10(type="primary" @click="addUserDialogVisible = true; user = {}") 增加用户
      el-select.margin-right-10(v-model="statusVaule" placeholder="所有状态")
        el-option(v-for="status in statusList" :key="status.value" :label="status.label" :value="status.value")
      el-input.search-text.margin-right-10(placeholder="name" icon="search" v-model="searchText" :on-icon-click="handleIconClick")
    .manage-user-main
      el-table(:data="userList" height="auto" stripe)
        el-table-column(prop="userName" label="账户名")
        el-table-column(prop="password" label="密码")
        el-table-column(prop="space" label="空间")
        el-table-column(prop="loginTime" label="登录时间")
        el-table-column(prop="createTime" label="创建时间")
        el-table-column(prop="status" label="状态")
        el-table-column(prop="status" label="操作")
          template(scope="scope")
            el-button(@click="userDetail(scope.row)" type="text" size="small") 详情
            el-button(@click="userDetail(scope.row)" type="text" size="small") 编辑
            el-button(@click="userDetail(scope.row)" type="text" size="small") 启用
    el-pagination(@size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[10, 20, 50, 100]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="400")

    el-dialog(title="增加用户" :visible.sync="addUserDialogVisible")
      el-form(:model="user")
        el-form-item(label="用户名" :label-width="formLabelWidth")
          el-input(v-model="user.userName" auto-complete="off")
        el-form-item(label="密码" :label-width="formLabelWidth")
          el-input(v-model="user.password" auto-complete="off")
      .dialog-footer(slot="footer")
        el-button(@click="addUserDialogVisible = false") 取消
        el-button(type="primary" @click="addUser") 确定
    el-dialog(title="编辑用户" :visible.sync="eidtUserDialogVisible")
      el-form(:model="user")
        el-form-item(label="用户名" :label-width="formLabelWidth")
          el-input(v-model="user.userName" auto-complete="off")
        el-form-item(label="密码" :label-width="formLabelWidth")
          el-input(v-model="user.password" auto-complete="off")
      .dialog-footer(slot="footer")
        el-button(@click="eidtUserDialogVisible = false") 取消
        el-button(type="primary" @click="eidtUser") 确定                
</template>

<script>
import UserService from '@/api/user'

export default {
  name: 'manage-user',
  components: {
  },
  data () {
    return {
      statusVaule: '',
      statusList: [{
        value: '1',
        label: '启用'
      }, {
        value: '2',
        label: '禁用'
      }, {
        value: '0',
        label: '所有状态'
      }],
      searchText: '',
      userList: [],
      // userList: [{
      //   userName: '王小虎',
      //   password: '12312'
      // },{
      //   userName: '王asd虎',
      //   password: '2432'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // },{
      //   userName: '王大虎',
      //   password: '12312'
      // }],
      currentPage: 4,
      pageSize: 10,
      addUserDialogVisible: false,
      eidtUserDialogVisible: false,
      formLabelWidth: "120px",
      user: {}
    }
  },
  computed: {
    //this.initUserList()
  },
  mounted() {
    //this.initUserList()
  },
  created () {
    this.initUserList()
  },
  methods: {
    initUserList () {
      UserService.getUserList({
        pageIndex: this.currentPage,
        pageSize: this.pageSize,
        userNameKey: '',
        roleType: '',
        inuse: ''
      })
        .then(function(res){
          console.log(res)
        })
        .catch(function(error){
          console.log(error)
        })
    },
    handleIconClick(ev) {
      console.log(ev)
    },
    userDetail(user) {
      console.log(user)
      this.eidtUserDialogVisible = true
      this.user = user
    },
    handleSizeChange() {
      console.log('handleSizeChange')
    },
    handleCurrentChange() {
      console.log('handleCurrentChange')
    },
    addUser() {
      console.log('addUser')
      console.log(this.user)
      
      this.addUserDialogVisible = false
    },
    eidtUser() {
      console.log('addUser')
      console.log(this.user)
      this.eidtUserDialogVisible = false
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
	.manage-user{
    position: relative;
    height: 100%;
    width: 100%;
    background-color: #f6f5f6;
    .margin-right-10{
      margin-right: 10px;
    }
    .search-bar{
      position: absolute;
      top: 20px;
      left: 0;
      right: 0;
      .search-text{
        width: 180px;
      }
    }
    .manage-user-main{
      height: 100%;
      width: 100%;
      padding-top: 70px;
      padding-bottom: 60px;
      .el-table{
        height: 100%;
      }
    } 
    .el-pagination{
      position: absolute;
      bottom: 20px;
      left: 0;
      right: 0;
    }
  }
</style>
