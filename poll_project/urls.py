"""poll_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from poll import views
from poll.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #страницы опросов
    path('', views.home, name='home'),#главная страница
    path('results/<int:poll_id>/', views.results, name='results'),#страница с результатами опроса
    path('vote/<int:poll_id>/', views.vote, name='vote'),#страница с голосованием по опросу

    #служебные страницы
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),

    #api
    path('api/v1/information', InformationAPIView.as_view()),#получение списка голосований
    path('api/v1/questions', QuestionAPIView.as_view()),#получение подробной информации о голосовании
    path('api/v1/winners', WinnerAPIView.as_view()),#получение подробной информации о голосовании

]
