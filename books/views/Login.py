from http.client import responses, HTTPResponse
from urllib.request import HTTPPasswordMgr

from django.contrib.admin import action
from django.http import HttpResponse
from django.utils import timezone  # 导入 timezone
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from books.models import Deletion,Book,Sell,CustomUser
from django.shortcuts import render, redirect
from django.db.models import Q
# from .models import Book, Member
from django.http import JsonResponse
import os
import django

def check_cookie(request):
    # 判断session是否有效
    if request.session.exists(request.session.session_key):
        # 从会话中获取 tel，如果没有则返回 None
        tel = request.session.get('tel', None)

        if tel:
            # 如果 tel 存在，返回存储的电话号码
            return tel
    # 如果 tel 不存在，返回提示信息
    return None

def home_login(request):
    tel = check_cookie(request)
    print("tttttt:",tel)
    if tel:
        if request.session.get('status') == 'user':
            return redirect('users', tel = tel)
        else:
            return redirect('manage', id=tel)

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'fankui':
            name = request.POST.get('name')
            text = request.POST.get('text')
            try:
                Deletion.objects.create(b_name=name,b_content=text)
                return JsonResponse({'status': 'success', 'message': "反馈成功！"})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})
        # print("POST data:", request.POST)

        tel = request.POST.get('username')
        pwd = request.POST.get('password')
        usertype = request.POST.get('usertype')

        # 使用 authenticate 验证用户
        print(tel)
        print(pwd)
        user = authenticate(request, tel=tel, password=pwd)
        print("uuuu:",user)

        if user is not None:  # 验证密码
            # 登录用户
            login(request, user)
            # 将用户的电话存储到会话中
            request.session['tel'] = user.tel

            if user.is_staff and usertype == 'administrator':
                request.session['status'] = 'manage'
                return redirect('manage', id = tel)  # 登录成功后重定向
            else:
                request.session['status'] = 'user'
                return redirect('users', tel = tel)  # 登录成功后重定向
            # return render(request, 'login.html', {'error': '用户登录成功！'})
        else:
            return render(request, 'login.html', {'error': '账户不存在或密码错误！'})

    return render(request, 'login.html')


        # print("Username:", tel_id)
        # print("Password:", pwd)
        # print("User Type:", usertype)
        # if usertype == "member":
        #     try:
        #         user = CustomUser.objects.get(m_tel=tel_id)  # 查找用户
        #         # print("user:",user)
        #         if check_password(pwd, user.m_pwd):  # 验证密码
        #             # 登录成功
        #             user.m_dl = True  # 更新登录状态
        #             user.last_login = timezone.now()  # 更新最后登录时间
        #             user.save()  # 保存用户状态更新
        #             # users(request, tel_id)  # 登录用户
        #             return redirect('users', tel = tel_id)  # 登录成功后重定向
        #             # return render(request, 'login.html', {'error': '用户登录成功！'})
        #         else:
        #             return render(request, 'login.html', {'error': '密码错误！'})
        #     except CustomUser.DoesNotExist:
        #         return render(request, 'login.html', {'error': '用户不存在！'})
        # #     user = Member.objects.get(m_tel=tel_id)
        # #     if user.check_password(pwd):
        # #         print("pass")
        # try:
        #     user = administrator.objects.get(a_id=tel_id)  # 查找管理员
        #     if user.a_status == "False":
        #         return render(request, 'login.html', {'error': '管理员账号已注销！'})
        #     if check_password(pwd, user.a_pwd):  # 验证密码
        #         # 登录成功
        #         # user.m_dl = True  # 更新登录状态
        #         user.update_last_login()  # 调用更新方法  更新最后登录时间
        #         # user.save()  # 保存用户状态更新
        #         return redirect('manage', id = tel_id)  # 登录成功后重定向
        #         # return render(request, 'login.html', {'error': '管理员登录成功！'})
        #     else:
        #         return render(request, 'login.html', {'error': '密码错误！'})
        # except administrator.DoesNotExist:
        #     return render(request, 'login.html', {'error': '管理员不存在！'})

    # return render(request, 'login.html', {'error': '程序出现未知错误！'})

# python manage.py runserver


