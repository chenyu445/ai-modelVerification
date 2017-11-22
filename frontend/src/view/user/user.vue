<template lang="pug">
	.user
		.header.clearfix
			.pull-left.logo
				i.el-icon-MV-model
				span 模型验证
			.space
				p {{usedSpace}}M/{{totalSpace}}M
				.progress
					.progressIn(:style="'width:'+usedSpace/totalSpace *100+'%'")
			.pull-right.exit(@click="logout")
				i.el-icon-MV-exit
		.container
			validation
</template>

<script>
	import Validation from '../common/validation'
	export default {
	  name: 'user',
	  components: {
			validation: Validation
	  },
	  data () {
	    return {
				setDefaultModelVisible:false,
				defaultModel:'',
				formLabelWidth: "120px",
				uploadDialogVisible:false,
	      usedSpace: 600,
				totalSpace: 2048,

			}
	  },
	  computed: {

	  },
	  methods: {
	    logout () {

	    }
	  }
	}
</script>

<style rel="stylesheet/scss" lang="scss">
	.user{
		height: 100%;
		.header{
			height: 42px;
			width: 100%;
			line-height: 42px;
			background-color: #303846;
			color: #ffffff;
			overflow: hidden;
			padding: 0 10px;
			position: fixed;
			z-index: 10;
			.exit{
				padding-top: 5px;
			}
			.el-icon-MV-exit{
				font-size: 30px;
				cursor: pointer;
				&:hover{
					color: #20a0ff;
				}
			}
			.el-icon-MV-model{
				font-size: 36px;
			}
			.logo{
				span{
					font-size: 24px;
					margin-left: 5px;
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
		}
	}

</style>
