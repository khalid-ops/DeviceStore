<template>
<h1>Sign Up For electronic store</h1>
<div class="register">
    <input type="text" v-model='name' placeholder="Name" />
    <input type="text" v-model='email' placeholder="Email" />
    <input type="text" v-model="password" placeholder="Password" />
    <input type="text" v-model="phone" placeholder="Phone No" />
    <button v-on:click="submitForm()">Sign up </button>
    <p>
    <router-link to="/login">Login here</router-link>
    </p>
</div>
</template>

<script>
import axios from 'axios'

export default {
    name : 'SignUp',
    data (){
        return {
            name : '', 
            email : '',
            password : ''

        }
    },
    methods:{
        submitForm(){
            let data = {
                name : this.name,
                email : this.email,
                password : this.password,
                phoneno : this.phone,
            }
            axios({
                url: "http://127.0.0.1:8000/app/user-register",
                method : "post",
                data: data
                }).then((response)=>{
                if(response.status === 201){
                    alert(response.data.status)
                    this.$router.push({name:"HomePage"})
                }
                
            }).catch((error) => {
                console.log(error)
            })
            
        }
    },
    mounted(){
        if(localStorage.getItem("userId")){
            this.$router.push({name:"HomePage"})
        }

    }
}
</script>

<style scoped>
</style>
