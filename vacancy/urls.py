from django.contrib import admin
from django.urls import path
from . import views

app_name = 'vacancy'

urlpatterns = (
    path('', views.all_vacancies, name='all_vacancies'),
    path('<int:id>',
         views.vacancy_detail,
         name='vacancy_details'),
)