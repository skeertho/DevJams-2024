
from django.contrib import admin
from django.urls import path
from quackpack import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login/', views.loginUser, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('registration/',views.registration,name='registration'),
    path('doRegistration/',views.doRegistration,name='doRegistration'),
    path('registration/student/', views.studentregistration, name='student_registration'),
    path('registration/warden/', views.wardenregistration, name='warden_registration'),
    path('doRegistration/student/', views.dostudentregistration, name='dostudent_registration'),
    path('doRegistration/warden/', views.dowardenregistration, name='dowarden_registration'),
    path('doLogin/main1', views.main1, name='student_main'),
    path('doLogin/main2', views.main2, name='warden_main'),
    path('doLogin/main1/request_page', views.request_page, name='request_page'),
    path('doLogin/main1/deliver_page', views.deliver_page, name='deliver_page'),
]
