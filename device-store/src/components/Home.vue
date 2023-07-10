<template>
<HeaderBar/>
<h1>Welcome {{userName}} To Store!</h1>
<h2 style="text-align:left;margin-left:20px">Devices</h2>
<div>
    <div class="row">
    <div class="col-sm-3 mb-3" v-for="item in deviceList" :key="item.id">
    <div class="card" style="width: 18rem;" >
        <div class="card-body">
            <h5 class="card-title">{{item.device_name}}</h5>
            <ul class="list-group list-group-flush">
            <li class="list-group-item">Brand : {{item.device_brand}}</li>
            <li class="list-group-item">Manufactured-in : {{item.manufactured_in}}</li>
            <li class="list-group-item">Status : {{item.device_status}}</li>
            </ul>
            <button type="button" class="btn btn-primary btn-sm" v-on:click="buyDevice(item.id)">Buy</button>
        </div>
    </div>
    </div>
    </div>
</div>
<h2 style="text-align:left;margin-left:20px">Sims</h2>
<div>
    <div class="row">
    <div class="col-sm-3 mb-3" v-for="item in simList" :key="item.id">
    <div class="card" style="width: 18rem;" >
        <div class="card-body">
            <h5 class="card-title">{{item.sim_name}}</h5>
            <ul class="list-group list-group-flush">
            <li class="list-group-item">Brand : {{item.sim_brand}}</li>
            <li class="list-group-item">IMEI : {{item.imei}}</li>
            <li class="list-group-item">Status : {{item.sim_status}}</li>
            </ul>
            <router-link class="btn btn-success btn-sm" :to="'/install/sim/'+item.id">Install</router-link>
        </div>
    </div>
    </div>
    </div>
</div>
</template>

<script>

import HeaderBar from './Headers.vue'
import axios from 'axios'
export default {
    name : 'HomePage',
    data (){
        return {
        userName : '',
        deviceList : [],
        simList : []
        }
    },
    components: {
        HeaderBar
    },
    methods : {
        fetchHomeProducts(){
            let data = {
                userId : localStorage.getItem("userId")
            }
            axios({
                method : "get",
                url : "http://127.0.0.1:8000/app/get-products",
                params :data,
            }).then((response) =>{
                console.log('products response ', response);
                this.deviceList = response.data.devices
                this.simList = response.data.sims
            }).catch((error) => {
                console.log(error)
            })
        },
        buyDevice(id){

            let data = {
                userId : localStorage.getItem("userId"),
                deviceId : id
            }
            axios({
                method : "get",
                url : "http://127.0.0.1:8000/app/buy-device",
                params :data,
            }).then((response) =>{
                console.log(response);
                alert(response.data.status);
                this.$router.push({name:"DevicesPage"})
            }).catch((error) => {
                console.log(error)
            })

        },
        installSim(){

        }
    },
    mounted (){
        if(localStorage.getItem("user")){
            this.userName = localStorage.getItem("user")
        }
        if(!localStorage.getItem("userId")){
            this.userName = "user"
            this.$router.push({name:"SignUp"})
        }

        this.fetchHomeProducts();

    }
}
</script>