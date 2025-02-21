from email.message import Message
from enum import member

from pyexpat.errors import messages

from books.models import Book, Sell, Deletion,CustomUser
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

MemberTel = 'tel'
MemberName = 'username'
BookId = 'b_id'
BookName = 'b_name'

 # python manage.py runserver

@login_required
def manages(request,id):
    if request.method == "GET":
        # for field in Member._meta.get_fields():
        #     print(f"Field: {field.name}, Type: {field.get_internal_type()}")
        # print(id)
        member_list = CustomUser.objects.filter(is_staff=False).order_by('last_login')  # 获取所有用户信息
        book_list = Book.objects.all().order_by('b_id')
        sell_list = Sell.objects.all().order_by('time_out')
        deletion_list = Deletion.objects.all().order_by('settime')

        member_paginator = Paginator(member_list, 10)  # 每页显示 15 条成员记录
        book_paginator = Paginator(book_list, 10)  # 每页显示 15 条书籍
        sell_paginator = Paginator(sell_list, 15)  # 每页显示 20 条信息
        deletion_paginator = Paginator(deletion_list, 2)  # 每页显示 30 条删除记录

        member_page_number = request.GET.get('member_page')  # 获取请求的页码
        book_page_number = request.GET.get('book_page')  # 获取请求的页码
        sell_page_number = request.GET.get('sell_page')  # 获取请求的页码
        deletion_page_number = request.GET.get('deletion_page')  # 获取请求的页码
        try:
            # 获取当前页的内容
            members = member_paginator.get_page(member_page_number)
            books = book_paginator.get_page(book_page_number)
            sells = sell_paginator.get_page(sell_page_number)
            deletions = deletion_paginator.get_page(deletion_page_number)
        except EmptyPage:
            # 如果请求的页码超出范围，返回最后一页
            members = member_paginator.page(member_paginator.num_pages)
            books = book_paginator.page(book_paginator.num_pages)
            sells = sell_paginator.page(sell_paginator.num_pages)
            deletions = deletion_paginator.page(deletion_paginator.num_pages)
        except PageNotAnInteger:
            # 如果页码不是整数，则返回第一页
            members = member_paginator.page(1)
            books = book_paginator.page(1)
            sells = sell_paginator.page(1)
            deletions = deletion_paginator.page(1)

        print(request)
        print("GET:",request.GET)
        # currentTab = request.GET.get('tab')  # 默认tab为1
        # if currentTab == 'None':  # 处理URL中tab为None的情况
        #     currentTab = '1'
        print("bookpage:",len(members))
        # print("tab:",currentTab)

        context = {
            'id': id,
            'members': members,
            'books': books,
            'sells': sells,
            'deletions': deletions,
            # 'currentTab': currentTab,
            'member_page': request.GET.get('member_page', 1),
            'book_page': request.GET.get('book_page', 1),
            'sell_page': request.GET.get('sell_page', 1),
            'deletion_page': request.GET.get('deletion_page', 1),
        }
        # 返回管理员界面
        # return render(request, 'manage.html', context=context)
        return render(request,'Guanliyuan.html',context=context)

    elif request.method == "POST":
        action = request.POST.get('action')

        if action == 'member_search':
            # 获取 POST 请求中的 id 和 name
            member_tel = request.POST.get('tel', None)
            member_name = request.POST.get('name', None)

            # # 如果两个都为空，返回所有成员
            if not member_tel and not member_name:
                return redirect('manage', id = id)
            members = find_data(member_tel, member_name,CustomUser,MemberTel,MemberName)

            if not members:
                return render(request, 'Guanliyuan.html', {
                    'id':id,
                    'members': members,
                    'message': '未找到符合条件的成员。',
                })
            return render(request, 'Guanliyuan.html', {
                    'id':id,
                    'members': members,
                    'message': None,  # 没有错误时不需要提示
                })

        if action == 'member_del':
            # 获取 POST 请求中的 id 和 name
            member_tel = request.POST.get('tel', None)
            member_name = request.POST.get('name', None)
            # print("tel:",member_tel)
            # print("name:",member_name)
            # # 如果两个都为空，返回所有成员
            if not member_tel and not member_name:
                return JsonResponse({'status': 'error', 'message': '信息不能为空！'})
            members = find_data(member_tel, member_name,CustomUser,MemberTel,MemberName)
            try:
                if not members:
                    return JsonResponse({'status': 'error', 'message': '删除失败！未找到目标'})
                if members.first().book_number > 0:
                    return JsonResponse({'status': 'error', 'message': '删除失败！此用户并未归还所有书籍！'})
                members.delete()
                return JsonResponse({'status': 'success', 'message': '删除成功！'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})

        if action == 'member_status':
            member_tel = request.POST.get('tel', None)
            member_name = request.POST.get('name', None)
            if not member_tel and not member_name:
                members = CustomUser.objects.exclude(borrowed_books_count='0').order_by('last_login')
                # return render(request, 'Guanliyuan.html', {
                #     'id': id,
                #     'members': members,
                #     'message': None,
                # })
            else:
                members_a = find_data(member_tel, member_name,CustomUser,MemberTel,MemberName)
                members = members_a.exclude(borrowed_books_count='0').order_by('last_login')
            return render(request, 'Guanliyuan.html', {
                'id': id,
                'members': members,
                'message': None,
            })

        if action == 'member_add':
            name = request.POST.get('name')
            tel = request.POST.get('tel')
            address = request.POST.get('address')
            id_card = request.POST.get('id_card')
            pwd = request.POST.get('pwd')
            try:
                CustomUser.objects.create_user(username=name,tel=tel,address=address,id_card=id_card,password=pwd)
                return JsonResponse({'status': 'success','message':"创建成功！"})
            except IntegrityError:
                return JsonResponse({'status': 'error', 'message': '同一手机号或同一身份证不能注册多个账户！'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})

        if action == 'searchsell':
            tel_id = request.POST.get('tel_id')
            name = request.POST.get('name')
            # # 如果两个都为空，返回所有借阅信息
            if not tel_id and not name:
                url = reverse('manage', kwargs={'id':id}) + '?tab=2'
                return redirect(url)
            sell_member = find_data(tel_id,name,Sell,MemberTel,MemberName)
            sell_book = find_data(tel_id,name,Book,BookId,BookName)
            # if not tel_id:
            #     sells = Sell.objects.filter(b_id=b_id)
            #     messages = "未找到符合条件的记录或输入图书id有误！"
            # elif not name:
            #     if tel_id.isdigit():
            #         sells = Sell.objects.filter(m_tel=name_tel)
            #     else:
            #         sells = Sell.objects.filter(m_name=name_tel)
            #     messages = "未找到符合条件的记录或输入用户姓名电话有误！"

            if not sell_member and not sell_book:
                sells = None
                messages = "未找到符合条件的记录或输入信息有误！"
            else:
                sells = sell_book or sell_member
                messages = None
            return render(request, 'Guanliyuan.html', {
                'id': id,
                'tab': 2,
                'sell': sells,
                'message': messages,
            })

        if action == 'addbook':
            b_id = request.POST.get('id')
            name = request.POST.get('name')
            zone = request.POST.get('zone')
            address = request.POST.get('address')
            state = request.POST.get('state')
            try:
                Book.objects.create(b_id=b_id,b_name=name,b_address=address,b_zone=zone,b_state=state)
                return JsonResponse({'status': 'success','message':"图书新增成功！"})
            except IntegrityError:
                book = Book.objects.get(b_id=b_id)
                book.m_state = book.m_state + state
                book.save()
                return JsonResponse({'status': 'success', 'message': f'图书{book.b_name}数量增加{book.b_state}成功！'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})

        if action == 'removebook':
            b_id = request.POST.get('b_id')
            state = request.POST.get('state')
            # if not id and not state:
            #     return JsonResponse({'status': 'error', 'message': '信息不能为空！'})
            try:
                book = Book.objects.get(b_id=b_id)
                if book.m_state == state:
                    book.delete()
                    return JsonResponse({'status': 'success', 'message': '删除成功！'})
                elif book.m_state > state:
                    book.m_state -= state
                    book.save()
                    return JsonResponse({'status': 'success', 'message': f'图书数量成功减少{state}！剩余{book.m_state-state}本'})
                elif book.m_state < state:
                    return JsonResponse({'status': 'error', 'message': '删除失败！图书数量不足'})
            except Book.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': '删除失败！图书id错误'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})

        if action == 'searchbooks':
            b_id = request.POST.get('id')
            name = request.POST.get('name')
            print("id:",b_id)
            print("name:",name)
            if not b_id and not name:
                print(22222222)
                url = reverse('manage', kwargs={'id':id}) + '?tab=3'
                return redirect(url)
            print(1111)
            books = find_data(b_id,name,Book,BookId,BookName)
            print(22222)
            return render(request, 'Guanliyuan.html', {
                'id': id,
                'tab': 3,
                'books': books,
            })










    # elif request.method == "PATCH":
    #

# def find_members(member_tel,member_name,model):
#     # print("tel:",member_tel)
#     # print("name:",member_name)
#     if not member_tel:
#         members = model.objects.filter(m_name__icontains=member_name)
#     # 如果 name 为空，查询 id
#     elif not member_name:
#         members = model.objects.filter(m_tel__icontains=member_tel)
#     # 如果两个都不为空，根据 id 和 name 都来查询
#     else:
#         members = model.objects.filter(m_tel__icontains=member_tel, m_name__icontains=member_name)
#     return members

# 用两个数据分别查找一个模型下两个属性（前提：必须有一个不是空的）
def find_data(id_tel,name,model,field_tel_id,field_name):
    # id_tel、name为查询的两个数据，model为模型名，field为两个属性名称
    # 动态构建查询条件
    filter_kwargs_tel_id = {f'{field_tel_id}__icontains': id_tel}  # 动态构造查询条件
    filter_kwargs_name = {f'{field_name}__icontains': name}  # 动态构造查询条件
    if not id_tel:
        datas = model.objects.filter(**filter_kwargs_name)
    # 如果 id_tel 为空，查询 name
    elif not name:
        datas = model.objects.filter(**filter_kwargs_tel_id)
    # 如果两个都不为空，根据 id_tel 和 name 都来查询
    else:
        datas = model.objects.filter(**filter_kwargs_tel_id, **filter_kwargs_name)
    return datas




