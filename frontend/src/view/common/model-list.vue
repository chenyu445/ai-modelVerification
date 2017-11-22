<template lang="pug">
  .modelList
    el-row.setPanel(:gutter="20")
      el-col(:span="20")
        el-input(placeholder="模型名称",icon="search",v-model="searchValue" :on-icon-click="searchModelIconClick(searchValue)")
      el-col(:span="4" )
        el-tooltip(effect="dark" content="设置默认模型" placement="top")
          i.el-icon-MV-Set(@click="setDefaultModelVisible = true")
    ul.clearfix
      li(v-for="model in modelList")
        .logo.pull-left {{model.modelName.charAt(0)}}
        .content.pull-left
          p {{model.modelName}}
          p.modelInfo
            span.version V{{model.modelVersion}}
            span.uploadTime
              i.el-icon-MV-time
              span {{model.updateTime}}
        .totalCount.pull-right {{model.modelFilesNum}}
        .clearfix
    el-dialog(title="设置默认模型" :visible.sync="setDefaultModelVisible")
      el-select.margin-right-10(v-model="defaultModel" placeholder="所有模型")
        el-option(v-for="item in modelList" :key="item.modelId" :label="item.modelName" :value="item")
      .dialog-footer(slot="footer")
        el-button(@click="setDefaultModelVisible = false") 取消
        el-button(type="primary" @click="setDefault") 确定
</template>
<script type="text/javascript">
export default {
  name: 'modelList',
  components: {
  },
  data () {
    return {
      setDefaultModelVisible:false,
      defaultModel:'',
      formLabelWidth: "45px",
      searchValue: '',
      modelList: [
        {
          modelId:1
          ,modelName:'动态键盘'
          ,modelVersion:1.4
          ,modelFilesNum:5
          ,updateTime:'2017-9-28'
          ,icon:''
        }
        ,{
          modelId:2
          ,modelName:'动态密码'
          ,modelVersion: 1.2
          ,modelFilesNum: 10
          ,updateTime:'2017-9-28'
          ,icon:''
        }
        ,{
          modelId:3
          ,modelName:'模型3'
          ,modelVersion: 1.2
          ,modelFilesNum: 20
          ,updateTime:'2017-9-28'
          ,icon:''
        }
      ]
    }
  },
  computed: {

  },
  methods: {
    searchModelIconClick (value) {
      console.log(value)
    }
    ,setDefault (e) {
      console.log(e)
      this.setDefaultModelVisible = true
    }
  }
}

</script>

<style lang="scss">
.modelList{
  .el-icon-MV-Set{
    font-size: 25px;
    margin-top: 6px;
    color: #20a0ff;
    cursor: pointer;
  }
  .el-select{
    width: 100%;
  }
  .setPanel{
    padding:10px;
  }
  li{
    padding:5px 10px;
    cursor: pointer;
    height: 42px;
    &:hover{
      background-color: #d7e7f1;
    }
  }

  .logo{
    width: 30px;
    height: 30px;
    background-color: #ccc;
    border-radius: 4px;
  }
  .content{
    padding-left: 5px;
    .modelInfo{
      color:#777;
      .version{
        display: inline-block;
        width: 50px;
      }
    }
  }
  .totalCount{
    color: #28B779;
    line-height: 40px;
  }
}
</style>
