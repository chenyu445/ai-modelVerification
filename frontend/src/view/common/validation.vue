<template lang="pug">
	.validation
		.leftSide.pull-left
			modelList
		.rightSide
			.innerRight
				.controlpanel
					el-button(type="primary" @click="uploadFile") Upload
					el-button.margin-right-10(type="primary" @click="removeFile") Remove
					el-select.margin-right-10(v-model="filter.version" placeholder="所有版本")
						el-option(label="所有版本" value="0")
						el-option(v-for="item in versionList" :key="item" :label="item" :value="item")
					el-date-picker.margin-right-10(v-model="filter.time" type="daterange" placeholder="选择日期范围")
					el-input.searchBox(placeholder="文件名",icon="search",v-model="filter.fileName" :on-icon-click="handleIconClick(searchValue)")
				.fileList
					el-table(:data="fileList" stripe)
						el-table-column(type="selection")
						el-table-column(prop="fileName" label="文件名")
						el-table-column(prop="totalNum" label="文件数")
						el-table-column(prop="version" label="最后验证版本号")
						el-table-column(prop="verificationTimes" label="验证次数")
						el-table-column(prop="fileSize" label="文件大小")
						el-table-column(prop="uploadTime" label="UploadTime")
						el-table-column(label="Action")
							template(scope="scope")
								span.iconBtn(@click="runTest(scope.row)")
									i.el-icon-MV-run
								span.iconBtn(@click="fileDetail(scope.row)")
									i.el-icon-MV-detailslist
								span.iconBtn(@click="removeFile(scope.row)")
									i.el-icon-MV-delete
				.pageNation
					el-pagination(@size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="pageNation.currentPage" :page-sizes="pageNation.pageSizes" :page-size="pageNation.currentPageSize" layout="total, sizes, prev, pager, next, jumper" :total="pageNation.total")

		el-dialog(title="上传" :visible.sync="uploadDialogVisible")
			el-form(:model="upload")
				el-form-item(label="文件" )
					el-upload.upload-demo(ref="uploadFile" action="https://jsonplaceholder.typicode.com/posts/" :file-list="uploadFileList" :auto-upload="false" :multiple="false" :on-change="changeUploadFile" :before-upload="beforeUploadFile" :show-file-list="false")
						el-button(slot="trigger" type="primary") 选取文件
					el-input(v-model="upload.file" auto-complete="off" :disabled="true")
						el-button(slot="append") 选取文件
				el-form-item(label="模型" )
					el-select.model-vaule(v-model="upload.model" placeholder="所有模型")
						el-option(v-for="model in modelList" :key="model.modelId" :label="model.modelName" :value="model.modelId")
			.dialog-footer(slot="footer")
				el-button(@click="uploadDialogVisible = false") 取消
				el-button.uploadSubmit(@click="uploadSubmit") 上传
				el-button(type="primary" @click="uploadAndRun") 上传并验证


		el-dialog(title="设置默认模型" :visible.sync="setDefaultModelVisible")
			el-select.model-vaule(v-model="defaultModel" placeholder="所有版本")
				el-option(v-for="item in modelList" :key="item.modelId" :label="item.modelName" :value="item")
			.dialog-footer(slot="footer")
				el-button(@click="setDefaultModelVisible = false") 取消
				el-button(type="primary" @click="setDefault") 确定

		el-dialog(title="确认" :visible.sync="comfirmVisible")
			p 确认删除此文件?
			.dialog-footer(slot="footer")
				el-button(@click="comfirmVisible = false") 取消
				el-button(type="primary" @click="confirmRemove") 确定
		el-dialog.detailList(title="详情列表" :visible.sync="listVisible" )
			table.info
				tr
					td 文件名
					td {{modelInfo.fileName}}
					td 文件数
					td {{modelInfo.fileNum}}
					td 文件大小
					td {{modelInfo.fileSzie}}
				tr
					td 验证次数
					td {{modelInfo.validationTimes}}
					td 上传时间
					td {{modelInfo.uploadTime}}
					td
					td
			el-table(:data="modelInfo.resultList.content" stripe)
				el-table-column(label="结果")
					template(scope="scope")
						span.resultCircle(:class="scope.row.result == 'success' ? 'success':'failure'")
							i.successIcon
							i.failureIcon
						span {{scope.row.result}}
				el-table-column(prop="validateTimeCost" label="耗时")
				el-table-column(prop="version" label="验证版本号")
				el-table-column(prop="validateStartTime" label="验证时间")
				el-table-column(label="Action")
					template(scope="scope")
						span.iconBtn(@click="fileDetail(scope.row)")
							i.el-icon-MV-detailslist
						span.iconBtn(@click="download(scope.row)")
							i.el-icon-MV-download
			.pageNation
				el-pagination(@size-change="detailHandleSizeChange" @current-change="detailHandleCurrentChange" :current-page="modelInfo.resultList.pageIndex" :page-sizes="modelInfo.resultList.pageSizes" :page-size="modelInfo.resultList.currentPageSize" layout="total, sizes, prev, pager, next, jumper" :total="modelInfo.resultList.total")
</template>

<script>
import ModelList from './model-list'
	export default {
	  name: 'validation',
	  components: {
			modelList:ModelList
	  },
	  data () {
	    return {
				listVisible:false,
				comfirmVisible:false,
				setDefaultModelVisible:false,
				defaultModel:'',
				formLabelWidth: "45px",
				uploadDialogVisible:false,
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
				,versionList: [1,2,3,4,5,6]
				,filter: {
					version:''
					,time:''
					,fileName:''
				}
				,fileList: [
					{
						fileId:1
						,fileName:'招商银行动态键盘'
						,fileSize:'36MB'
						,uploadTime:'2017-9-02'
						,status:1
						,uploader:'游走的鱼'
						,totalNum:36
						,version:1.2
						,verificationTimes:10
					}
					,{
						fileId:2
						,fileName:'招商银行动态键盘'
						,fileSize:'36MB'
						,uploadTime:'2017-9-02'
						,status:1
						,uploader:'游走的鱼'
						,totalNum:36
						,version:1.2
						,verificationTimes:10
					}
					,{
						fileId:3
						,fileName:'招商银行动态键盘'
						,fileSize:'36MB'
						,uploadTime:'2017-9-02'
						,status:1
						,uploader:'游走的鱼'
						,totalNum:36
						,version:1.2
						,verificationTimes:10
					}
					,{
						fileId:4
						,fileName:'招商银行动态键盘'
						,fileSize:'36MB'
						,uploadTime:'2017-9-02'
						,status:1
						,uploader:'游走的鱼'
						,totalNum:36
						,version:1.2
						,verificationTimes:10
					}
				]
				,pageNation: {
					currentPage:4
					,pageSizes: [10, 20, 30, 40]
					,currentPageSize: 10
					,total:400
				}
				,filessList: [
					{name: 'food.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}, {name: 'food2.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}
				]
				,upload:{
					file:'',
					model:''
				}
				,uploadFileList: []
				,modelInfo:{
					fileName:'招商银行动态键盘.zip',
					fileNum:20,
					fileSzie:'36.04MB',
					validationTimes:36,
					uploadTime:'2017-09-02 08:06',
					resultList:{
						currentPage:1,
						pageSizes:[10,20,30,40],
						currentPageSize:10,
						total:200,
						content:[
							{
								result:'success',
								validateTimeCost:1000,
								validateStartTime:'2017-09-02 08:06',
								version:1.4
							}
							,{
								result:'success',
								validateTimeCost:1000,
								validateStartTime:'2017-09-02 08:06',
								version:1.4
							}
							,{
								result:'success',
								validateTimeCost:1000,
								validateStartTime:'2017-09-02 08:06',
								version:1.4
							}
							,{
								result:'fail',
								validateTimeCost:1000,
								validateStartTime:'2017-09-02 08:06',
								version:1.4
							}
							,{
								result:'fail',
								validateTimeCost:1000,
								validateStartTime:'2017-09-02 08:06',
								version:1.4
							}
						]
					}
				}
			}
	  },
	  computed: {

	  },
	  methods: {
			handleRemove(file, fileList) {
	      console.log(file, fileList);
	    },
	    handlePreview(file) {
	      console.log(file);
	    }
	    ,toggleSideBar () {

	    },
			uploadFile(){
				this.uploadDialogVisible = true
			},
			removeFile (){
				this.comfirmVisible = true
			},
			uploadSubmit (){
				console.log('uploadSubmit')
				this.$refs.uploadFile.submit()
			},
			handleIconClick (value) {
				console.log(value)
			}
			,setDefault (e) {
				console.log(e)
 				this.setDefaultModelVisible = true
			}
			,handleSizeChange (value){
					console.log('handleSizeChange:',value)
			}
			,handleCurrentChange (value) {
				console.log('handleCurrentChange:',value)
			}
			,detailHandleSizeChange (value){
					console.log('detailHandleSizeChange:',value)
			}
			,detailHandleCurrentChange (value) {
				console.log('detailHandleCurrentChange:',value)
			}
			,runTest (value) {
				console.log('runTest',value)
			}
			,fileDetail (value) {
				// this.$refs.detailList.listVisible = true
				// this.listVisible = true
				console.log('runTest',this)
			}
			,confirmRemove (){

			}
			,uploadAndRun (){

			}
			, changeUploadFile (file, uploadFileList) {
				console.log(this.$refs.uploadFile)
				this.$refs.uploadFile.uploadFiles = [file]
				this.upload.file = file.name
			}
			, beforeUploadFile (file) {

			}
	  }
	}
</script>

<style rel="stylesheet/scss" lang="scss">
	.validation{
		height: 100%;
		position: relative;
		.iconBtn i{
			color: #20A0FF;
			font-size: 30px;
			cursor: pointer;
			margin-right:  10px;
		}
		.detailList{
			.el-dialog{
				width: 900px;
				max-height: 620px;
			}
			.info{
				width: 100%;
				border-collapse: collapse;
				tr{
					height: 40px;
					text-align: center;
					td:nth-of-type(2n+1){
						background-color: #efefef;
					}
				}
				td{
	 				border:1px solid #ccc;

	 			}
			}
			.el-table{
				margin:10px 0;
			}
			.resultCircle{
				display: inline-block;
				width: 10px;
				height: 10px;
				border-radius: 5px;
				&.success{
					background-color: #13CE66;
				}
				&.failure{
					background-color: #FF4949;
				}
				+span{
					padding-left: 5px;
				}
			}
		}
		.leftSide{
			width: 300px;
      // position: absolute;
      left: 10px;
			z-index: 1;
      bottom: 0;
      top: 0;
      background-color: #ffffff;
			padding-bottom: 70px;
			// width: 300px;
			height: 100%;
			border:1px solid #ccc;
			// padding:0 10px;
			.innerLeft{
				height: 100%;
				.el-icon-MV-Set{
					font-size: 25px;
					margin-top: 6px;
					color: #20a0ff;
					cursor: pointer;
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
		}
		ul li{
			list-style: none;
		}
		.el-input__inner{
			background-color: #efefef;
			border-color: #ccc;
		}
		.rightSide{
			margin-left: 320px;
			position: relative;
			height: 100%;
			padding-bottom: 40px;
			.innerRight{
				// border: 1px solid red;
				height: 100%;
				position: relative;
				.controlpanel{
					position: absolute;
					width: 100%;
					top:0;
					left: 0;
					.searchBox{
						width:150px;
					}
				}
				.fileList{
					height: 100%;
					padding-top:40px;
					.iconBtn{
						cursor: pointer;
						margin-left: 5px;

					}
				}
			}
		}
		.el-dialog{
			width: 580px;
			// height: 370px;
			.uploadSubmit{
				color: #20A0FF;
				border-color: #20A0FF;
			}
			.upload-demo{
				position: absolute;
				right: 0;
				bottom: 0;
				z-index: 9;
				opacity: 0;
			}
			.el-input__inner{
				background-color: #fff;
				border-color: #ccc;
			}

			.model-vaule{
				width: 100%;
			}

			.el-input.is-disabled .el-input__inner{
				color: #303846;
			}
			.el-dialog__header{
				background-color: #303846;
				color: #fff;
				height: 45px;
				padding-top: 15px;
				.el-dialog__title{
					color: #fff;
				}
			}
		}
	}
</style>
