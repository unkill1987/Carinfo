from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from tkinter.messagebox import showerror, showinfo
from tkinter import *
# Create your views here.
from app.models import Manufacture, Government, Repairshop, Insurance
from carinfo import settings

def search(request):
    try:
        sn = str(request.POST['sn'])
        url = ("http://localhost:8001/history/%s" %sn)
        res = requests.get(url)
        history = res.json()
        init = history[0]
        history.pop(0)
        history.reverse()

        return render(request, 'app/search.html', {'history':history, 'init':init})
    except Exception as e:
        print(e)
        return redirect('index')

def index(request):
    return render(request, 'app/index.html', {})



def manufacture(request):
    if request.method == 'GET':
        return render(request, 'app/manufacture.html', {})
    else:
        user_id = request.POST.get('user_id', False)
        passwd = request.POST.get('passwd', False)

        result_dict = {}
        try:
            Manufacture.objects.get(user_id=user_id, passwd=passwd)
            company = Manufacture.objects.filter(user_id=user_id).values('company')[0]['company']
            result_dict['result'] = 'success'
            request.session['user_id'] = user_id
            request.session['company'] = company

        except Manufacture.DoesNotExist:
            result_dict['result'] = 'fail'
        return JsonResponse(result_dict)


def manufacture_record(request):
    try:
        user_id = request.session['user_id']
        company = request.session['company']
        templates = ''
        if (len(company) == 0):
            templates = 'app/manufacture.html'
        else:
            templates = 'app/manufacture_record.html'

        return render(request, templates, {'user_id': user_id})
    except:
        return redirect('manufacture')


def manufacture_success(request):
    return render(request, 'app/manufacture_success.html', {})


def government(request):
    if request.method == 'GET':
        return render(request, 'app/government.html', {})
    else:
        user_id = request.POST.get('user_id', False)
        passwd = request.POST.get('passwd', False)

        result_dict = {}
        try:
            Government.objects.get(user_id=user_id, passwd=passwd)
            government = Government.objects.filter(user_id=user_id).values('government')[0]['government']
            result_dict['result'] = 'success'
            request.session['user_id'] = user_id
            request.session['government'] = government

        except Government.DoesNotExist:
            result_dict['result'] = 'fail'
        return JsonResponse(result_dict)


def government_record(request):
    try:
        user_id = request.session['user_id']
        government = request.session['government']
        templates = ''
        if len(government) == 0:
            templates = 'app/government.html'
        else:
            templates = 'app/government_record.html'

        return render(request, templates, {'user_id': user_id})
    except Exception as e:
        print(e)
        return redirect('government')


def repairshop(request):
    if request.method == 'GET':
        return render(request, 'app/repairshop.html', {})
    else:
        user_id = request.POST.get('user_id', False)
        passwd = request.POST.get('passwd', False)

        result_dict = {}
        try:
            Repairshop.objects.get(user_id=user_id, passwd=passwd)
            repairshop = Repairshop.objects.filter(user_id=user_id).values('repairshop')[0]['repairshop']
            result_dict['result'] = 'success'
            request.session['user_id'] = user_id
            request.session['repairshop'] = repairshop

        except Repairshop.DoesNotExist:
            result_dict['result'] = 'fail'
        return JsonResponse(result_dict)


def repairshop_record(request):
    try:
        user_id = request.session['user_id']
        repairshop = request.session['repairshop']
        templates = ''
        if len(repairshop) == 0:
            templates = 'app/repairshop.html'
        else:
            templates = 'app/repairshop_record.html'

        return render(request, templates, {'user_id': user_id})
    except Exception as e:
        print(e)
        return redirect('repairshop')


def insurance(request):
    if request.method == 'GET':
        return render(request, 'app/insurance.html', {})
    else:
        user_id = request.POST.get('user_id', False)
        passwd = request.POST.get('passwd', False)

        result_dict = {}
        try:
            Insurance.objects.get(user_id=user_id, passwd=passwd)
            insurance = Insurance.objects.filter(user_id=user_id).values('insurance')[0]['insurance']
            result_dict['result'] = 'success'
            request.session['user_id'] = user_id
            request.session['insurance'] = insurance

        except Insurance.DoesNotExist:
            result_dict['result'] = 'fail'
        return JsonResponse(result_dict)


def insurance_record(request):
    try:
        user_id = request.session['user_id']
        insurance = request.session['insurance']
        templates = ''
        print(insurance)
        if len(insurance) == 0:
            templates = 'app/insurance.html'
        else:
            templates = 'app/insurance_record.html'

        return render(request, templates, {'user_id': user_id})
    except:
        return redirect('insurance')


def recordcarinfo(request):

    sn = request.POST['sn']
    manufacture = request.session['company']
    factory = request.POST['factory']
    name = request.POST['name']
    type = request.POST['type']
    volume = request.POST['volume']
    fuel = request.POST['fuel']

    url = 'http://localhost:8001/init_car/' + sn + '-' + manufacture + '-' + factory + '-' + name + '-' + type + '-' + volume + '-' + fuel
    response = requests.get(url)
    res = response.text

    result_dict={}
    if (res == "The contract already exists"):
        result_dict['result'] = 'Already exists Vehicle'
    else:
        result_dict['result'] = 'success'
    return JsonResponse(result_dict)



def recordcarchange(request):

    government = request.session['government']
    sn = request.POST['sn']
    plate = request.POST['plate']
    owner = request.POST['owner']
    tradehistory = request.POST['tradehistory']
    price = request.POST['price']

    url = 'http://localhost:8001/change_car/' + sn + '-' + government + '-' + plate + '-' + owner + '-' + tradehistory + '-' + price
    response = requests.get(url)
    res = response.text

    result_dict = {}
    if (res == "Could not found contract_id"):
        result_dict['result'] = 'Check S/N of Vehicle'
    else:
        result_dict['result'] = 'success'
    return JsonResponse(result_dict)


def recordcarrepair(request):
    shop = request.session['repairshop']
    sn = request.POST['sn']
    repair = request.POST['repair']
    repairprice = request.POST['repairprice']

    url = 'http://localhost:8001/repair_car/' + sn + '-' + repair + '-' + repairprice + '-' + shop
    response = requests.get(url)
    res = response.text

    result_dict = {}
    if (res == "Could not found contract_id"):
        result_dict['result'] = 'Check S/N of Vehicle'
    else:
        result_dict['result'] = 'success'
    return JsonResponse(result_dict)



def recordcaraccident(request):
    insurance = request.session['insurance']
    sn = request.POST['sn']
    accident = request.POST['accident']
    costs = request.POST['costs']

    url = 'http://localhost:8001/accident_car/' + sn + '-' + accident + '-' + costs + '-' + insurance
    response = requests.get(url)
    res = response.text

    result_dict = {}
    if (res == "Could not found contract_id"):
        result_dict['result'] = 'Check S/N of Vehicle'
    else:
        result_dict['result'] = 'success'
    return JsonResponse(result_dict)


def logout(request):

    try:
        try:
            if len(str(request.session['insurance'])) != 0:
                del request.session['insurance']
                del request.session['user_id']
        except:
            pass
        try:
            if len(str(request.session['repairshop'])) != 0:
                del request.session['repairshop']
                del request.session['user_id']
        except:
            pass
        try:
            if len(str(request.session['government'])) != 0:
                del request.session['government']
                del request.session['user_id']
        except:
            pass
        try:
            if len(str(request.session['company'])) != 0:
                del request.session['company']
                del request.session['user_id']
        except:
            pass

        return redirect('index')

    except Exception as e:
        print(e)
        return render(request, 'app/index.html', {})
