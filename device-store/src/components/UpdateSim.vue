<template>
<HeaderBar/>
<h1>Update Sim</h1>
<form class="Add">
    <input type="text" v-model='sim.simName' placeholder="Sim Name" />
    <input type="text" v-model="sim.simStatus" placeholder="Status" />
    <input type="text" v-model="sim.imei" placeholder="IMEI" /> 
    <button type="button" v-on:click="updateSims()">Update sim</button> 
</form>

</template>

<script>
import HeaderBar from './Headers.vue'
import axios from 'axios'

export default {
    name : 'UpdateSim',
    data(){
        return {
            sim :{
            simName:'',
            imei:'',
            simStatus:''
            }
        }
    },
    components :{
        HeaderBar
    },
    methods : {
        updateSims(){
            let data = {
            userId : localStorage.getItem("userId"),
            id : this.$route.params.id,
            simName : this.sim.simName,
            imeiNo : this.sim.imei,
            simStatus : this.sim.simStatus
        }
        axios({
            url: "http://127.0.0.1:8000/app/update-sim",
            method : "post",
            data: data
            }).then((response)=>{
            if(response.status === 200){
                alert(response.data.status)
                this.$router.push({name:"SimsPage"})
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
        let result = await axios.get("http://127.0.0.1:8000/app/get-sim/"+this.$route.params.id)
        let sim_data = result.data.data[0]
        this.sim.simName = sim_data.sim_name
        this.sim.imei = sim_data.imei
        this.sim.simStatus = sim_data.status
    }
}
</script>