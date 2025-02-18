from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    # path('lend_book/', views.lend_book, name='lend_book'),
    # path('return_book/', views.return_book, name='return_book'),
]