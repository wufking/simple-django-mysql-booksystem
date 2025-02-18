from django.contrib import admin

# Register your models here.
# books/admin.py
from django.contrib import admin
from .models import Deletion, Book, Sell,CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # 显示哪些字段，字段按组划分，按需要显示在表单中
    fieldsets = (
        (None, {'fields': ('tel', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'address', 'book_number', 'code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # 在列表页中显示的字段
    list_display = ('tel', 'username', 'code', 'email', 'is_staff', 'is_active', 'book_number','last_login')

    # 搜索字段：允许通过这些字段进行搜索
    search_fields = ('tel', 'email', 'username', 'code')

    # 过滤字段：可在侧边栏中按这些字段过滤
    list_filter = ('is_staff', 'is_active', 'groups')

    # 用户模型的可编辑字段
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tel', 'username', 'password1', 'password2', 'is_staff'),
        }),
    )

# 注册自定义的用户模型和管理器
admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(administrator)
# admin.site.register(Member)
admin.site.register(Deletion)
admin.site.register(Book)
admin.site.register(Sell)
