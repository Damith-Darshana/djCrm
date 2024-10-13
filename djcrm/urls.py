from os import name # for naming convention for urls
from django.contrib import admin
from django.urls import path,include

from django.contrib.auth.views import LoginView, LogoutView
from leads.views import LandingPageView, SignUpView


from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
    path('admin/', admin.site.urls),
     path('',LandingPageView.as_view(),name='landing'),
    path('signup/', SignUpView.as_view(), name='sign'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

   
    path('leads/',include('leads.urls',namespace='leads')),
]

if settings.DEBUG :
  urlpatterns+= static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)