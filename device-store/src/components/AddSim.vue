<template>
<HeaderBar/>
<h1>Add Sim</h1>
<form class="Add">
    <input type="text" v-model='simName' placeholder="Sim Name" />
    <input type="text" v-model="simBrand" placeholder="Sim Brand" />
    <input type="text" v-model="simStatus" placeholder="Status" />
    <input type="text" v-model="imEi" placeholder="IMEI" />
    <button type="button" v-on:click="addSims()">Add Sim</button> 
</form>

</template>

<script>
import axios from 'axios'
import HeaderBar from './Headers.vue'
export default {
    name : 'AddSim',
    data(){
        return {
            simName:'',
            simBrand:'',
            simStatus:'',
            imEi : ''
        }
    },
    components :{
        HeaderBar
    },
    methods : {
        addSims(){
        let data = {
            userId : localStorage.getItem("userId"),
            simName : this.simName,
            imeiNo : this.imEi,
            simBrand : this.simBrand,
            simStatus : this.simStatus
        }
        axios({
            url: "http://127.0.0.1:8000/app/add-sims",
            method : "post",
            data: data
            }).then((response)=>{
            if(response.status === 201){
                console.log(response)
                alert(response.data.status)
                this.$router.push({name:"SimsPage"})
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