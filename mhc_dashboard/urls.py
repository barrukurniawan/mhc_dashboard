"""mhc_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_dashboard import views as dashboard

urlpatterns = [
    path('entry-employees/', dashboard.add_user_dashboard, name='entry-employees'),
    path('entry-companies/', dashboard.add_company, name='entry-companies'),
    path('company-lists/result-company/<path:sort>/<path:page>/<path:tipe_filter>/<path:keywords>', dashboard.company_lists, name='result-company'),
    path('company-lists/result-message/', dashboard.message_lists, name='result-message'),
    path('company-lists/result-page/', dashboard.page_lists, name='result-page'),
    path('employee-lists/result-page-emp/', dashboard.page_lists_emp, name='result-page-emp'),
    path('remove-company/<path:dash_id>', dashboard.remove_company, name='remove-company'),
    path('employee-lists/result-employee/<path:sort>/<path:page>/<path:tipe_filter>/<path:keywords>', dashboard.employee_lists, name='result-employee'),
    path('remove-employee/<path:my_email>', dashboard.remove_employee, name='remove-employee'),
    path('company-lists/', dashboard.filter_company, name='company-lists'),
    path('detail-company/<path:dash_id>', dashboard.comp_detail_view, name='detail-company'),
    path('detail-user/<path:email>', dashboard.user_detail_view, name='detail-user'),
    path('account-user/', dashboard.my_detail_view, name='account-user'),
    path('employee-lists/', dashboard.filter_employee, name='employee-lists'),
    path('user-lists/', dashboard.user_lists, name='user-lists'),
    path('change-password/', dashboard.change_password_view, name='change-password'),
    path('login/', dashboard.login_view, name='login'),
    path('', dashboard.home_view, name='home'),
    path('logout/', dashboard.logout_view, name='logout'),
    path('company-lists/', dashboard.company_lists, name='company-lists'),
    path('register/', dashboard.register_view, name='register'),
]

handler404 = 'user_dashboard.views.handler404'
handler500 = 'user_dashboard.views.handler500'
