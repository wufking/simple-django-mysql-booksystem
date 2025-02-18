from pathlib import Path
import os

# 项目的基本目录，通常是项目的根目录。用于构建其他路径
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# 安全警告：对生产中使用的密钥保密！
SECRET_KEY = "django-insecure-9e6x)xanlj)jbtk366z)oug6k3nv(w92z5hljp_a%nn3ut5dw&"

# 指示是否启用调试模式。开发时应设置为 True，在生产环境中应设置为 False
DEBUG = True

# 一个列表，指定可以向其发送请求的主机/域名。对于生产环境，必须设置
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'books'
]

# 定义了中间件的顺序和处理请求/响应的方式。中间件用于处理请求/响应的生命周期，如用户认证、CSRF 保护等。
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # 内置的安全机制，保护用户和网站之间的通信安全
    "django.contrib.sessions.middleware.SessionMiddleware",   # 会话session功能
    "django.middleware.common.CommonMiddleware",   # 国际化和本地化服务
    "django.middleware.csrf.CsrfViewMiddleware",   # 处理请求信息，规范化请求内容
    "django.contrib.auth.middleware.AuthenticationMiddleware",   # 开启内置的用户认证系统
    "django.contrib.messages.middleware.MessageMiddleware",   # 开启内置的信息提示功能
    "django.middleware.clickjacking.XFrameOptionsMiddleware",   # 防止恶意程序单击劫持
]

# 指定 URL 配置的模块名，通常是 urls.py 文件
ROOT_URLCONF = "Booksystem.urls"

# 这是一个字典，定义了模板引擎的配置，包括模板目录、上下文处理器等
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Django 项目的 WSGI 应用入口点,Django 和 Web 服务器（如 Apache、Nginx）之间的接口
WSGI_APPLICATION = "Booksystem.wsgi.application"

# 一个字典，定义了数据库的配置，如数据库引擎、名称、用户、密码等。
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        # "NAME": BASE_DIR / "db.sqlite3",
        'NAME': 'books',  # 您的数据库名
        'USER': 'root',  # MySQL 用户名
        'PASSWORD': '123456',  # MySQL 用户密码
        'HOST': 'localhost',  # 数据库主机，一般是 'localhost'
        'PORT': '3306',  # MySQL 默认端口
    }
}

# 一个列表，包含了密码强度验证器的配置，用于确保用户密码的安全性。
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 定义了项目的语言代码，用于国际化支持
LANGUAGE_CODE = "zh-hans"
#定义了项目的时区
TIME_ZONE = "Asia/Shanghai"
# 用于启用或禁用 Django 的国际化（I18N）功能,如果项目需要多语言支持或翻译，应该设置为 True。
USE_I18N = True
# 启用时区支持，Django 会自动处理不同时区之间的时间转换,如果项目涉及多个时区的数据处理，应该设置为 True。
USE_TZ = False

# 静态文件（如 CSS、JavaScript、图片等）的 URL 路径
STATIC_URL = "static/"

# 定义模型中默认使用的主键字段类型。Django 3.2 之后，模型中不定义 id 字段时会自动使用 DEFAULT_AUTO_FIELD 指定的类型。
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 用户上传的媒体文件的 URL 路径
# MEDIA_URL =

# 使用自定义的 CustomUser 用户模型
AUTH_USER_MODEL = 'books.CustomUser'

# 设置session有效期为 1 小时
SESSION_COOKIE_AGE = 60*60

# 用户未登录时会被重定向到这个 URL
LOGIN_URL = '/login/'

# session自定义名称,默认sessionid
# SESSION_COOKIE_NAME = 'sessionid'

# 浏览器关闭时session失效
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 指向你的静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]