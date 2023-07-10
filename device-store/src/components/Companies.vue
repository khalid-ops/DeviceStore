<template>
<HeaderBar/>
<div>
    <h2>Companies
    </h2>
    <button class="btn btn-primary" style="margin-left:1200px" @click="toAddform()">Add</button>
    <table class="table table-striped-columns">
        <thead>
        <tr>
            <th>Company</th>
            <th>Contact Person</th>
            <th>Company Status</th>
            <th>To Do</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in companies" :key="item.id">
        <td>{{item.data.company_name}}</td>
        <td>{{item.data.contact_person}}</td>
        <td>{{item.data.status}}</td>
        <td>
            <router-link  class="btn btn-primary btn-sm" style="margin-right:7px" :to="'/update/company/'+item.id">Update</router-link>
            <button  class="btn btn-danger btn-sm" v-on:click="deleteCompany(item.id)">Delete</button>
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
    name : 'CompanyPage',
    data (){
        return{
            companies : [],
        }
    },
    components: {
        HeaderBar
    },
    methods: {
            fetchProducts(){
            let data = {
                userId : localStorage.getItem("userId")
            }
            axios({
                method : "get",
                url : "http://127.0.0.1:8000/app/get-companies",
                params :data,
            }).then((response) =>{
                console.log('products response ', response);
                this.companies = response.data.company_list
            }).catch((error) => {
                console.log(error)
            })
        },
        toAddform(){
            this.$router.push({name:"AddCompany"})
        },
        deleteCompany(Id){
            let data = {
                userId : localStorage.getItem("userId"),
                id : Id
            }
            axios({
                method : "delete",
                url : "http://127.0.0.1:8000/app/delete-company",
                data :data,
            }).then((response) =>{
                alert(response.data.status);
                this.fetchProducts();
            }).catch((error) => {
                console.log(error)
            })
        }
    },
    mounted (){
        if(!localStorage.getItem("userId")){
            this.$router.push({name:"SignUp"})
        }
        this.fetchProducts();

    }

}
</script>

<style>

</style>