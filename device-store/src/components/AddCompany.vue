<template>
<HeaderBar/>
<h1>Add Company</h1>
<form class="Add">
    <input type="text" v-model='companyName' placeholder="Company Name" />
    <input type="text" v-model="contactPerson" placeholder="Contact Person" />
    <input type="text" v-model="companyStatus" placeholder="Status" />
    <button type="button" v-on:click="addCompany()">Add company</button> 
</form>

</template>

<script>
import axios from 'axios'
import HeaderBar from './Headers.vue'
export default {
    name : 'AddCompany',
    data(){
        return {
            companyName:'',
            contactPerson:'',
            companyStatus:''
        }
    },
    components :{
        HeaderBar
    },
    methods : {
        addCompany(){
        let data = {
            userId : localStorage.getItem("userId"),
            companyName : this.companyName,
            contactPerson : this.contactPerson,
            companyStatus : this.companyStatus
        }
        axios({
            url: "http://127.0.0.1:8000/app/add-company",
            method : "post",
            data: data
            }).then((response)=>{
            if(response.status === 201){
                alert(response.data.status)
                // this.$router.push({name:"HomePage"})
            }
            
        }).catch((error) => {
            console.log(error)
        })
        }
    },
    mounted (){
        if(!localStorage.getItem("userId")){
            this.$router.push({name:"SignUp"})
        }
    }
}
</script>