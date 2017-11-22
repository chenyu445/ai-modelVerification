<template lang="pug">
  .model-statistics
    .model-search-list-statistical
      .model-search-list
        modelList
      .model-statistical
        .model-statistical-type-main
          .view-type.clearfix
            el-radio-group.pull-right(v-model="viewType" @change="changeViewType")
              el-radio-button(label="1")
                i.el-icon-MV-statistical
              el-radio-button(label="2")
                i.el-icon-MV-list
          .view-main
            .chart-view(v-show="viewType == 1")
              #chart-dom
            .file-list-view(v-show="viewType == 2")
              .statistical-filter-bar
                el-select.margin-right-10.version-vaule(v-model="versionVaule" placeholder="所有版本")
                  el-option(v-for="version in versionList" :key="version.value" :label="version.label" :value="version.value")
                el-date-picker.margin-right-10.date-range(v-model="dateRange" type="daterange" placeholder="选择日期范围" @change="changeDateRange")
                el-input.search-text(placeholder="文件名称" icon="search" v-model="searchText" :on-icon-click="handleIconClick")
              .statistical-file-list
                el-table(:data="fileList" height="auto" stripe)
                  el-table-column(prop="fileName" label="文件名称")
                  el-table-column(prop="fileCount" label="文件数")
                  el-table-column(prop="lastValidationVersion" label="最后版本号")
                  el-table-column(prop="validationCount" label="验证次数")
                  el-table-column(label="文件大小")
                    template(scope="scope")
                      span {{scope.row.fileSize | fileSizeToString}}
                  el-table-column(label="上传时间")
                    template(scope="scope")
                      span {{scope.row.uploadTime | parseTime('YYYY-MM-DD HH:mm:ss')}}
                  el-table-column(label="上传者")
                    template(scope="scope")
                      span {{scope.row.uploadTime | parseTime('YYYY-MM-DD HH:mm:ss')}}
                  el-table-column(label="操作")
                    template(scope="scope")
                      el-button(@click="userDetail(scope.row)" type="text" size="small")
                        i.el-icon-MV-detailslist

              el-pagination(@size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[10, 20, 50, 100]" :page-size="20" layout="prev, pager, next, jumper, sizes, total" :total="400")
</template>

<script>
import echarts from 'echarts'
import ModelList from '../common/model-list'
export default {
  name: 'model-statistics',
  components: {
    modelList: ModelList
  },
  data () {
    return {
      viewType: 1,
      searchText: '',
      log: '213',
      avatar: '12321',
      currentPage: 1,
      chart: null,
      dateRange: '',
      versionVaule: '',
      versionList: [
        {
          value: 1,
          label: 'V1.1'
        },{
          value: 2,
          label: 'V1.2'
        },{
          value: 3,
          label: 'V1.3'
        }
      ],
      fileList: [{
        fileId: '1',
        fileName: '王小虎',
        fileCount: '12312',
        lastValidationVersion: 'v1.1',
        validationCount: '20',
        fileSize: '213210',
        uploadTime: new Date()
      },{
        fileId: '1',
        fileName: '王小虎',
        fileCount: '12312',
        lastValidationVersion: 'v1.1',
        validationCount: '20',
        fileSize: '213210',
        uploadTime: new Date()
      },{
        fileId: '1',
        fileName: '王小虎',
        fileCount: '12312',
        lastValidationVersion: 'v1.1',
        validationCount: '20',
        fileSize: '213210',
        uploadTime: new Date()
      },{
        fileId: '1',
        fileName: '王小虎',
        fileCount: '12312',
        lastValidationVersion: 'v1.1',
        validationCount: '20',
        fileSize: '213210',
        uploadTime: new Date()
      },{
        fileId: '1',
        fileName: '王小虎',
        fileCount: '12312',
        lastValidationVersion: 'v1.1',
        validationCount: '20',
        fileSize: '213210',
        uploadTime: new Date()
      },{
        fileId: '1',
        fileName: '王小虎',
        fileCount: '12312',
        lastValidationVersion: 'v1.1',
        validationCount: '20',
        fileSize: '213210',
        uploadTime: new Date()
      },{
        fileId: '1',
        fileName: '王小虎',
        fileCount: '12312',
        lastValidationVersion: 'v1.1',
        validationCount: '20',
        fileSize: '213210',
        uploadTime: new Date()
      },{
        fileId: '1',
        fileName: '王小虎',
        fileCount: '12312',
        lastValidationVersion: 'v1.1',
        validationCount: '20',
        fileSize: '213210',
        uploadTime: new Date()
      }]
    }
  },
  computed: {

  },
  mounted() {
    this.initChart()
    this.chart = null
  },
  methods: {
    changeDateRange () {

    },
    changeViewType () {
      console.log(this.viewType)
      if(this.viewType == 1){
        this.initChart()
      }else{
        echarts.dispose(document.getElementById('chart-dom'))
        console.log('initlist')
      }
    },
    handleSizeChange () {

    },
    handleCurrentChange () {

    },
    toggleSideBar () {

    },
    logout () {

    },
    handleIconClick () {

    },
    initChart () {
      this.chart = echarts.init(document.getElementById('chart-dom'))
      var option = {
        color: ['#3398DB'],
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
            {
                type : 'category',
                data : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name:'直接访问',
                type:'bar',
                barWidth: '60%',
                data:[10, 52, 200, 334, 390, 330, 220]
            },
            {
                name: '模拟数据',
                type: 'line',
                showSymbol: false,
                hoverAnimation: false,
                data: [10, 52, 200, 334, 390, 330, 220],
                itemStyle:{
                    normal:{
                        color:"#1eb2b5"
                    }
                },
            }
        ]
      };
      this.chart.setOption(option)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
	.model-statistics{
    position: relative;
    height: 100%;
    width: 100%;
    padding: 20px 0;
    .model-search-list-statistical{
      position: relative;
      height: 100%;
      width: 100%;
    }
    .model-search-list{
      width: 300px;
      position: absolute;
      left: 0;
      bottom: 0;
      top: 0;
      background-color: #ffffff;
      border:1px solid #ccc;      
    }
    .model-statistical{
      height: 100%;
      margin-left: 300px;
      padding: 10px 20px;
      .model-statistical-type-main{
        height: 100%;
        width: 100%;
        position: relative;
        .view-type{
          height: 40px;
          position: absolute;
          width: 100%;
          left: 0;
          top: 0;
        }
        .view-main{
          height: 100%;
          width: 100%;
          padding-top: 40px;
          .chart-view{
            background-color: #ffffff;
            height: 100%;
            width: 100%;
          }
          .file-list-view{
            height: 100%;
            width: 100%;
            // background-color: #ffffff;
            padding-top: 50px;
            padding-bottom: 40px;
            position: relative;
            // border: 1px solid #dddddd;
            .statistical-filter-bar{
              position: absolute;
              top: 0;
              left: 0;
              right: 0;
              .search-text{
                width: 150px;
              }
              .version-vaule{
                width: 120px;
              }
              .date-range{
                width: 230px;
              }

            }
            .statistical-file-list{
              height: 100%;
              .el-table{
                height: 100%;
              }
            }
            .el-pagination{
              position: absolute;
              bottom: 0;
              left: 0;
              right: 0;
            }
          }
        }
      }
    }
    #chart-dom{
      width: 100%;
      height: 100%;
    }
  }
</style>
