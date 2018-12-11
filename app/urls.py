"""carinfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('manufacture/', views.manufacture, name='manufacture'),
    path('manufacture/record/', views.manufacture_record, name='manufacture_record'),
    path('manufacture/success/', views.manufacture_success, name='manufacture_success'),
    path('recordcarinfo/',views.recordcarinfo, name='recordcarinfo'),

    path('government/', views.government, name='government'),
    path('government/record/', views.government_record, name='government_record'),
    path('recordcarchange/',views.recordcarchange, name='recordcarchange'),

    path('repairshop/', views.repairshop, name='repairshop'),
    path('repairshop/record/', views.repairshop_record, name='repairshop_record'),
    path('recordcarrepair/',views.recordcarrepair, name='recordcarrepair'),


    path('insurance/', views.insurance ,name='insurance'),
    path('insurance/record/', views.insurance_record, name='insurance_record'),
    path('recordcaraccident/',views.recordcaraccident, name='recordcaraccident'),
    path('logout/', views.logout, name='logout'),
]