from django.urls import path
from . import views
urlpatterns=[
    path('',views.home),
    path('home/',views.home),
    path('',views.base),
    path('about/',views.about),
    path('contact/',views.contactus),
    path('myprofile/',views.myprofile),
    path('myorder/',views.myorder),
    path('brand/',views.brands),
    path('product/',views.prod),
    path('signin/',views.signin),
    path('signup/',views.signup),
    path('feedback/',views.feedback),
    path('view/',views.detail),
    path('proccess/',views.proccess),
    path('cart/',views.cart),
    path('logout/',views.logout),
]