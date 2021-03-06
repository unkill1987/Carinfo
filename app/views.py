import os

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import requests
from app.models import Manufacture, Government, Repairshop, Insurance, Sellcar, Market, Notice
from carinfo import settings
import pyotp
import time
import json


def notice(request):
    try:
        all = Notice.objects.all().order_by('-id')
        total_len = len(all)
        page = request.GET.get('page')
        paginator = Paginator(all, 10)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 3 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        notice = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

        return render(request, 'app/notice.html', notice)

    except Exception as e:
        print(e)
        return redirect('notice')


def mypage(request):
    return render(request, 'app/mypage.html', {})


def makeotp(request):
    if request.method == 'GET':
        return render(request, 'app/marketlogin.html', {})
    else:
        try:
            user_id = request.session['user_id']
            otpkey = pyotp.random_base32()
            otpsave = Market.objects.get(user_id=user_id)
            if Market.objects.filter(user_id=user_id).values('otp')[0]['otp'] == '':
                otpsave.otp = otpkey
                otpsave.save()
                data = pyotp.totp.TOTP(otpkey).provisioning_uri(user_id, issuer_name="Vehicle App")

                return render(request, 'app/mypage.html', {'otpkey': otpkey, 'user_id': user_id, 'data': data})
            else:
                message = "Already Issued"
                return render(request, 'app/mypage.html', {'message': message})
        except Exception as e:
            print(e)
            return redirect('market')


def marketform(request):
    try:
        buyer = request.session['user_id']
        buyerrrn = Market.objects.filter(user_id=buyer).values('residentnum')[0]['residentnum'][:8] + '*' * 6
        sn = request.POST['sn']
        url = ("http://45.32.103.121:8001/history/%s" % sn)
        res = requests.post(url)
        history = res.json()
        init = history[0]
        info = Sellcar.objects.filter(serialnumber=sn)
        seller = info.values('owner')[0]['owner']
        sellerrrn = Market.objects.filter(user_id=seller).values('residentnum')[0]['residentnum'][:8] + '*' * 6
        return render(request, 'app/marketform.html',
                      {'init': init, 'info': info, 'buyer': buyer, 'sn': sn, 'buyerrrn': buyerrrn,
                       'sellerrrn': sellerrrn})
    except Exception as e:
        print(e)
        return redirect('market')


def marketdetails(request):
    try:

        sn = request.POST['serial']
        url = ("http://45.32.103.121:8001/history/%s" % sn)
        res = requests.post(url)
        history = res.json()
        init = history[0]
        history.pop(0)
        history.reverse()

        return render(request, 'app/marketdetails.html', {'history': history, 'init': init})
    except Exception as e:
        print(e)
        return redirect('market')


def marketsearch(request):
    try:
        search = request.POST['vehiclesearch']

        all = Sellcar.objects.filter(modelname=search).order_by('-id')
        total_len = len(all)
        page = request.GET.get('page')
        paginator = Paginator(all, 10)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 3 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        allcars = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

        return render(request, 'app/marketsearch.html', allcars)

    except Exception as e:
        print(e)
        return redirect('marketlogin')


def allvehicles(request):
    try:
        url = ("http://45.32.103.121:8001/all")
        res = requests.post(url)
        all = res.json()
        total_len = len(all)
        page = request.GET.get('page')
        paginator = Paginator(all, 100)

        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        index = lines.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 3 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        allcars = {'result_list': lines, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

        return render(request, 'app/allvehicles.html', allcars)
    except Exception as e:
        print(e)
        return ('index')


def search(request):
    try:
        sn = str(request.POST['sn'])
        url = ("http://45.32.103.121:8001/history/%s" % sn)
        res = requests.post(url)
        history = res.json()
        if len(history) == 0:
            message = "Invalid S/N"
            return render(request, 'app/index.html', {'message': message})
        else:

            init = history[0]
            history.pop(0)
            history.reverse()

            return render(request, 'app/search.html', {'sn': sn, 'history': history, 'init': init})
    except Exception as e:
        print(e)
        return redirect('index')


def index(request):
    return render(request, 'app/index.html', {})


def market(request):
    try:
        user_id = request.session['user_id']
        name = request.session['name']
        templates = ''
        if (len(name) == 0):
            templates = 'app/marketlogin.html'

        else:
            templates = 'app/market.html'
            all = Sellcar.objects.all().order_by('-id')
            total_len = len(all)
            page = request.GET.get('page')
            paginator = Paginator(all, 10)

            try:
                lines = paginator.page(page)
            except PageNotAnInteger:
                lines = paginator.page(1)
            except EmptyPage:
                lines = paginator.page(paginator.num_pages)
            index = lines.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 2 if index >= 2 else 0
            if index < 2:
                end_index = 3 - start_index
            else:
                end_index = index + 3 if index <= max_index - 3 else max_index
            page_range = list(paginator.page_range[start_index:end_index])

            allcars = {'result_list': lines, 'page_range': page_range, 'total_len': total_len,
                       'max_index': max_index - 2}
        return render(request, templates, allcars)

    except Exception as e:
        print(e)
        return redirect('marketlogin')


def marketlogin(request):
    if request.method == 'GET':
        return render(request, 'app/marketlogin.html', {})
    else:
        user_id = request.POST.get('user_id', False)
        passwd = request.POST.get('passwd', False)

        result_dict = {}
        try:
            Market.objects.get(user_id=user_id, passwd=passwd)
            name = Market.objects.filter(user_id=user_id).values('name')[0]['name']
            result_dict['result'] = 'success'
            request.session['user_id'] = user_id
            request.session['name'] = name

        except Market.DoesNotExist:
            result_dict['result'] = 'fail'
        return JsonResponse(result_dict)


def marketregister(request):
    if request.method == 'GET':
        return render(request, 'app/marketregister.html', {})
    else:
        result_dict = {}

        Name = request.POST['name']
        Address = request.POST['address']
        User_id = request.POST['user_id']
        PW = request.POST['passwd']
        CPW = request.POST['confirm']
        BIRTH = request.POST['birth']
        RRN = request.POST['rrn']
        residentnum = BIRTH + '-' + RRN
        alluser = Market.objects.all()
        list = []
        for i in range(0, len(alluser)):
            a = alluser.values('residentnum')[i]['residentnum']
            list.append(a)

        if PW != CPW:
            result_dict['result'] = 'Password does not match'
            return JsonResponse(result_dict)
        elif Name == '' or Address == '' or User_id == '' or PW == '' or BIRTH == '' or RRN == '':
            result_dict['result'] = 'Please pill out the form'
            return JsonResponse(result_dict)
        elif residentnum in list:
            result_dict['result'] = 'Resident Number cannot be used'
            return JsonResponse(result_dict)

        else:
            try:
                Market.objects.get(user_id=User_id)
                result_dict['result'] = 'ID cannot be used'

            except Market.DoesNotExist:

                market = Market(name=Name, address=Address, user_id=User_id, passwd=PW, passconfirm=CPW,
                                residentnum=residentnum)
                market.c_date = timezone.now()
                market.save()
                result_dict['result'] = 'success'
        return JsonResponse(result_dict)


def modify(request):
    if request.method == 'GET':
        return render(request, 'app/maypage.html', {})
    else:
        user_id = request.session['user_id']
        pw = request.POST['passwd']
        newpw = request.POST['newpasswd']
        cpw = request.POST['confirm']
        address = request.POST['address']
        result_dict = {}
        PW = Market.objects.filter(user_id=user_id).values('passwd')[0]['passwd']
        try:
            if pw == PW and newpw == cpw:
                market = Market.objects.get(user_id=user_id)
                market.passwd = newpw
                market.passconfirm = cpw
                market.address = address
                market.save()
                alret = "Success"
                return render(request, 'app/mypage.html', {'alret': alret})
            else:
                alret = "Fail"
                return render(request, 'app/mypage.html', {'alret': alret})
        except Exception as e:
            print(e)
            return redirect('mypage')


def registervehicle(request):
    return render(request, 'app/registervehicle.html', {})


def mytrade(request):
    try:
        user_id = request.session['user_id']
        name = request.session['name']
        templates = ''
        if (len(name) == 0):
            templates = 'app/marketlogin.html'

        else:
            templates = 'app/mytrade.html'
            sellcars = Sellcar.objects.filter(owner=user_id).order_by('-id')
            n = len(sellcars)
            paginator = Paginator(sellcars, 10)
            page = request.GET.get('page')
            mycars = paginator.get_page(page)

        return render(request, templates, {'mycars': mycars, 'n': n, 'uesr_id': user_id})

    except Exception as e:
        print(e)
        return redirect('marketlogin')


def remove(request):
    check_id = request.GET['check_id']
    check_ids = check_id.split(',')

    for id in check_ids:
        try:
            Sellcar.objects.get(id=id).delete()
        except:
            pass
    return redirect('mytrade')


def register(request):
    try:
        user_id = request.session['user_id']
        sn = request.POST['sn']
        otp = request.POST['otp']
        Sellprice = request.POST['sellprice']
        Details = request.POST['details']
        result_dict = {}
        if sn == '' or Sellprice == '' or otp == '':
            result_dict['result'] = "Please pill out the form"
            return JsonResponse(result_dict)
        else:
            residentnum = Market.objects.filter(user_id=user_id).values('residentnum')[0]['residentnum']
            rrn = residentnum[:6] + residentnum[7:]
            url = ("http://45.32.103.121:8001/history/%s" % sn)
            res = requests.post(url)
            history = res.json()
            init = history[0]
            Time = init['Timestamp']
            Model = init['Value']['name']
            Company = init['Value']['manufacture']
            Type = init['Value']['vehicletype']
            Volume = init['Value']['volume']
            Fuel = init['Value']['fuel']

            currentrrn = []
            for i in range(0, len(history)):
                owner = history[i]['Value']['rrnum']
                if owner == '':
                    pass
                else:
                    currentrrn.append(owner)
                    set(currentrrn)
                    seller = currentrrn[-1]

            serial = []
            for i in Sellcar.objects.all():
                num = i.serialnumber
                serial.append(num)

            currentplate = []
            for i in range(0, len(history)):
                plate = history[i]['Value']['plate']
                if plate == '':
                    pass
                else:
                    currentplate.append(plate)
                    set(currentplate)
                    plate = currentplate[-1]

            otpkey = Market.objects.filter(user_id=user_id).values('otp')[0]['otp']
            totp = pyotp.TOTP(otpkey)
            nowotp = totp.now()
            if otp == nowotp:
                try:
                    if sn not in serial and seller == rrn:

                        upload_files = request.FILES.getlist('my_file')
                        path = ('upload/%s' % user_id)

                        try:
                            os.mkdir(path)
                        except FileExistsError as e:
                            pass
                        files = []
                        for upload_file in upload_files:
                            file_name = upload_file.name
                            files.append(file_name)
                            with open(path + '/' + file_name, 'wb') as file:
                                for chunk in upload_file.chunks():
                                    file.write(chunk)
                        if len(files) == 1:
                            files1 = files[0]
                            files2 = ''
                            files3 = ''
                        elif len(files) == 2:
                            files1 = files[0]
                            files2 = files[1]
                            files3 = ''
                        else:
                            files1 = files[0]
                            files2 = files[1]
                            files3 = files[2]

                        sellcar = Sellcar(serialnumber=sn, company=Company, modelname=Model, type=Type, volume=Volume,
                                          fuel=Fuel, owner=user_id, whentobuy=Time, sellprice=Sellprice,
                                          details=Details, plate=plate, file1=files1, file2=files2, file3=files3)
                        sellcar.save()
                        result_dict['result'] = 'Success'
                        return JsonResponse(result_dict)
                    else:
                        result_dict['result'] = 'Make sure your car is right'
                        return JsonResponse(result_dict)
                except Exception as e:
                    print(e)
                    result_dict['result'] = 'Fail'
                    return JsonResponse(result_dict)
            else:
                result_dict['result'] = 'OTP Authentication Failed'
                return JsonResponse(result_dict)
    except Exception as e:
        print(e)
        return redirect('registervehicle')


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
    result_dict = {}
    if sn == '' or factory == '' or name == '' or type == '' or volume == '' or fuel == '':
        result_dict['result'] = "Please pill out the form"
        return JsonResponse(result_dict)

    else:
        url = 'http://45.32.103.121:8001/init_car/' + sn + '-' + manufacture + '-' + factory + '-' + name + '-' + type + '-' + volume + '-' + fuel
        response = requests.post(url)
        res = response.text

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
    birth = request.POST['birth']
    rrn = request.POST['rrn']
    tradehistory = request.POST['tradehistory']
    price = request.POST['price']
    result_dict = {}
    if sn == '' or plate == '' or owner == '' or birth == '' or rrn == '' or tradehistory == '' or price == '':
        result_dict['result'] = "Please pill out the form"
        return JsonResponse(result_dict)

    else:
        url = 'http://45.32.103.121:8001/change_car/' + sn + '-' + government + '-' + plate + '-' + owner + '-' + birth + rrn + '-' + tradehistory + '-' + price
        response = requests.post(url)
        res = response.text
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
    result_dict = {}
    if sn == '' or repair == '' or repairprice == '':
        result_dict['result'] = "Please pill out the form"
        return JsonResponse(result_dict)

    else:
        url = 'http://45.32.103.121:8001/repair_car/' + sn + '-' + repair + '-' + repairprice + '-' + shop
        response = requests.post(url)
        res = response.text
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
    result_dict = {}
    if sn == '' or accident == '' or costs == '':
        result_dict['result'] = "Please pill out the form"
        return JsonResponse(result_dict)
    else:
        url = 'http://45.32.103.121:8001/accident_car/' + sn + '-' + accident + '-' + costs + '-' + insurance
        response = requests.post(url)
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
        try:
            if len(str(request.session['name'])) != 0:
                del request.session['name']
                del request.session['user_id']
        except:
            pass

        return redirect('index')

    except Exception as e:
        print(e)
        return render(request, 'app/index.html', {})
