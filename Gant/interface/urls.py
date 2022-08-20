from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', start_page, name='start_page'),
    path('data/', data_info, name='data_info'),
    path('input/', input_page, name='input_page'),
    path('experiment/', experiment, name="experiment"),
    path('archive/', archive, name='archive'),
    path('about/', about, name='about'),
    path('turn/', turn_result, name='turn'),
    path('turn_another/', turn_another_table, name='another'),
    path('turn_rating/', turn_rating_table, name='rating'),
    path('result/', result, name='result')
]

