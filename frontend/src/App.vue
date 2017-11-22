<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'app'
}
</script>
<style rel="stylesheet/scss" lang="scss">
@import '~normalize.css/normalize.css';// normalize.css 样式格式化
@import url("./assets/iconfont/iconfont.css"); //图标字体
  html , body , #app {
    height: 100%;
    width: 100%;
    min-width: 1280px;
    font-size: 12px;
    color: #333;
  }

  [class^="el-icon-MV"], [class*="el-icon-MV"] {
    font-family:"iconfont" !important;
    font-size:16px;
    font-style:normal;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  a{
    text-decoration:none;
  }
  *{
    box-sizing: border-box;
  }
  *{
    margin:0;
    padding:0;
  }
  .pull-left{
    float: left;
  }
  .pull-right{
    float: right;
  }
  .clearfix{
    clear: both;
  }

  .margin-right-10{
    margin-right: 10px;
  }
</style>
