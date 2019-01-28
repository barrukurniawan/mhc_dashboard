from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.contrib.postgres.search import SearchVector
from .backends import UserModelAuth
from .forms import CustomUserCreationForm, LoginForm, OtpForm, ResetPassForm, UserBusinessForm, GroupBusinessForm, CompanyListForm, userDetailForm, ChangePassword, CommentsForm
from .models import CustomUser, GroupBusiness, UserBusiness, TaskBusiness
from bcrypt import hashpw, gensalt, checkpw
from django.core.mail import send_mail, EmailMessage
from datetime import datetime, timedelta
import json, string, random, uuid
from django.utils import timezone
import pytz
# Create your views here.

@login_required(login_url='/login')
def company_lists(request):
    return render(request, 'user_dashboard/company_lists.html')

@login_required(login_url='/login')
def user_lists(request):
    return render(request, 'user_dashboard/user_lists.html')

def register_view(request):
    if request.method == 'POST':
        formRegis = CustomUserCreationForm(request.POST)

        if formRegis.is_valid():
            email = formRegis.cleaned_data.get('email')
            first_name = formRegis.cleaned_data.get('first_name')
            last_name = formRegis.cleaned_data.get('last_name')
            password = formRegis.cleaned_data.get('password1')
            hashed = hashpw(password.encode('utf-8'), gensalt())
            dash_id = ''.join(random.choice(string.ascii_uppercase) for i in range(3)) + str(''.join(random.choice(string.digits) for i in range(3))) + ''.join(random.choice(string.ascii_uppercase) for i in range(2))
            event = formRegis.save(commit=False)
            event.api_token = create_token()
            event.password = hashed.decode('utf-8')
            event.is_active = 'true'
            event.first_name
            event.last_name
            event.dashboard_id = dash_id
            event.status = 'Super Admin' 
            event.full_name = first_name + ' ' + last_name
            event.save()

            user = UserBusiness.objects.create(
                first_name  = first_name,
                last_name   = last_name,
                full_name   = first_name + ' ' + last_name,
                email       = email,
                status      = 'Super Admin',
                dashboard_id= dash_id,
                is_active   = 'true'
            )
            user.save()

            user = UserModelAuth.authenticate(username=email, password=password)

            return redirect('login')
    else:
        formRegis = CustomUserCreationForm()

    data ={
        'formRegis': formRegis
    }
    return render(request, 'user_dashboard/register.html', data)

def login_view(request):
    if request.method == 'POST':
        formLogin = LoginForm(request.POST)
        if formLogin.is_valid():
            email = formLogin.cleaned_data.get('email')
            password = formLogin.cleaned_data.get('password')
            user = UserModelAuth.authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                
                if user.is_active == 'true':
                    return HttpResponseRedirect('/entry-companies')
                else:
                    return HttpResponseRedirect('/register')
            else:
                formRegis = CustomUserCreationForm()
                formLogin.error = 'Email / Password salah'

        else:
            formRegis = CustomUserCreationForm()

    else:
        formLogin = LoginForm()

    data ={
        'formLogin': formLogin,
    }
    return render(request, 'user_dashboard/login.html', data)

def handler404(request, exception):
    return render(request, 'user_dashboard/404.html', locals())

def email_user(subject, message, email_to):
    email_from = 'barru.kurniawan@gmail.com'
    send = send_mail(subject, message, email_from, email_to)
    print (email_from)
    print (send)
    return send

def create_token():
    return uuid.uuid4().hex

def logout_view(request):
    logout(request)

    return redirect('login')

def password_reset_view(request):
    if request.method == 'POST':
        formPass = ResetPassForm(request.POST)

        if formPass.is_valid():
            email = formPass.cleaned_data.get('email')
            user = CustomUser.objects.get(email=email)
            new_pass = random_pass(8)
            hashed = hashpw(new_pass.encode('utf-8'), gensalt())

            user.password = hashed.decode('utf-8')
            user.save()

            subject = 'Reset Password Account WE+'
            message = 'Password telah berhasil direset menjadi: ' + new_pass
            email_to = [email]
            email_user(subject, message, email_to)

            formPass.non_field_errors = ['Password telah di reset, check email untuk info lebih lanjut']
    else:
        formPass = ResetPassForm()

    data = {
        'formPass': formPass
    }
    return render_view(request, 'accounts/resetpassword.html', data)

@login_required(login_url='/login')
def add_user_dashboard(request):
    if request.method == 'POST':
        formUser = UserBusinessForm(request.POST)
        print (formUser.errors)
        if formUser.is_valid():
            instance = formUser.save(commit=False)
            password = create_password()
            email = formUser.cleaned_data['email']
            
            instance.full_name = formUser.cleaned_data['first_name'] + ' ' + formUser.cleaned_data['last_name']
            instance.status = formUser.cleaned_data['status']
            instance.email = email
            instance.wilayah = formUser.cleaned_data['wilayah']
            instance.role = formUser.cleaned_data['role']
            instance.dashboard_id = request.user.dashboard_id
            instance.is_active = 'true'
            instance.save()

            user = CustomUser.objects.create(
                first_name  = formUser.cleaned_data['first_name'],
                last_name   = formUser.cleaned_data['last_name'],
                full_name   = instance.full_name,
                email       = email,
                api_token   = create_token(),
                password    = password['hashed'],
                status      = formUser.cleaned_data['status'],
                dashboard_id= request.user.dashboard_id,
                is_active   = 'true'
            )
            user.save()
            print ("email akun : " + str(email) + " passwordnya : " + str(password))
            subject = 'Selamat Bergabung di MHC Dashboard Web'
            message = 'Anda telah terdaftar pada account business atas nama perusahaan ' + 'MH Consulting' + '\r\n\r\n'
            message += 'Silakan menggunakan fasilitas Dashboard Business di http://156.67.217.27:8000/login. Akun Anda memiliki hak akses sebagai ' + formUser.cleaned_data['role'] + '. Terima kasih \r\n\r\n'
            message += 'Dashboard ID : ' + request.user.dashboard_id + '\r\n' \
                       'Nama Lengkap : ' + formUser.cleaned_data['first_name'] + ' ' + formUser.cleaned_data['last_name'] + '\r\n' \
                       'Silahkan Login dengan menggunakan: \r\n' \
                        'Email : ' + formUser.cleaned_data['email'] + '\r\n' \
                        'Password : ' + password['password']

            email_user(subject, message, [formUser.cleaned_data['email']])

            return HttpResponseRedirect('/entry-employees')

    else:
        formUser = UserBusinessForm()

    user_data = UserBusiness.objects.filter(is_active='true').count()
    data = {
        'formUser': formUser,
        'user_data': user_data,
    }
    return render(request, 'user_dashboard/insert_data_employees.html', data)

@login_required(login_url='/login')
def add_company(request):
    if request.method == 'POST':
        formComp = GroupBusinessForm(request.POST)
        print (formComp.errors)
        if formComp.is_valid():
            password = create_password()
            instance = formComp.save(commit=False)
            dashboard_comp = ''.join(random.choice(string.ascii_uppercase) for i in range(3)) + str(''.join(random.choice(string.digits) for i in range(3))) + ''.join(random.choice(string.ascii_uppercase) for i in range(2))
            instance.company_name = formComp.cleaned_data['company_name']
            instance.address = formComp.cleaned_data['address']
            instance.email = formComp.cleaned_data['email']
            instance.mobile_number = formComp.cleaned_data['mobile_number']
            instance.jenis_usaha = formComp.cleaned_data['jenis_usaha']
            instance.pic = formComp.cleaned_data['pic']
            instance.tipe_sistem = formComp.cleaned_data['tipe_sistem']
            instance.rating = formComp.cleaned_data['rating']
            instance.dashboard_id = dashboard_comp
            instance.is_active = 'true'
            instance.save()

            user = CustomUser.objects.create(
                username    = formComp.cleaned_data['company_name'],
                first_name  = 'admin',
                last_name   = 'client',
                full_name   = 'admin client',
                email       = formComp.cleaned_data['email'],
                api_token   = create_token(),
                password    = password['hashed'],
                dashboard_id= dashboard_comp,
                is_active   = 'true'
            )
            user.save()
            print ("email akun : " + str(formComp.cleaned_data['email']) + " passwordnya : " + str(password))
            return HttpResponseRedirect('/entry-companies')

    else:
        formComp = GroupBusinessForm()

    comp_data = GroupBusiness.objects.filter(is_active='true').count()
    print (comp_data)
    data = {
        'formComp': formComp,
        'comp_data': comp_data,
    }
    return render(request, 'user_dashboard/insert_data_companies.html', data)

@login_required(login_url='/login')
def company_lists(request, page, sort, tipe_filter, keywords):
    # keywords = request.POST.get('cari')
    # print (keywords)
    # print (tipe_filter)

    page_choosen = request.POST.get('page', page)

    date_from = timezone.now() - timedelta(days=365)
    date_to = timezone.now()

    if tipe_filter == 'company_name' and keywords == 'all':
        query = GroupBusiness.objects.filter(is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'company_name' and keywords == keywords :
        query = GroupBusiness.objects.filter(company_name__icontains=keywords, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'jenis_usaha' and keywords == 'all':
        query = GroupBusiness.objects.filter(is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'jenis_usaha' and keywords == keywords :
        query = GroupBusiness.objects.filter(jenis_usaha__icontains=keywords, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'province' and keywords == 'all':
        query = GroupBusiness.objects.filter(is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'province' and keywords == keywords :
        query = GroupBusiness.objects.filter(province__icontains=keywords, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'city' and keywords == 'all':
        query = GroupBusiness.objects.filter(is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'city' and keywords == keywords :
        query = GroupBusiness.objects.filter(city__icontains=keywords,is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'pulau' and keywords == 'all':
        query = GroupBusiness.objects.filter(is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'pulau' and keywords == keywords :
        query = GroupBusiness.objects.filter(pulau__icontains=keywords, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'jenis_usaha' and keywords == 'all':
        query = GroupBusiness.objects.filter(is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'jenis_usaha' and keywords == keywords :
        query = GroupBusiness.objects.filter(jenis_usaha__icontains=keywords, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    else :
        query = GroupBusiness.objects.filter(is_active='true')

    paginator = Paginator(query, sort)
    hasil = paginator.page(page_choosen)
    # print ('paginatornya = ',paginator)
    print ('jumlah total data = ',paginator.count,',sort : ', sort,',keyword : ', keywords,',pilihan page = ',page_choosen)
    # print ('jumlah halaman = ',paginator.num_pages)
    # print ('range halaman = ',paginator.page_range)
    # print ('halaman yang dipilih = ',hasil)
    # print ('isi object = ',hasil.object_list)
    # print (hasil.start_index())
    # print (hasil.end_index())

    # print ('isi query = ',query)

    listing = []
    for item in hasil.object_list:
        if item.is_active == 'true':
            status = 'Active'
            total_data = paginator.count 
            halaman_now = page_choosen
            jumlah_halaman = paginator.num_pages
            hasil_akhir = hasil.end_index()
        elif item.is_active == 'false':
            status = 'Inactive'
        

        # if item.province or item.city or item.pulau or item.jenis_usaha or item.pic or item.rating or item.tipe_sistem is undefined:

        listing.append({
            'company_name':item.company_name,
            'email':item.email,
            'address':item.address,
            'mobile_number':item.mobile_number,
            'jenis_usaha':item.jenis_usaha,
            'dashboard_id': item.dashboard_id,
            'pic': item.pic,
            'province': item.province,
            'city': item.city,
            'pulau': item.pulau,
            'created_at':str(item.created_at.strftime('%d/%m/%Y')),
            'updated_at':str(item.updated_at.strftime('%d/%m/%Y')),
            'tipe_sistem': item.tipe_sistem,
            'rating': item.rating,
            'status': status,
            'message' : item.message,
            'type_msg' : item.type_msg,
            'recipient' : item.recipient,
            'total_data' : total_data,
            'halaman_now' : halaman_now,
            'jumlah_halaman' : jumlah_halaman,
            'sortir' : sort,
            'hasil_akhir' : hasil_akhir
        })

    data ={
        'comp_lists': listing
    }
    s1 = json.dumps(data)
    return JsonResponse(json.loads(s1))

@login_required(login_url='/login')
def page_lists(request):
    page =1;
    page_choosen = request.POST.get('page', page)

    date_from = timezone.now() - timedelta(days=365)
    date_to = timezone.now()

    query = GroupBusiness.objects.filter(is_active='true')
    sort =1;

    paginator = Paginator(query, sort)
    hasil = paginator.page(page_choosen)
    # print ('paginatornya = ',paginator)
    # print ('GET DATA JUMLAH PAGINATION = ',paginator.count,',sort : ', sort,',pilihan page = ',page_choosen)
    # print ('jumlah halaman = ',paginator.num_pages)
    # print ('range halaman = ',paginator.page_range)
    # print ('halaman yang dipilih = ',hasil)
    # print ('isi object = ',hasil.object_list)
    # print (hasil.start_index())
    # print (hasil.end_index())

    # print ('isi query = ',query)

    listing = []
    for item in query :
        if item.is_active == 'true':
            status = 'Active'
            total_data = paginator.count 
            halaman_now = page_choosen
            jumlah_halaman = paginator.num_pages
        elif item.is_active == 'false':
            status = 'Inactive'

        listing.append({
            'company_name':item.company_name,
            'total_data' : total_data,
            'halaman_now' : halaman_now,
            'jumlah_halaman' : jumlah_halaman,
            'sortir' : sort
        })

    data ={
        'page_lists': listing
    }
    s1 = json.dumps(data)
    return JsonResponse(json.loads(s1))

@login_required(login_url='/login')
def message_lists(request):
    date_from = timezone.now() - timedelta(days=365)
    date_to = timezone.now()

    query = TaskBusiness.objects.filter(created_at__range=(date_from, date_to)).order_by('-created_at')

    listing = []
    for item in query:

        listing.append({
            'cc_comp':item.cc_comp,
            'created_at':str(item.created_at.strftime('%d/%m/%Y')),
            'updated_at':str(item.updated_at.strftime('%d/%m/%Y')),
            'message' : item.message,
            'dashboard_id' : item.dashboard_id,
            'type_msg' : item.type_msg,
            'recipient' : item.recipient
        })

    # print (listing)

    data ={
        'msg_lists': listing
    }
    s1 = json.dumps(data)
    return JsonResponse(json.loads(s1))

@login_required(login_url='/login')
def employee_lists(request, page, sort, tipe_filter, keywords):
    # keywords = request.POST.get('cari')

    page_choosen = request.POST.get('page', page)
    date_from = timezone.now() - timedelta(days=365)
    date_to = timezone.now()

    if tipe_filter == 'nama' and keywords == 'all':
        query = UserBusiness.objects.filter(role__isnull=False, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'nama' and keywords == keywords :
        query = UserBusiness.objects.filter(role__isnull=False, full_name__icontains=keywords, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'posisi' and keywords == 'all':
        query = UserBusiness.objects.filter(role__isnull=False, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'posisi' and keywords == keywords :
        query = UserBusiness.objects.filter(role__isnull=False, status__icontains=keywords, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'status' and keywords == 'all':
        query = UserBusiness.objects.filter(role__isnull=False, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')
    elif tipe_filter == 'status' and keywords == keywords :
        query = UserBusiness.objects.filter(role__isnull=False, role__icontains=keywords, is_active='true', created_at__range=(date_from, date_to)).order_by('-created_at')

    paginator = Paginator(query, sort)
    hasil = paginator.page(page_choosen)
    # print ('paginatornya = ',paginator)
    print ('jumlah total data = ',paginator.count,',sort : ', sort,',keyword : ', keywords,',pilihan page = ',page_choosen)

    listing = []
    for item in hasil.object_list:
        if item.is_active == 'true':
            akun = 'Active'
            total_data = paginator.count
            hasil_akhir = hasil.end_index()
        elif item.is_active == 'false':
            akun = 'Inactive'

        # if item.province or item.city or item.pulau or item.jenis_usaha or item.pic or item.rating or item.tipe_sistem is undefined:

        listing.append({
            'full_name':item.full_name,
            'email':item.email,
            'dashboard_id':item.dashboard_id,
            'status':item.status,
            'role':item.role,
            'wilayah':item.wilayah,
            'created_at':str(item.created_at.strftime('%d/%m/%Y')),
            'updated_at':str(item.updated_at.strftime('%d/%m/%Y')),
            'akun': akun,
            'total_data':total_data,
            'hasil_akhir':hasil_akhir
        })

    data ={
        'emp_lists': listing
    }
    s1 = json.dumps(data)
    return JsonResponse(json.loads(s1))

@login_required(login_url='/login')
def page_lists_emp(request):
    page =1;
    page_choosen = request.POST.get('page', page)

    date_from = timezone.now() - timedelta(days=365)
    date_to = timezone.now()

    query = UserBusiness.objects.filter(is_active='true')
    sort =1;

    paginator = Paginator(query, sort)
    hasil = paginator.page(page_choosen)
    print(paginator.count)
    print (hasil)

    listing = []
    for item in query :
        if item.is_active == 'true':
            status = 'Active'
            total_data = paginator.count 
            halaman_now = page_choosen
            jumlah_halaman = paginator.num_pages
        elif item.is_active == 'false':
            status = 'Inactive'

        listing.append({
            'total_data' : total_data,
            'halaman_now' : halaman_now,
            'jumlah_halaman' : jumlah_halaman,
            'sortir' : sort
        })

    data ={
        'page_lists_emp': listing
    }
    s1 = json.dumps(data)
    return JsonResponse(json.loads(s1))

@login_required(login_url='/login')
def filter_company(request):
    query = GroupBusiness.objects.filter(is_active='true')
    if request.method == 'POST':
        filter = CommentsForm(request.POST)

        if filter.is_valid():
            recipient = filter.cleaned_data['recipient']
            print (recipient)
            message = filter.cleaned_data['message']
            print (message)
            type_msg = filter.cleaned_data['type_msg']
            cc_comp = request.POST['cc_comp']

            query_comp = GroupBusiness.objects.get(company_name=cc_comp)

            group_msg = TaskBusiness.objects.update_or_create(
                recipient    = filter.cleaned_data['recipient'],
                message  = filter.cleaned_data['message'],
                type_msg   = filter.cleaned_data['type_msg'],
                cc_comp   = request.POST['cc_comp'],
                dashboard_id   = query_comp.dashboard_id
            )
            group_msg = GroupBusiness.objects.filter(company_name=cc_comp).update(
                recipient    = filter.cleaned_data['recipient'],
                message  = filter.cleaned_data['message'],
                type_msg   = filter.cleaned_data['type_msg']
            )

    else:
        default ={
            'recipient': request.user.full_name,
        }
        filter = CommentsForm(default)
    listing = []
    for item in query:

        listing.append({
            'company_name':item.company_name,
            'email':item.email
        })

    data = {
        'filter'     : filter,
        'listing'    : listing
    }
    return render(request, 'user_dashboard/user_lists_comp.html', data)

@login_required(login_url='/login')
def filter_employee(request):

    return render(request, 'user_dashboard/user-lists_emp.html')

@login_required(login_url='/login')
def remove_company(request, dash_id):
    print (dash_id)
    comp_name = GroupBusiness.objects.filter(dashboard_id__icontains=dash_id)
    comp_name.delete()
    return HttpResponseRedirect('/company-lists/')

@login_required(login_url='/login')
def remove_employee(request, my_email):
    print (my_email)
    emp_bus = UserBusiness.objects.filter(email__icontains=my_email)
    emp_bus.delete()
    emp_name = CustomUser.objects.filter(email__icontains=my_email)
    emp_name.delete()
    return HttpResponseRedirect('/employee-lists/')

def create_password():
    length = 8
    password = ''.join(random.choice(string.ascii_letters) for m in range(length))
    hashed = hashpw(password.encode('utf-8'), gensalt())
    data ={
        'password': password,
        'hashed': hashed.decode('utf-8')
    }
    return data

@login_required(login_url='/login')
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST)

        if form.is_valid():
            old_pass = form.cleaned_data['old_pass']
            new_pass = form.cleaned_data['new_pass']
            confirm_pass = form.cleaned_data['confirm_pass']
            print (old_pass)

            if new_pass != confirm_pass:
                form.non_field_errors = ['Konfirmasi password tidak sama dengan password baru']

            else:
                try:
                    user = CustomUser.objects.get(email=request.user.email)
                    if checkpw(old_pass.encode('utf-8'), user.password.encode('utf-8')):
                        new_pass = form.cleaned_data['new_pass']
                        hashed = hashpw(new_pass.encode('utf-8'), gensalt())

                        CustomUser.objects.filter(id=user.id).update(password=hashed.decode('utf-8'))

                        return HttpResponseRedirect('/logout/')

                except:
                    form.non_field_errors = ['Password lama anda salah']

    else:
        form = ChangePassword()

    data ={
        'form': form
    }
    return render(request, 'user_dashboard/change_password.html', data)

@login_required(login_url='/login')
def user_detail_view(request, email):
    the_user = CustomUser.objects.get(email=email)
    if request.method == 'POST':
        form = userDetailForm(instance=the_user, data=request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.full_name = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
            instance.save()

            UserBusiness.objects.filter(email=email).update(
                first_name  = form.cleaned_data['first_name'],
                last_name   = form.cleaned_data['last_name'],
                full_name   = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name'],
                email       = form.cleaned_data['email'],
                status      = form.cleaned_data['status']
            )

        else:
            return HttpResponse(form.errors)

    else:

        default ={
            'first_name': the_user.first_name,
            'last_name': the_user.last_name,
            'no_identification': the_user.no_identification,
            'mobile_number': the_user.mobile_number,
            'sex': the_user.sex,
            'status': the_user.status,
            'email': the_user.email,
            'birthday': the_user.birthday,
            'address': the_user.address,
            'state': the_user.state,
            'city': the_user.city,
            'code_pos': the_user.code_pos
        }
        form = userDetailForm(default)


    data = {
        'formDetail' : form,
        'full_name' : the_user.full_name,
        'my_email' : email
    }
    return render(request, 'user_dashboard/detail-user.html', data)

@login_required(login_url='/login')
def my_detail_view(request):
    if request.method == 'POST':
        form = userDetailForm(instance=request.user, data=request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.full_name = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
            instance.save()

            UserBusiness.objects.filter(email=request.user.email).update(
                first_name  = form.cleaned_data['first_name'],
                last_name   = form.cleaned_data['last_name'],
                full_name   = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name'],
                email       = form.cleaned_data['email'],
                status      = form.cleaned_data['status']
            )

        else:
            return HttpResponse(form.errors)

    else:

        default ={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'no_identification': request.user.no_identification,
            'mobile_number': request.user.mobile_number,
            'sex': request.user.sex,
            'status': request.user.status,
            'email': request.user.email,
            'birthday': request.user.birthday,
            'address': request.user.address,
            'state': request.user.state,
            'city': request.user.city,
            'code_pos': request.user.code_pos
        }
        form = userDetailForm(default)


    data = {
        'formDetail' : form
    }
    return render(request, 'user_dashboard/account-user.html', data)

@login_required(login_url='/login')
def comp_detail_view(request, dash_id):
    the_bis = UserBusiness.objects.get(email=request.user.email)
    the_comp = GroupBusiness.objects.get(dashboard_id=dash_id)
    if request.method == 'POST':
        form = GroupBusinessForm(instance=the_comp, data=request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

        else:
            return HttpResponse(form.errors)

    else:

        default ={
            'company_name': the_comp.company_name,
            'email': the_comp.email,
            'address': the_comp.address,
            'mobile_number': the_comp.mobile_number,
            'status': the_comp.is_active,
            'jenis_usaha': the_comp.jenis_usaha,
            'updated_at': the_comp.updated_at.strftime('%d-%m-%Y'),
            'tipe_sistem': the_comp.tipe_sistem,
            'province': the_comp.province,
            'pulau': the_comp.pulau,
            'city': the_comp.city,
            'pic': the_comp.pic,
            'rating': the_comp.rating,
            'type_msg' : the_comp.type_msg,
            'message' : the_comp.message
        }
        form = GroupBusinessForm(default)

    data = {
        'formDetail' : form,
        'dashboard_id' : dash_id,
        'the_bis' : the_bis,
        'company_name' : the_comp.company_name
    }
    return render(request, 'user_dashboard/detail-company.html', data)