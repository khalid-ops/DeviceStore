<template>
<HeaderBar/>
<div>
    <h2>Company and Customers</h2>
    <button class="btn btn-primary" style="margin-left:1200px" v-on:click="getReport()">Devices Report</button>
    <table class="table table-striped-columns">
        <thead>
        <tr>
            <th>Company</th>
            <th>Customer</th>
            <th>Category</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in customers" :key="item.id">
        <td>{{item.Company_name}}</td>
        <td>{{item.Customer_name}}</td>
        <td>{{item.category}}</td>
        </tr>
        </tbody>
    </table>
</div>

</template>

<script>

import HeaderBar from './Headers.vue'
import axios from 'axios'

export default {
    name : 'DisplayCustomers',
    data (){
        return{
            customers : [],
        }
    },
    components: {
        HeaderBar
    },
    methods: {
            fetchList(){
            let data = {
                userId : localStorage.getItem("userId")
            }
            axios({
                method : "get",
                url : "http://127.0.0.1:8000/app/get/comp-customers",
                params :data,
            }).then((response) =>{
                console.log('products response ', response);
                this.customers = response.data.customers_data
            }).catch((error) => {
                console.log(error)
            })
        },
        getReport(){
            let data = {
                userId : localStorage.getItem("userId")
            }
            axios({
                method : "get",
                url : "http://127.0.0.1:8000/app/rep/download",
                params :data,
                responseType: 'blob', 
                headers: { 
                    "Content-Type" : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                }
            }).then((response) =>{
                // console.log(data);
                const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.setAttribute('download', 'Device_company_report.xlsx');
                document.body.appendChild(link);
                link.click();
                link.remove();
            })
            .catch((error) => {
                console.log(error)
            })
        }
    },
    mounted (){
        if(!localStorage.getItem("userId")){
            this.$router.push({name:"SignUp"})
        }
        this.fetchList();

    }

}
</script>

<style>

</style>