import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './components/Home.vue';
import SignUp from './components/Signup.vue';
import LoginPage from './components/Login.vue';
import DevicesPage from './components/Devices.vue'
import SimsPage from './components/Sims.vue';
import CompanyPage from './components/Companies.vue';
import AddCompany from './components/AddCompany.vue';
import AddDevice from './components/AddDevice.vue';
import AddSim from './components/AddSim.vue';
import UpdateCompany from './components/UpdateCompany.vue';
import UpdateDevice from './components/UpdateDevice.vue';
import UpdateSim from './components/UpdateSim.vue';
import InstallSim from './components/InstallSim.vue';
import DisplayCustomers from './components/DisplayCustomers.vue';


const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/devices',
    name: 'DevicesPage',
    component: DevicesPage
  },
  {
    path: '/sims',
    name: 'SimsPage',
    component: SimsPage
  },
  {
    path: '/companies',
    name: 'CompanyPage',
    component: CompanyPage
  },
  {
    path: '/add/company',
    name: 'AddCompany',
    component: AddCompany
  },
  {
    path: '/add/device',
    name: 'AddDevice',
    component: AddDevice
  },
  {
    path: '/add/sim',
    name: 'AddSim',
    component: AddSim
  },
  {
    path: '/update/company/:id',
    name: 'UpdateCompany',
    component: UpdateCompany
  },
  {
    path: '/update/device/:id',
    name: 'UpdateDevice',
    component: UpdateDevice
  },
  {
    path: '/update/sim/:id',
    name: 'UpdateSim',
    component: UpdateSim
  },
  {
    path: '/install/sim/:id',
    name: 'InstallSim',
    component: InstallSim
  },
  {
    path: '/display',
    name: 'DisplayCustomers',
    component: DisplayCustomers
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// router.beforeEach((to, from, next) => {
//   if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
//     next({ name: 'LogIn', query: { to: to.path } });
//   } else {
//     next()
//   }
// })

export default router