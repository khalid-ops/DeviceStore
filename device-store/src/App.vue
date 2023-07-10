<template>
<router-view/>
</template>

<script>
export default {
  name: 'App',

}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body{
  padding:0px;
  margin: 0px
}
.login input, .register input, .Add input{
    width : 300px;
    height : 40px;
    padding-left : 20px;
    margin-bottom: 30px;
    display:block;
    margin-right : auto;
    margin-left : auto;
    border : 1px solid
}
.login button, .register button, .Add button{
    width : 320px;
    height : 40px;
    color : rgb(0, 49, 128);
    font-size : 18px;
    cursor : pointer;
}
.nav{
  background-color : #333;
  overflow : hidden;
}
.nav a{
  float : left ;
  color : white;
  padding: 14px 16px;
  text-align : center;
  font-size: 17px;
  text-decoration: none;
  margin-right: 5px;
  background-color : #333;
}
.nav a:hover{
background:#ddd;
color:#333
}
</style>
