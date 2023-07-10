<template>
<HeaderBar/>
<h1>Add Device</h1>
<form class="Add">
    <input type="text" v-model='deviceName' placeholder="Device Name" />
    <input type="text" v-model="deviceBrand" placeholder="Device Brand" />
    <input type="text" v-model="deviceStatus" placeholder="Status" />
    <input type="text" v-model="deviceManufacturedIn" placeholder="Manufactured Country" />
    <button type="button" v-on:click="addDevices()">Add device</button> 
</form>

</template>

<script>
import axios from 'axios'
import HeaderBar from './Headers.vue'

export default {
    name : 'AddDevice',
    data(){
        return {
            deviceName:'',
            deviceBrand:'',
            deviceStatus:'',
            deviceManufacturedIn : ''
        }
    },
    components :{
        HeaderBar
    },
    methods : {
        addDevices(){
        let data = {
            userId : localStorage.getItem("userId"),
            deviceName : this.deviceName,
            manufacturedIn : this.deviceManufacturedIn,
            deviceBrand : this.deviceBrand,
            status : this.deviceStatus
        }
        axios({
            url: "http://127.0.0.1:8000/app/add-device",
            method : "post",
            data: data
            }).then((response)=>{
            if(response.status === 201){
                console.log(response)
                alert(response.data.status)
                this.$router.push({name:"DevicesPage"})
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