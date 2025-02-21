
import re
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from books.models import CustomUser,Deletion,Book,Sell
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# def registration(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         tel = request.POST.get('tel')
#         address = request.POST.get('address')
#         code = request.POST.get('code')
#         pwd = request.POST.get('pwd')
#         try:
#             CustomUser.objects.create_user(
#                 tel=tel,  # 用户名字段
#                 password=pwd,  # 密码字段
#                 code=code,  # 身份证号
#                 username=name,  # 用户名称
#                 address=address  # 地址
#             )
#             # CustomUser.objects.create_user(code,name,address,password=pwd,tel=tel)
#             # CustomUser.objects.create(m_name=name,m_tel=tel,madness=address,m_pwd=pwd,m_code=code)
#             return JsonResponse({'status': 'success', 'message': '注册成功'})
#         except IntegrityError:
#             return JsonResponse({'status': 'error', 'message': '同一手机号不能注册多个账户！'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})
#     return render(request,'zhuce.html')


def validate_chinese_id_card(id_number):
    # 检查长度是否为18位
    if len(id_number) != 18:
        return False, "身份证号码长度不正确"

    # 检查前17位是否为数字
    if not re.match(r"^\d{17}", id_number):
        return False, "前17位必须为数字"

    # 检查校验码是否为数字或X
    if not re.match(r"[\dX]$", id_number[-1]):
        return False, "校验码必须为数字或X"

    # 检查出生日期是否有效
    try:
        birth_date = datetime.strptime(id_number[6:14], "%Y%m%d")
        if birth_date > datetime.now():
            return False, "出生日期无效"
    except ValueError:
        return False, "出生日期格式不正确"

    # 校验码计算
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    # 计算加权和
    total = sum(int(id_number[i]) * weights[i] for i in range(17))
    remainder = total % 11

    # 验证校验码
    if check_codes[remainder] != id_number[-1]:
        return False, "校验码无效"

    return True, "身份证号码有效"

def validate_tel(value):
    if len(value) < 11 or not value.isdigit():
        raise ValidationError("手机号必须为11位纯数字")


def validate_id_card(value):
    if value:  # 允许为空
        value = value.upper()
        # 真实身份证校验
        # is_valid, message = validate_chinese_id_card(value)
        # if is_valid is False:
        #     raise ValidationError(message)
        if len(value) != 18 :
            raise ValidationError("身份证号格式应为18位（最后一位可为X）")


def registration(request):
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        tel = request.POST.get('tel', '').strip()
        pwd = request.POST.get('pwd', '').strip()
        code = request.POST.get('code', '').strip().upper()  # 身份证统一大写
        address = request.POST.get('address', '').strip()[:50]  # 自动截断超长地址

        try:
            # 数据校验
            validate_tel(tel)
            validate_id_card(code)

            # 创建用户
            CustomUser.objects.create_user(
                name=name if code else None,
                tel=tel,
                password=pwd,
                id_card=code if code else None,  # 空值处理
                address=address if address else None
            )

            return JsonResponse({
                'status': 'success',
                'message': '注册成功',
                'redirect': '/login/'  # 添加跳转指引
            })

        except ValidationError as ve:
            return JsonResponse({'status': 'error', 'message': str(ve)})
        except IntegrityError as ie:
            if 'tel' in str(ie):
                msg = "手机号已被注册"
            elif 'id_card' in str(ie):
                msg = "身份证号已存在"
            else:
                msg = "数据唯一性冲突"
            return JsonResponse({'status': 'error', 'message': msg})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'系统错误：{str(e)}'})

    return render(request, 'zhuce.html')