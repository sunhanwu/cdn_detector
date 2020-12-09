<template>
  <div class="hello">    
    <img src="../assets/logo.png">
    <h1>{{ msg }}</h1>
    <h2>
      <el-input v-model="input" placeholder="请输入域名" style="display:inline-table; width: 30%; float:middle" @keyup.enter.native="searchnews()" clearable></el-input>
      <el-button type="primary" @click="searchnews()" style="float:middle; margin: 20px;">查询</el-button>
    </h2>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to CDN-Detetor',
      input:'',
    }
  },
  methods:{
    searchnews(){
      // this.$http.get('http://127.0.0.1:8000/api/add?search=' + this.search)
      //   .then((response) => {
      //     var res = JSON.parse(response.bodyText)
      //     console.log('1',res)
          this.$router.push({path:'/finall',query: {search:this.input}})
        // })
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
