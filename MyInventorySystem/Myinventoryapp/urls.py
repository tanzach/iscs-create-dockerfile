"""MyInventorySystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.homepage, name='homepage'), 
    path('change_password', views.create_employee, name='create_employee'),
    path('homepage', views.homepage, name='homepage'),
    path('payslips', views.payslips, name='payslips'),
    path('create_payslips', views.create_payslip, name='create_payslip'),
    path('update_employee/<int:pk>/', views.update_employee, name="update_employee"),
    path('delete_employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('add_overtime/<int:pk>/', views.add_overtime, name='add_overtime'),
    path('view_payslipC1/<int:pk>/', views.view_payslip, name='view_payslipC1'),
    path('view_payslipC2/<int:pk>/', views.view_payslip, name='view_payslipC2'),
]