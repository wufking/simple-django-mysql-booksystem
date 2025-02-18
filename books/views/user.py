from distutils.command.config import config
from enum import member
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from books.models import Deletion,Book,Sell,CustomUser
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone  # 导入 timezone


@login_required # 验证是否登录
def users(request, tel):
    if request.method == 'GET':
        # # books_list = Book.objects.all()  # 获取所有书籍
        # page_number = request.GET.get('page')  # 获取请求的页码
        # if request.session:
        #     print(request.session)
        # session_data = request.COOKIES.items()
        # print("user:", request.user)
        # print(len(session_data))
        # for key,value in session_data:
        #     print(key,value)
        books = pagination(request)
        context = {
            'tel':tel,
            'books':books,
        }
        # 返回用户界面
        return render(request, 'users.html', context=context)

    elif request.method == 'POST':
        action = request.POST.get('action')
        print("request.post:",request.POST)
        print("action:",action)
        if action == 'search':
            # 查询图书
            search_query = request.POST.get('id_name')
            if not search_query:
                return redirect('users', tel = tel)
            try:
                # 初始化查询条件
                query_conditions = Q(b_name__icontains=search_query)
                # 检查search_query是否为数字字符串
                if search_query.isdigit():  # 判断是否是一个有效的数字字符串
                    # 如果是数字，转换为整数并添加到查询条件
                    query_conditions |= Q(b_id=int(search_query))
                # 执行查询
                books = Book.objects.filter(query_conditions)

                context = {
                    'tel': tel,
                    'books': books,
                }
                # book_list = [{'b_id': book.b_id, 'b_name': book.b_name, 'b_zone': book.b_zone, 'b_address': book.b_address, 'b_state': book.b_state} for book in books]
                # return JsonResponse(book_list, safe=False)
                return render(request, 'users.html', context=context)
            except Book.DoesNotExist:
                books = None
                context = {
                    'tel': tel,
                    'books': books,
                }
                return render(request, 'users.html', context=context)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})

        # { % csrf_token %}
        elif action == 'borrow':
            # 借阅图书
            book_id = request.POST.get('b_id')
            print("borrow_b_id:",book_id)
            try:
                if request.user.is_authenticated is not True:
                    return JsonResponse({'status':'dl_error','message':'登录状态异常'})

                member = CustomUser.objects.get(tel=tel)

                if member.book_number >= 100:
                    return JsonResponse({'status': 'error', 'message': '您借阅的图书数量超过限制！'})

                if Sell.objects.filter(Q(b_id=book_id) & Q(m_tel=tel) & Q(is_back=False)):
                    return JsonResponse({'status':'borrow_error','message':'您已借阅此书！'})

                book = Book.objects.get(b_id=book_id)
                if book.b_state > 0:
                    book.b_state -= 1  # 减少书籍数量
                    member.book_number += 1 # 增加借书数量
                    book.save()
                    member.save()

                    Sell.objects.create(m_name=member.username,
                                        m_tel=tel,
                                        b_id=book.b_id,
                                        b_name=book.b_name,
                                        time_out=timezone.now)
                    return JsonResponse({'status': 'success', 'message': '借阅成功'})
                else:
                    return JsonResponse({'status': 'error', 'message': '书籍数量不足'})
            except Book.DoesNotExist:
                return JsonResponse({'status': 'book_error', 'message': '书籍不存在'})
            except CustomUser.DoesNotExist:
                return JsonResponse({'status': 'member_error', 'message': '账户不存在'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})

        elif action == 'return':
            # 归还图书
            book_id = request.POST.get('b_id')
            try:
                if request.user.is_authenticated is not True:
                    return JsonResponse({'status':'dl_error','message':'登录状态异常'})

                member = CustomUser.objects.get(tel=tel)

                if member.book_number <= 0:
                    return JsonResponse({'status': 'return_error', 'message': '您未曾借阅图书！'})

                book = Book.objects.get(b_id=book_id)
                sell = Sell.objects.get(Q(b_id=book_id) & Q(m_tel=tel) & Q(is_back=False))

                book.b_state += 1  # 增加书籍数量
                book.save()
                member.book_number -= 1
                member.save()
                sell.time_out = timezone.now()
                sell.is_back = True
                sell.save()

                return JsonResponse({'status': 'success', 'message': '归还成功'})
            except Book.DoesNotExist:
                return JsonResponse({'status': 'book_error', 'message': '书籍不存在'})
            except CustomUser.DoesNotExist:
                return JsonResponse({'status': 'member_error', 'message': '账户不存在'})
            except Sell.DoesNotExist:
                return JsonResponse({'status': 'Sell_error', 'message': '您并未借阅此书'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'未知错误异常:{str(e)}'})

    elif request.method =='PATCH':
        # member = CustomUser.objects.get(m_tel=tel)
        # member.m_dl = False
        # member.save()
        # 登出操作
        logout(request)
        return JsonResponse({'status': 'success', 'message': '退出成功'})


def pagination(request):
    books_list = Book.objects.all().order_by('b_id')  # 获取所有书籍
    paginator = Paginator(books_list, 15)  # 每页显示 15 条记录

    page_number = request.GET.get('page')  # 获取请求的页码
    try:
        books = paginator.get_page(page_number)  # 获取当前页的书籍
    except EmptyPage:
        books = paginator.page(paginator.num_pages)  # 如果请求的页码超出范围，返回最后一页
    except PageNotAnInteger:
        books = paginator.page(1)
    return books