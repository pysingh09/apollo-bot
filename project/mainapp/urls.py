"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from mainapp.views import Login, Logout, SignUp, HomePage, Dashboard, gentella_html, index,\
        PrivacyPolicy
from django.conf.urls import url, include

urlpatterns = [
    url('login/', Login.as_view(), name='login'),
    url('logout/', Logout.as_view(), name='logout'),
    url('signup/', SignUp.as_view(), name='signup'),
    url('privacy_policy/', PrivacyPolicy.as_view(), name='privacy_policy'),
    url('dashboard/', Dashboard.as_view(), name='dashboard'),
    url(r'^.*\.html', gentella_html, name='gentella'),

    # The home page
    url(r'^$', Login.as_view(), name='index'),
]
