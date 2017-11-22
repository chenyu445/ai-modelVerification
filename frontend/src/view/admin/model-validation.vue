<template lang="pug">
  .model-validation
    validation
</template>

<script>
import Validation from '../common/validation'

export default {
  name: 'manage-user',
  components: {
    validation: Validation
  },
  data () {
    return {

    }
  },
  computed: {

  },
  methods: {
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
	.model-validation{
    position: relative;
    height: 100%;
    width: 100%;
    padding: 20px 0;

  }
</style>
