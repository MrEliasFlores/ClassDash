"""ClassDash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url, static
from django.conf import settings
from django.conf.urls.static import static
from WebSite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.landingPage, name = 'landingPage'),
    url(r'^orderFood/',views.orderFood, name = 'orderFood'),
    url(r'^orderChoice/',views.orderChoice, name = 'orderChoice'),
    url(r'^Meal1/',views.Meal1, name = 'Meal1'),
    url(r'^Meal2/', views.Meal2, name = 'Meal2'),
]
