from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('data/',data_info,name ='data_info'),
    path('', first_page, name='first_page'),
    path('experiment/', experiment, name="experiment"),
    path('result1/', result1_random, name='result1'),
    path('test/', test ,name='test')
]

