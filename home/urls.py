from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('index', views.index, name='indexPage'),
    path('login', views.user_login, name='loginPage'),
    path('logout', views.user_logout, name='logoutPage'),
    path('signup', views.user_signup, name='signupPage'),
    path('profile', views.user_profile, name='profilePage'),
    path('changepass', views.user_changepass, name='changepasspage'),
    path('member', views.memberView, name='memberPage'),
    path('vaccineslot', views.vaccineSlotView, name='vaccineSlotPage'),
    path('datafetch', views.datafetchview, name='dataPage'),
    path('vaccineBook', views.booking, name='bookingPage'),
    path('verification', views.verification_view, name='verificationPage'),
    path('contact', views.contact_view, name='contactPage'),
    path('slot', views.slot, name='slotPage')


    # path('adminProfile', views.admin_profile, name='adminProfilePage'),
]
