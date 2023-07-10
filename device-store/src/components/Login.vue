<template>
    <h1>Login to Electronic store</h1>
    <div class="login">
    <input type="text" v-model='email' placeholder="Email" />
    <input type="text" v-model="password" placeholder="Password" />
    <button v-on:click="userLogin()">Log In</button>
    <p>
    <router-link to="/sign-up">SignUp here</router-link>
    </p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name : 'LoginPage',
    data() {
        return{
        email : '',
        password : ''
        }
    },
    methods:{
    userLogin(){
        let data = {
            email : this.email,
            password : this.password,
        }
        axios({
            url: "http://127.0.0.1:8000/app/user-login",
            method : "post",
            data: data
            }).then((response)=>{
            if(response.status === 200){
                alert(response.data.status)
                localStorage.setItem("userId", response.data.userData.id)
                localStorage.setItem("accountStatus", response.data.userData.accountStatus)
                localStorage.setItem("user", response.data.userData.name)
                this.$router.push({name:"HomePage"})
            }
            
        }).catch((error) => {
            console.log(error)
        })

    } 
    },
    mounted (){
        if(localStorage.getItem("userId")){
            this.$router.push({name:"HomePage"})
        }
},
}
</script>

<style scoped>
</style>
