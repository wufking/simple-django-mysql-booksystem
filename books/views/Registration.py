
from django.shortcuts import render, redirect
from django.http import JsonResponse
from books.models import CustomUser,Deletion,Book,Sell
from django.db import IntegrityError

def registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        tel = request.POST.get('tel')
        address = request.POST.get('address')
        code = request.POST.get('code')
        pwd = request.POST.get('pwd')
        try:
            CustomUser.objects.create_user(
                tel=tel,  # 用户名字段
                password=pwd,  # 密码字段
                code=code,  # 身份证号
                username=name,  # 用户名称
                address=address  # 地址
            )
            # CustomUser.objects.create_user(code,name,address,password=pwd,tel=tel)
            # CustomUser.objects.create(m_name=name,m_tel=tel,madness=address,m_pwd=pwd,m_code=code)
            return JsonResponse({'status': 'success', 'message': '注册成功'})
        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': '同一手机号不能注册多个账户！'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})
    return render(request,'zhuce.html')