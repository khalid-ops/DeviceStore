<template>
<HeaderBar/>
<div>
    <h2>Sims
    </h2>
    <button class="btn btn-primary" style="margin-left:1200px" v-show="showAddSims" @click="toAddform()">Add</button>
    <table class="table table-striped-columns">
        <thead>
        <tr>
            <th>Sim</th>
            <th>Sim Brand</th>
            <th>IMEI</th>
            <th>Sim status</th>
            <th>To Do</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in sims" :key="item.id">
        <td>{{item.sim_name}}</td>
        <td>{{item.sim_brand}}</td>
        <td>{{item.imei}}</td>
        <td>{{item.sim_status}}</td>
        <td>
            <router-link  class="btn btn-primary btn-sm" style="margin-right:7px" :to="'/update/sim/'+item.id">Update</router-link>
            <button  class="btn btn-danger btn-sm" v-on:click="deleteSim(item.id)">Delete</button>
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
    name : 'SimsPage',
    data (){
        return{
            sims : [],
            showAddSims:false
        }
    },
    components: {
        HeaderBar
    },
    methods: {
            fetchSims(){
            let data = {
                userId : localStorage.getItem("userId")
            }
            axios({
                method : "get",
                url : "http://127.0.0.1:8000/app/get/user-sims",
                params :data,
            }).then((response) =>{
                console.log('products response ', response);
                this.sims = response.data.sims_list
            }).catch((error) => {
                console.log(error)
            })
        },
        toAddform(){
            this.$router.push({name:"AddSim"})
        },
        deleteSim(Id){
            let data = {
                userId : localStorage.getItem("userId"),
                id : Id
            }
            axios({
                method : "delete",
                url : "http://127.0.0.1:8000/app/delete-sim",
                data :data,
            }).then((response) =>{
                alert(response.data.status);
                this.fetchSims();
            }).catch((error) => {
                console.log(error)
            })
        }
    },
    mounted (){
        if(!localStorage.getItem("userId")){
            this.$router.push({name:"SignUp"})
        }
        this.fetchSims();
        if(localStorage.getItem("userId")==="3"){
            this.showAddSims = true;
        }
    }

}
</script>