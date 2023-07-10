from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('user-register',  views.user_registration),
    path('user-login',  views.user_login),
    path('user-logout', views.user_logout),
    path('get-companies', views.get_companies),
    path('update-company', views.update_company),
    path('add-company', views.add_company),
    path('delete-company', views.delete_company),
    path('get-devices', views.get_devices),
    path('get/user-devices', views.get_user_devices),
    path('update-device', views.update_devices),
    path('add-device', views.add_devices),
    path('delete-device', views.delete_devices),
    path('get-sims', views.get_sims),
    path('get/user-sims', views.get_user_sims),
    path('update-sim', views.update_sims),
    path('add-sims', views.add_sims),
    path('delete-sim', views.delete_sims),
    path('get/user-order', views.get_user_orders),
    path('update-order', views.update_orders),
    path('add-order', views.add_orders),
    path('delete-order', views.delete_orders),
    path('get-company/<int:id>', views.get_company),
    path('get-device/<int:id>', views.get_device),
    path('get-sim/<int:id>', views.get_sim),
    path('get-order/<int:id>', views.get_order),
    path('get-products', views.get_all_products),
    path('buy-device', views.buy_devices),
    path('install-sim', views.install_sims),
    path('get/comp-customers', views.get_company_customers),
    path("rep/download", views.download_report)

]