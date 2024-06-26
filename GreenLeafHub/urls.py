"""
URL configuration for GreenLeafHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls import include

from GreenWebsite.views import dashboard, logout_user, signup_view, login_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', signup_view, name='signup'),
]
