from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .models import UserRegistry, CompanyRegistry, SimRegistry, DeviceRegistry, OrderStatus
import os
from django.http import HttpResponse
from datetime import datetime
import json
import traceback
import pyexcel as pe
# Create your views here.

@api_view(['POST'])
def user_registration(request):

    try:
        user_data = request.data
        if user_data is not None: 
            print(user_data)
            user_email = user_data['email']
            if UserRegistry.objects.filter(email=user_email).exists():
                response_payload = {'status' : "User already exists"}
                return Response(response_payload, status=200)
            
            UserRegistry.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                phone_number=user_data['phoneno'],
                status="active"
            )

            response_payload = {'status' : "Account created successfully!"}
            return Response(response_payload, status=201)
        else:
            response_payload = {'status': "Invalid Data"}
            return Response(response_payload, status=200)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['POST'])
def user_login(request):

    try:
        login_info = request.data
        user_email = login_info['email']
        if login_info is not None:
            if UserRegistry.objects.filter(email=user_email).exists():
                user_data = UserRegistry.objects.get(email=user_email)
                user_pass = user_data.password
                if user_pass == login_info['password']:
                    UserRegistry.objects.filter(email=user_email).update(status="loggedin")
                    data = UserRegistry.objects.get(email=user_email)
                    user_data_list = {
                    'id' : data.id,
                    'name' : data.name,
                    'email' : data.email,
                    'accountStatus' : data.status
                    }
                    response_payload = {
                        'status' : "Login Successful",
                        'userData' : user_data_list
                        }
                    return Response(response_payload, status=200)
                else:
                    response_payload = {
                        'status' : "Login Failed",
                        }
                    return Response(response_payload, 401)
            else:
                response_payload = {
                    'status' : "User doesn't exist!"
                }
                return Response(response_payload, 404)
        else:    
            response_payload = {
                'status' : "Invalid credentials! Try again"
            }
            return Response(response_payload, 401)
    except:
        return Response({'status' : 'system error'}, 500)

@api_view(['GET'])
def user_logout(request):

    try:
        user_id = request.query_params['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            UserRegistry.objects.filter(id=user_id).update(status="loggedout")
            response_payload = {
            'status' : "Logged out Successfully"
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                'status' : "Invalid request!"
            }
            return Response(response_payload,200)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['POST'])
def add_devices(request):
    try:
        unit = request.data
        user_id = unit['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            if unit is not None:
                DeviceRegistry.objects.create(
                    device_name = unit['deviceName'],
                    device_owned_by = UserRegistry.objects.get(id=user_id),
                    device_brand = CompanyRegistry.objects.get(company_name=unit['deviceBrand']),
                    manufactured_in = unit['manufacturedIn'],
                    device_status = unit['status'],
                    )
                
                response_payload = {'status' : "Device added successfully!"}
                return Response(response_payload, status=201)
            else:
                response_payload = {'status': "Invalid Data"}
                return Response(response_payload, status=404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)


@api_view(['GET'])
def get_user_devices(request):
    try:
        user_id = request.query_params['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            devices = DeviceRegistry.objects.filter(device_owned_by=user_id)
            devices = serializers.serialize('json', devices)
            data = json.loads(devices)
            user_devices_list = []
            for d in data:
                user_devices_list.append({
                    'id': d['pk'],
                    'device_name' : d['fields']['device_name'],
                    'device_brand' : CompanyRegistry.objects.get(id=d['fields']['device_brand']).company_name,
                    'manufactured_in' : d['fields']['manufactured_in'],
                    'device_owner' : d['fields']['device_owned_by'],
                    'device_status' : d['fields']['device_status'],
                    'device_sim_name' : d['fields']['device_sim_name']
                })

            response_payload = {
                'status' : "fetched successfully!",
                'devices_list': user_devices_list}
            return Response(response_payload, 200)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    
@api_view(['GET'])
def get_devices(request):
    try:
        user_id = request.query_params['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            devices = DeviceRegistry.objects.all()
            devices = serializers.serialize('json', devices)
            data = json.loads(devices)
            devices_list = []
            for d in data:
                devices_list.append({
                    'id': d['pk'],
                    'device_name' : d['fields']['device_name'],
                    'device_brand' : CompanyRegistry.objects.get(id=d['fields']['device_brand']).company_name,
                    'manufactured_in' : d['fields']['manufactured_in'],
                    'device_owner' : d['fields']['device_owned_by'],
                    'device_status' : d['fields']['device_status'],
                    'device_sim_name' : d['fields']['device_sim_name']
                })

            response_payload = {
                'status' : "fetched successfully!",
                'devices_list': devices_list}
            return Response(response_payload, 200)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['POST'])
def update_devices(request):
    try:
        updation_data = request.data
        if UserRegistry.objects.filter(id=updation_data['userId']).exists():
            if DeviceRegistry.objects.filter(id=updation_data['id']).exists():
                if "deviceName" in updation_data.keys():
                    DeviceRegistry.objects.filter(id=updation_data['id']).update(device_name=updation_data['deviceName'])
                if "deviceOwner" in updation_data.keys():
                    DeviceRegistry.objects.filter(id=updation_data['id']).update(device_owned_by=updation_data['deviceOwner'])
                if "manufacturedIn" in updation_data.keys():
                    DeviceRegistry.objects.filter(id=updation_data['id']).update(manufactured_in=updation_data['manufacturedIn'])
                if "deviceStatus" in updation_data.keys():
                    DeviceRegistry.objects.filter(id=updation_data['id']).update(device_status=updation_data['deviceStatus'])
                response_payload = {'status' : "updated successfully!"}
                return Response(response_payload, status=200)
            else:
                response_payload = {'status': "Invalid device"}
                return Response(response_payload, status=404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=401)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['DELETE'])
def delete_devices(request):
    try:
        data = request.data
        if UserRegistry.objects.filter(id=data['userId']).exists():
            if DeviceRegistry.objects.filter(id=data['id']).exists():
                DeviceRegistry.objects.get(id=data['id']).delete()

                response_payload = {
                    'status' : "deleted successfully"
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'status' : "device not found"
                }
                return Response(response_payload, 404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=401)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['POST'])
def add_company(request):
    try:
        comp_data = request.data
        if comp_data is not None:
            CompanyRegistry.objects.create(
                company_name = comp_data['companyName'],
                contact_person = comp_data['contactPerson'],
                status = comp_data['companyStatus'],
                )
            
            response_payload = {'status' : "Company added successfully!"}
            return Response(response_payload, status=201)
        else:
            response_payload = {'status': "Invalid Data"}
            return Response(response_payload, status=200)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)


@api_view(['GET'])
def get_companies(request):
    try:
        user_id = request.query_params['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            companies = CompanyRegistry.objects.all()
            companies = serializers.serialize('json', companies)
            data = json.loads(companies)
            companies_list = []
            for d in data:
                companies_list.append({
                    'id': d['pk'],
                    'data' : d['fields']
                })

            response_payload = {'status' : "fetched successfully!",
                                'company_list': companies_list}
            return Response(response_payload, status=200)
        else:
            response_payload = {'status': "Invalid User"}
            return Response(response_payload, status=404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['POST'])
def update_company(request):
    try:
        updation_data = request.data
        if UserRegistry.objects.filter(id=updation_data['userId']).exists():
            if CompanyRegistry.objects.filter(id=updation_data['id']).exists():
                if "companyName" in updation_data.keys():
                    CompanyRegistry.objects.filter(id=updation_data['id']).update(company_name=updation_data['companyName'])
                if "contactPerson" in updation_data.keys():
                    CompanyRegistry.objects.filter(id=updation_data['id']).update(contact_person=updation_data['contactPerson'])
                if "companyStatus" in updation_data.keys():
                    CompanyRegistry.objects.filter(id=updation_data['id']).update(status=updation_data['companyStatus'])
                response_payload = {'status' : "updated successfully!"}
                return Response(response_payload, status=200)
            else:
                response_payload = {'status': "Invalid company"}
                return Response(response_payload, status=404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=401)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['DELETE'])
def delete_company(request):
    try:
        data = request.data
        if UserRegistry.objects.filter(id=data['userId']).exists():
            if CompanyRegistry.objects.filter(id=data['id']).exists():
                CompanyRegistry.objects.get(id=data['id']).delete()

                response_payload = {
                    'status' : "deleted successfully"
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'status' : "company not found"
                }
                return Response(response_payload, 404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=401)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    

@api_view(['POST'])
def add_sims(request):
    try:
        unit = request.data
        user_id = unit['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            if unit is not None:
                SimRegistry.objects.create(
                    sim_name = unit['simName'],
                    sim_owned_by = UserRegistry.objects.get(id=user_id),
                    sim_brand = CompanyRegistry.objects.get(company_name=unit['simBrand']),
                    imei = unit['imeiNo'],
                    status = unit['simStatus'],
                    )
                
                response_payload = {'status' : "Sim added successfully!"}
                return Response(response_payload, status=201)
            else:
                response_payload = {'status': "Invalid Data"}
                return Response(response_payload, status=404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)


@api_view(['GET'])
def get_user_sims(request):
    try:
        user_id = request.query_params['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            devices = SimRegistry.objects.filter(sim_owned_by=user_id)
            devices = serializers.serialize('json', devices)
            data = json.loads(devices)
            user_sims_list = []
            for d in data:
                user_sims_list.append({
                    'id': d['pk'],
                    'sim_name' : d['fields']['sim_name'],
                    'sim_brand' : CompanyRegistry.objects.get(id=d['fields']['sim_brand']).company_name,
                    'imei' : d['fields']['imei'],
                    'sim_owner' : d['fields']['sim_owned_by'],
                    'sim_status' : d['fields']['status']
                })

            response_payload = {
                'status' : "fetched successfully!",
                'sims_list': user_sims_list}
            return Response(response_payload, 200)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    
@api_view(['GET'])
def get_sims(request):
    try:
        user_id = request.query_params['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            devices = SimRegistry.objects.all()
            devices = serializers.serialize('json', devices)
            data = json.loads(devices)
            sims_list = []
            for d in data:
                sims_list.append({
                    'id': d['pk'],
                    'sim_name' : d['fields']['sim_name'],
                    'sim_brand' : CompanyRegistry.objects.get(id=d['fields']['sim_brand']).company_name,
                    'imei' : d['fields']['imei'],
                    'sim_owner' : d['fields']['sim_owned_by'],
                    'sim_status' : d['fields']['status']
                })

            response_payload = {
                'status' : "fetched successfully!",
                'sims_list': sims_list}
            return Response(response_payload, 200)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['POST'])
def update_sims(request):
    try:
        updation_data = request.data
        if UserRegistry.objects.filter(id=updation_data['userId']).exists():
            if SimRegistry.objects.filter(id=updation_data['id']).exists():
                if "simName" in updation_data.keys():
                    SimRegistry.objects.filter(id=updation_data['id']).update(sim_name=updation_data['simName'])
                if "simOwner" in updation_data.keys():
                    SimRegistry.objects.filter(id=updation_data['id']).update(sim_owned_by=updation_data['simOwner'])
                if "imeiNo" in updation_data.keys():
                    SimRegistry.objects.filter(id=updation_data['id']).update(imei=updation_data['imeiNo'])
                if "simStatus" in updation_data.keys():
                    SimRegistry.objects.filter(id=updation_data['id']).update(status=updation_data['simStatus'])
                response_payload = {'status' : "updated successfully!"}
                return Response(response_payload, status=200)
            else:
                response_payload = {'status': "Invalid device"}
                return Response(response_payload, status=404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=401)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['DELETE'])
def delete_sims(request):
    try:
        data = request.data
        if UserRegistry.objects.filter(id=data['userId']).exists():
            if SimRegistry.objects.filter(id=data['id']).exists():
                SimRegistry.objects.get(id=data['id']).delete()

                response_payload = {
                    'status' : "deleted successfully"
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'status' : "device not found"
                }
                return Response(response_payload, 404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=401)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    

@api_view(['POST'])
def add_orders(request):
    try:
        order_data = request.data
        user_id = order_data['userId']
        unit = order_data['device']
        if UserRegistry.objects.filter(id=user_id).exists():
            if unit is not None:
                OrderStatus.objects.create(
                    status_desc = unit['status'],
                    order_by = UserRegistry.objects.get(id=user_id),
                    )
                
                response_payload = {'status' : "order added successfully!"}
                return Response(response_payload, status=201)
            else:
                response_payload = {'status': "Invalid Data"}
                return Response(response_payload, status=404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

    
@api_view(['GET'])
def get_user_orders(request):
    try:
        user_id = request.query_params['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            devices = DeviceRegistry.objects.all()
            devices = serializers.serialize('json', devices)
            data = json.loads(devices)
            devices_list = []
            for d in data:
                devices_list.append({
                    'id': d['pk'],
                    'data' : d['fields']
                })

            response_payload = {
                'status' : "fetched successfully!",
                'devices_list': devices_list}
            return Response(response_payload, 200)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['POST'])
def update_orders(request):
    try:
        updation_data = request.data
        if UserRegistry.objects.filter(id=updation_data['userId']).exists():
            if OrderStatus.objects.filter(id=updation_data['id']).exists():
                if "orderStatus" in updation_data.keys():
                    OrderStatus.objects.filter(id=updation_data['id']).update(status_desc=updation_data['orderStatus'])
                response_payload = {'status' : "updated successfully!"}
                return Response(response_payload, status=200)
            else:
                response_payload = {'status': "Invalid device"}
                return Response(response_payload, status=404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=401)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)

@api_view(['DELETE'])
def delete_orders(request):
    try:
        data = request.data
        if UserRegistry.objects.filter(id=data['userId']).exists():
            if DeviceRegistry.objects.filter(id=data['id']).exists():
                DeviceRegistry.objects.get(id=data['id']).delete()

                response_payload = {
                    'status' : "deleted successfully"
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'status' : "device not found"
                }
                return Response(response_payload, 404)
        else:
            response_payload = {'status': "Unauthorized access"}
            return Response(response_payload, status=401)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    

@api_view(['GET'])
def get_company(request, id):
    try:
        companyId = int(id)
        data = CompanyRegistry.objects.filter(id=companyId).values()
        response_payload = {
            'data' : data 
        }
        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    
@api_view(['GET'])
def get_device(request, id):
    try:
        deviceId = int(id)
        data = DeviceRegistry.objects.filter(id=deviceId).values()
        print(data)
        response_payload = {
            'data' : data 
        }
        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    
@api_view(['GET'])
def get_sim(request, id):
    try:
        simId = int(id)
        data = SimRegistry.objects.filter(id=simId).values()
        response_payload = {
            'data' : data 
        }
        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    
@api_view(['GET'])
def get_order(request, id):
    try:
        orderId = int(id)
        data = OrderStatus.objects.filter(id=orderId).values()
        response_payload = {
            'data' : data 
        }
        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    
@api_view(['GET'])
def get_all_products(request):
    try:
        devices_list = []
        sims_list = []
        market_id = 3
        deviceData = DeviceRegistry.objects.filter(device_owned_by=market_id)
        simData = SimRegistry.objects.filter(sim_owned_by=market_id)
        deviceData = json.loads(serializers.serialize('json', deviceData))
        simData = json.loads(serializers.serialize('json', simData))

        for d in deviceData:
            devices_list.append({
                    'id': d['pk'],
                    'device_name' : d['fields']['device_name'],
                    'device_brand' : CompanyRegistry.objects.get(id=d['fields']['device_brand']).company_name,
                    'manufactured_in' : d['fields']['manufactured_in'],
                    'device_owner' : d['fields']['device_owned_by'],
                    'device_status' : d['fields']['device_status']
            })

        for s in simData:
            sims_list.append({
                'id': s['pk'],
                'sim_name' : s['fields']['sim_name'],
                'sim_brand' : CompanyRegistry.objects.get(id=s['fields']['sim_brand']).company_name,
                'imei' : s['fields']['imei'],
                'sim_owner' : s['fields']['sim_owned_by'],
                'sim_status' : s['fields']['status']
            })

        response_payload = {
            'status' : "fetched successfully",
            'devices' : devices_list,
            'sims' : sims_list
        }
        return Response(response_payload, 200)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    

@api_view(['GET'])
def buy_devices(request):
    try:
        user_id = request.query_params['userId']
        device_id = request.query_params['deviceId']
        if DeviceRegistry.objects.filter(id=device_id).exists():
            DeviceRegistry.objects.filter(id=device_id).update(device_owned_by=user_id)
            OrderStatus.objects.create(
                status_desc = "Bought",
                order_by = UserRegistry.objects.get(id=user_id)
            )
            response_payload = {
                'status' : "device bought successfully"
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                'status' : "device not found"
            }
            return Response(response_payload, 404)        
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)
    

@api_view(['POST'])
def install_sims(request):
    try:
        user_id = request.data['userId']
        device_name = request.data['deviceName']
        sim_id = request.data['simId']
        sim_name = request.data['simName']
        print(user_id, sim_id)
        if DeviceRegistry.objects.filter(device_name=device_name).exists():
            user = DeviceRegistry.objects.get(device_name=device_name).device_owned_by
            print("check", user.id)
            if int(user_id) == user.id:
                DeviceRegistry.objects.filter(device_name=device_name).update(device_sim_name=sim_name)
                SimRegistry.objects.filter(id=sim_id).update(sim_owned_by=user_id)
                OrderStatus.objects.create(
                    status_desc = "sim installed",
                    order_by = UserRegistry.objects.get(id=user_id),
                )
                response_payload = {
                    'status' : "Installed sim successfully"
                }
                return Response(response_payload, 200)
            else:
                response_payload = {'status': "device owner mismatch"}
                return Response(response_payload, 200)
        else:
            response_payload = {'status': "device not found"}
            return Response(response_payload, 404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)



@api_view(['GET'])
def get_company_customers(request):
    try:
        company_details = CompanyRegistry.objects.all().values_list('id', 'company_name')[::1]
        customers_list = []
        for item in company_details:
            dev_data = DeviceRegistry.objects.filter(device_brand=item[0]).exclude(device_owned_by=3).values_list('device_brand','device_owned_by')[::1]
            sim_data = SimRegistry.objects.filter(sim_brand=item[0]).exclude(sim_owned_by=3).values_list('sim_brand','sim_owned_by')[::1]
            if len(dev_data) > 0:
                for i in dev_data:
                    customers_list.append({
                        'Company_name': CompanyRegistry.objects.get(pk=i[0]).company_name,
                        'Customer_name' : UserRegistry.objects.get(pk=i[1]).name,
                        'category' : "Device"
                    })
            if len(sim_data) > 0:
                for j in sim_data:
                    customers_list.append({
                        'Company_name': CompanyRegistry.objects.get(pk=j[0]).company_name,
                        'Customer_name' : UserRegistry.objects.get(pk=j[1]).name,
                        'category' : "Sim"
                    })

        response_payload = {
            'customers_data' : customers_list
        }
        return Response(response_payload, 200)

    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)


def generate_report(user_id):
    try:
        user_id = user_id
        device_companies = []
        temp = []
        comps_id = CompanyRegistry.objects.all().values_list('id', flat=True)[::1]
        for ids in comps_id:
            data = DeviceRegistry.objects.filter(device_brand=ids).values()[::1]
            if len(data) > 0:
                temp.append(data)
        for t in temp:
            device_companies.append({
                "Company" : CompanyRegistry.objects.get(id=t[0]['device_brand_id']).company_name,
                "Owner" : UserRegistry.objects.get(id=t[0]['device_owned_by_id']).name,
                "Device" : t[0]['device_name']
            })
        
        pe.save_as(records=device_companies, dest_file_name="device_company_data.xlsx")
        return True
    except:
        traceback.print_exc()
        return False

@api_view(['GET'])
def download_report(request):
    try:
        user_id = request.query_params['userId']
        res = generate_report(user_id)
        if res:
            p = os.path.dirname(os.path.abspath("device_company_data.xlsx"))
            p = p+"/device_company_data.xlsx"
            with open(p, "rb") as f:
                data = f.read()

            response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Devices_Report.xlsx'

            os.remove(p)
            return response
        else:
            return Response({'status' : "Report not found"}, 404)
    except:
        traceback.print_exc()
        return Response({'status' : 'system error'}, 500)