from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from Registration import views
import Registration.execute

urlpatterns = [
    path('', views.home),
    path('vaccines/', views.vaccines),
    path('centres/', views.centres),
    path('read-more/', views.read_more),
    path('about-us/', views.about_us),
    path('signin/', views.signin),
    path('signup/', views.signup),
    path('signout/', views.signout),
    path('loggedin/1/', views.loggedin_1),
    path('loggedin/2/', views.loggedin_2),
    path('loggedin/3/', views.loggedin_3)
]
