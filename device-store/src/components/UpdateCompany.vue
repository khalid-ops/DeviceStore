<template>
<HeaderBar/>
<h1>Update Company</h1>
<form class="Add">
    <input type="text" v-model="company.companyName" placeholder="Company Name" />
    <input type="text" v-model="company.contactPerson" placeholder="Contact Person" />
    <input type="text" v-model="company.companyStatus" placeholder="Status" />
    <button type="button" v-on:click="updateCompany()">Update company</button> 
</form>

</template>

<script>

import axios from 'axios'
import HeaderBar from './Headers.vue'

export default {
    name : 'UpdateCompany',
    data(){
        return {
            company :{
            companyName:'',
            contactPerson:'',
            companyStatus:''
            }
        }
    },
    components :{
        HeaderBar
    },
    methods : {
        updateCompany(){
            let data = {
            userId : localStorage.getItem("userId"),
            id : this.$route.params.id,
            companyName : this.company.companyName,
            contactPerson : this.company.contactPerson,
            companyStatus : this.company.companyStatus
        }
        axios({
            url: "http://127.0.0.1:8000/app/update-company",
            method : "post",
            data: data
            }).then((response)=>{
            if(response.status === 200){
                alert(response.data.status)
                this.$router.push({name:"CompanyPage"})
            }
            
        }).catch((error) => {
            console.log(error)
        })

        }
    },
    async mounted (){
        if(!localStorage.getItem("userId")){
            this.$router.push({name:"SignUp"})
        }
        let result = await axios.get("http://127.0.0.1:8000/app/get-company/"+this.$route.params.id)
        let comp_data = result.data.data[0]
        this.company.companyName = comp_data.company_name
        this.company.contactPerson = comp_data.contact_person
        this.company.companyStatus = comp_data.status
    }
}
</script>