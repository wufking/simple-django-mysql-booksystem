# your_app/models.py
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone  # 导入 timezone
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, tel, password, **extra_fields):
        if not tel:
            raise ValueError('The Telephone field must be set')  # ValueError
        if not password:
            raise ValueError('The Password field must be set')  # 添加检查
        user = self.model(tel=tel, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tel, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(tel, password, **extra_fields)


class CustomUser(AbstractUser):
    tel = models.CharField(max_length=15, unique=True, primary_key=True) # 主键电话
    address = models.CharField(max_length=50, null=True, blank=True) # 用户地址
    book_number = models.IntegerField(default=0) # 现在借了几本书
    code = models.BigIntegerField(unique=True, null=True) # 身份证

    objects = CustomUserManager()  # 使用自定义管理器

    USERNAME_FIELD = 'tel'  # 使用 'tel' 作为用户名字段
    REQUIRED_FIELDS = ['username', 'email']  # 创建用户时要求 'username' 和 'email' 字段

    def __str__(self):
        return self.tel
"""
username：唯一标识用户的用户名。
last_name：用户的姓氏。
email：用户的电子邮件地址。
first_name：用户的名字。
password：加密存储的用户密码。
is_active：布尔值，表示用户账户是否处于激活状态。如果为 False，用户不能登录。
is_staff：布尔值，表示用户是否是站点管理员。如果为 True，用户可以访问 Django 后台。
is_superuser：布尔值，表示用户是否是超级管理员，超级管理员拥有所有权限。
last_login：用户的最后登录时间。
date_joined：用户账户创建的时间。
"""





# class administrator(models.Model):
#     a_id = models.IntegerField(primary_key=True) # 管理员id
#     a_name = models.CharField(max_length=10, null=True, blank=True) # 管理员名字
#     a_pwd = models.CharField(max_length=128, default="Admin123456!") # 密码
#     a_tel = models.CharField(max_length=12, unique=True, default='00000000') # 电话
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # 创建时间
#     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # 更新时间
#     last_login = models.DateTimeField(null=True, blank=True) # 最后登录时间
#     a_status = models.BooleanField(default=True) # 激活状态
#
#     def update_last_login(self):
#         self.last_login = timezone.now()  # 更新最后登录时间
#         self.save(update_fields=['last_login'])  # 只保存 last_login 字段
#
#     def save(self, *args, **kwargs):
#         if self.pk is None or self.a_pwd == "Admin123456!":  # 如果是新创建的实例
#             self.a_pwd = make_password(self.a_pwd)  # 对密码进行加密
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return str(self.a_id)
#
# class Member(models.Model):
#     m_name = models.CharField(max_length=10, null=True, blank=True) # 用户姓名
#     madness = models.CharField(max_length=50, null=True, blank=True) # 用户地址
#     m_tel = models.BigIntegerField(primary_key=True) # 电话
#     m_code = models.BigIntegerField(unique=True,default=None) # 身份证
#     m_dl = models.BooleanField(default=False) # 登录状态
#     m_state = models.IntegerField(default=0) # 现在借了几本书
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # 创建时间
#     last_login = models.DateTimeField(null=True, blank=True) # 最后登录时间
#     m_pwd = models.CharField(max_length=128, default="abc123456") # 密码
#
#     def save(self, *args, **kwargs):
#         # if self.pk is None or self.m_pwd == "abc123456":  # 如果是新创建的实例
#         if not self.m_pwd.startswith('pbkdf2_'):  # 检查密码是否未加密
#             self.m_pwd = make_password(self.m_pwd)  # 对密码进行加密
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.m_name




class Deletion(models.Model):
    # 定义四个状态
    # PENDING = 'pending'  # 待阅
    # REJECTED = 'rejected'  # 不采纳
    # TO_DO = 'to_do'  # 待办
    # DONE = 'done'  # 已办
    #
    # TASK_STATUS_CHOICES = [
    #     (PENDING, '待阅'),
    #     (REJECTED, '不采纳'),
    #     (TO_DO, '待办'),
    #     (DONE, '已办'),
    # ]
    #
    # # 模型字段，使用 choices 限制状态
    # status = models.CharField(
    #     max_length=10,
    #     choices=TASK_STATUS_CHOICES,
    #     default=PENDING  # 默认状态为 "待阅"
    # )
    b_name = models.CharField(max_length=20, null=True, blank=True)
    b_content = models.CharField(max_length=100, null=True, blank=True)
    settime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Book(models.Model):
    b_id = models.IntegerField(primary_key=True) # 图书id
    b_name = models.CharField(max_length=20, default="Unknown") # 书名
    b_zone = models.CharField(max_length=10, default="Unknown") # 区域
    b_address = models.CharField(max_length=10, default="Unknown") # 书的地址
    b_state = models.IntegerField(default=0) # 书的数量

class Sell(models.Model):
    m_name = models.CharField(max_length=10, default="Unknown") # 用户名字
    m_tel = models.BigIntegerField(default=0) # 用户id
    b_id = models.IntegerField(default=0) # 书id
    b_name = models.CharField(max_length=20, default="Unknown") # 书名
    is_back = models.BooleanField(default=False) # 归还状态，默认为否
    time_out = models.DateTimeField(auto_now_add=True, null=True, blank=True) # 借出时间(自动)
    time_back = models.DateTimeField(null=True, blank=True) # 归还时间

# python manage.py makemigrations
# python manage.py migrate
