from django.db import models

# Create your models here.

class UserRegistry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    
class OrderStatus(models.Model):
    status_desc = models.TextField(max_length=300)
    order_by = models.ForeignKey(UserRegistry, on_delete=models.CASCADE)

class CompanyRegistry(models.Model):
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

class SimRegistry(models.Model):
    sim_owned_by = models.ForeignKey(UserRegistry, on_delete=models.CASCADE)
    imei = models.CharField(max_length=15)
    sim_name = models.CharField(max_length=100)
    sim_brand = models.ForeignKey(CompanyRegistry, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

class DeviceRegistry(models.Model):
    device_name = models.CharField(max_length=100)
    device_owned_by = models.ForeignKey(UserRegistry, on_delete=models.CASCADE)
    device_brand = models.ForeignKey(CompanyRegistry, on_delete=models.CASCADE)
    manufactured_in = models.CharField(max_length=100)
    device_status = models.CharField(max_length=50)
    device_sim_name = models.CharField(max_length=100, default="No sim")