# from django.test import TestCase
#
# from django.contrib.auth.hashers import make_password,check_password
#
# from books.views import users
# # Create your tests here.
# from books.models import Member
#
#
# user = Member.objects.get(m_tel=111)
# print("pwd:",user.m_pwd)
# print("tel:",user.m_tel)

# tests.py
from django.test import TestCase
from books.models import Book
#
for i in range(1, 101):  # b_id 从 1 到 100
    # 生成符合格式的区域和地址
    b_zone = f"{i % 3 + 1}-{(i + 1) % 3 + 1}-{(i + 2) % 3 + 1}"  # 例如 1-2-3
    b_address = "生活区"  # 固定地址

    Book.objects.create(
        b_id=i,
        b_name=f"书名{i}",  # 例如 书名1
        b_zone=b_zone,
        b_address=b_address,
        b_state=i % 10  # 书的数量可以是 0 到 9
    )
books = Book.objects.all()
for book in books:
    print(book.b_id, book.b_name, book.b_zone, book.b_address, book.b_state)
#
from books.models import Book  # 替换为你的应用名
books = Book.objects.all()
for book in books:
    print(book.b_id, book.b_name, book.b_zone, book.b_address, book.b_state)
# print(int('123451',base=8))
# python manage.py test