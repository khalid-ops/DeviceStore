<template>
<HeaderBar/>
<h1>Install Sim</h1>
<form class="Add">
    <input type="text" v-model='deviceName' placeholder="Enter your Device Name" />
    <input type="text" v-model="sim.simName" placeholder="Sim Name" />
    <button type="button" v-on:click="InstallSims()">Install sim</button> 
</form>

</template>

<script>
import axios from 'axios'
import HeaderBar from './Headers.vue'

export default {
    name : 'InstallSim',
    data(){
        return {
            sim :{
            simName:'',
            },
            deviceName : '' 
        }
    },
    components :{
        HeaderBar
    },
    methods : {
        InstallSims(){
            let data = {
            userId : localStorage.getItem("userId"),
            simId : this.$route.params.id,
            simName : this.sim.simName,
            deviceName : this.deviceName
        }
        axios({
            url: "http://127.0.0.1:8000/app/install-sim",
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
    }
}
</script>