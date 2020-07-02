"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf.urls import include, url
from django.contrib import admin

from Diplom.views import index, index_for_all, login, logoutView, registration, calculate, calculate_for_all, start

app_name = 'Diplom'

urlpatterns = [
    url(r'^$', start, name='start'),
    url(r'^calculate/', calculate, name='calculate'),
    url(r'^for_all_calculate/', calculate_for_all, name='calculate_for_all'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logoutView, name='logout'),
    url(r'^registration/', registration),
    url(r'^prediction', index, name='index'),
    url(r'^for_all_prediction', index_for_all, name='index_for_all'),
]
