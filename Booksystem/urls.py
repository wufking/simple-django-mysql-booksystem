"""
URL configuration for Booksystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.views.generic import RedirectView
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.shortcuts import redirect
from books.views import Login,user,Manage,Registration  # 导入 books 应用中的视图

def custom_admin_view(request):
    if not request.user.is_superuser:  # 或其他条件
        return HttpResponseForbidden("You are not allowed to access the admin.")
    return admin.site.urls(request)


def custom_logout(request):
    logout(request)  # 清除会话中的用户信息
    return redirect('login')  # 重定向到登录页面

urlpatterns = [
    path("Admin123/", admin.site.urls),
    # path("Admin123/", custom_admin_view),
    path('', RedirectView.as_view(url='/login/', permanent=False)),  # 将根路径映射到/login
    path('login/', Login.home_login, name='login'),
    path('users/<str:tel>/', user.users, name='users'),
    path('manage/<str:id>/', Manage.manages, name='manage'),
    path('registration/', Registration.registration,name='registration'),
    path('logout/', custom_logout, name='logout'),
]
