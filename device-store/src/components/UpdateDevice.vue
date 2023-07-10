<template>
<HeaderBar/>
<h1>Update Device</h1>
<form class="Add">
    <input type="text" name="Device Name" v-model='device.deviceName' placeholder="Device Name" />
    <input type="text" name="Status" v-model="device.status" placeholder="Status" />
    <input type="text" name="ManufacturedIn" v-model="device.manufacturedIn" placeholder="Manufactured Country" /> 
    <button type="button" v-on:click="updateDevices()">Update device</button> 
</form>

</template>

<script>
import HeaderBar from './Headers.vue'
import axios from 'axios'

export default {
    name : 'UpdateDevice',
    data(){
        return {
            device :{
            deviceName:'',
            manufacturedIn:'',
            status:'',
            }
        }
    },
    components :{
        HeaderBar
    },
    methods : {
        updateDevices(){
            console.log(this.device.status, this.device.manufacturedIn)
            let data = {
            userId : localStorage.getItem("userId"),
            id : this.$route.params.id,
            deviceName : this.device.deviceName,
            manufacturedIn : this.device.manufacturedIn,
            deviceStatus : this.device.status
        }
        axios({
            url: "http://127.0.0.1:8000/app/update-device",
            method : "post",
            data: data,
            }).then((response)=>{
            if(response.status === 200){
                alert(response.data.status)
                this.$router.push({name:"DevicesPage"})
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
        let result = await axios.get("http://127.0.0.1:8000/app/get-device/"+this.$route.params.id)
        let dev_data = result.data.data[0]
        this.device.deviceName = dev_data.device_name
        this.device.manufacturedIn = dev_data.manufactured_in
        this.device.status = dev_data.device_status
    }
}
</script>