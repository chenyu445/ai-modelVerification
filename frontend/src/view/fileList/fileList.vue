<template lang="pug">
  .file-list
    .header
      .pull-left.logo
        i.el-icon-MV-model
        span 招商银行建行.zip
      .pull-right.exit(@click="logout")
        i.el-icon-MV-exit
    .container
      .main-view
        .filter-bar
          el-input.search-text(placeholder="文件名" icon="search" v-model="searchText")
        .image-list
          el-row(:gutter="20")
            el-col(:span="4" v-for="i in imageList" :key="i")
              img(src="../../assets/logo.png" @click="showimg(i)")
        el-pagination(@size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[10, 20, 50, 100]" :page-size="20" layout="total, sizes, prev, pager, next, jumper" :total="400")

    el-dialog.image-carousel-dialog(:visible.sync="dialogImageVisible" size="full")
      el-carousel(:interval="4000" indicator-position="none" arrow="always" :autoplay="false")
        el-carousel-item(v-for="i in imageList" :key="i")
          img(src="../../assets/logo.png")      
</template>

<script>
	export default {
	  name: 'user',
	  data () {
	    return {
        searchText: '',
        currentPage: 1,
        imageList: [1,2,3,23,23,2,3,23,2,3,23,123,12,321,321,3,21,4,21,3,213,21,3,12,312,3,12,31,23,12,321,3,12,312,21321312],
        dialogImageVisible: false
			}
	  },
	  computed: {

	  },
	  methods: {
	    logout () {

      },
      handleSizeChange () {

      },
      handleCurrentChange () {

      },
      showimg (i) {
        console.log(i)
        this.dialogImageVisible = true
      }
	  }
	}
</script>

<style rel="stylesheet/scss" lang="scss">
	.file-list{
		height: 100%;
		.header{
			height: 42px;
			width: 100%;
			line-height: 42px;
			background-color: #303846;
			color: #939fb3;
			overflow: hidden;
			position: fixed;
			z-index: 10;
			i{
				font-size: 36px;
			}
			.logo{
				span{
					font-size: 24px;
				}
			}
			.space{
				height: 100%;
				display: inline-block;
				line-height: 12px;
				width: 170px;
				margin-left: 20px;
				.progress{
					height: 6px;
					border:1px solid #000;
					position: relative;
					.progressIn{
						position: absolute;
						top: 0;
						left:0;
						height: 100%;
						background-color: #939fb3;
					}
				}
			}
			.exit{
				padding-right: 20px;
			}
		}
		.margin-right-10{
      margin-right: 10px;
    }
		.container{
			padding: 10px;
			height: 100%;
			padding-top: 48px;
			position: relative;
			background-color: #ccc;
      .main-view{
        height: 100%;
        width: 100%;
        padding-top: 40px;
        padding-bottom: 40px;
        position: relative;
        .filter-bar{
          position: absolute;
          top: 0;
          left: 0;
          .search-text{
            width: 250px;
          }
        }
        .image-list{
          height: 100%;
          width: 100%;
          overflow-y: auto;
          overflow-x: hidden;
          img{
            width: 100%;
          }
        }
        .el-pagination{
          position: absolute;
          bottom: 0;
          left: 0;
        }
      }
		}
    .image-carousel-dialog{
      .el-dialog__body{
        position: absolute;
        top: 50%;
        transform: translateY(-50%);  
        width: 100%;  
      }
      .el-carousel{
        .el-carousel__item{
          text-align: center;
        }
      }
    }
	}

</style>
