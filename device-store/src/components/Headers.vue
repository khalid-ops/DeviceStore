<template>
    <div class="nav">
        <router-link to="/">Home</router-link>
        <router-link to="/devices">Devices</router-link>
        <router-link to="/sims">Sims</router-link>
        <router-link to="/companies" v-show="showCompaniesCustomers">Companies</router-link>
        <router-link to="/display" v-show="showCompaniesCustomers">Customers</router-link>
        <button v-on:click="logout()">Logout</button>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name : 'HeaderBar',
    data(){
        return{
            showCompaniesCustomers:false
        }
    },
    methods : {
        logout() {
            let data = {
            userId : localStorage.getItem('userId')
        }
        axios({
            url: "http://127.0.0.1:8000/app/user-logout",
            method : "get",
            params : data
            }).then((response)=>{
            if(response.status === 200){
                alert(response.data.status)
                localStorage.removeItem("userId")
                localStorage.removeItem("accountStatus")
                this.$router.push({name:"LoginPage"})
            }
            
        }).catch((error) => {
            console.log(error)
        })

        } // TODO: Implement Logout functionality.
    },
    mounted(){
        if(localStorage.getItem("userId") === "3"){
            this.showCompaniesCustomers = true
        }
    }
}
</script>
