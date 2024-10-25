from os import name # for naming convention for urls
from django.contrib import admin
from django.urls import path,include

from django.contrib.auth.views import (
  LoginView, 
  LogoutView,
  PasswordResetView,
  PasswordResetDoneView,
  PasswordResetConfirmView,
  PasswordResetCompleteView
  )
from leads.views import LandingPageView, SignUpView ,user_logout


from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LandingPageView.as_view(),name='landing'),
    path('signup/', SignUpView.as_view(), name='sign'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),


    #password reset urls 
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('Password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

   
    path('leads/',include('leads.urls',namespace='leads')),    # urls file in the leads app
    path('agents/',include('agents.urls',namespace='agents')), # urls file in the agents app
]

if settings.DEBUG :
  urlpatterns+= static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)