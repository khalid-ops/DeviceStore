<template>
<HeaderBar/>
<div>
    <h2>Devices
    </h2>
    <button class="btn btn-primary" style="margin-left:1200px" @click="toAddform()">Add</button>
    <table class="table table-striped-columns">
        <thead>
        <tr>
            <th>Device</th>
            <th>Device Brand</th>
            <th>Manufactured Country</th>
            <th>Device status</th>
            <th>Device Sim</th>
            <th>To Do</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in devices" :key="item.id">
        <td>{{item.device_name}}</td>
        <td>{{item.device_brand}}</td>
        <td>{{item.manufactured_in}}</td>
        <td>{{item.device_status}}</td>
        <td>{{item.device_sim_name}}</td>
        <td>
            <router-link  class="btn btn-primary btn-sm" style="margin-right:7px" :to="'/update/device/'+item.id">Update</router-link>
            <button  class="btn btn-danger btn-sm" v-on:click="deleteDevice(item.id)">Delete</button>
        </td>
        </tr>
        </tbody>
    </table>
</div>

</template>

<script>

import HeaderBar from './Headers.vue'
import axios from 'axios'

export default {
    name : 'DevicesPage',
    data (){
        return{
            devices : [],
        }
    },
    components: {
        HeaderBar
    },
    methods: {
            fetchDevices(){
            let data = {
                userId : localStorage.getItem("userId")
            }
            axios({
                method : "get",
                url : "http://127.0.0.1:8000/app/get/user-devices",
                params :data,
            }).then((response) =>{
                console.log('products response ', response);
                this.devices = response.data.devices_list
            }).catch((error) => {
                console.log(error)
            })
        },
        toAddform(){
            this.$router.push({name:"AddDevice"})
        },
        deleteDevice(Id){
            let data = {
                userId : localStorage.getItem("userId"),
                id : Id
            }
            axios({
                method : "delete",
                url : "http://127.0.0.1:8000/app/delete-device",
                data :data,
            }).then((response) =>{
                alert(response.data.status);
                this.fetchDevices();
            }).catch((error) => {
                console.log(error)
            })
        }
    },
    mounted (){
        if(!localStorage.getItem("userId")){
            this.$router.push({name:"SignUp"})
        }
        this.fetchDevices();

    }

}
</script>