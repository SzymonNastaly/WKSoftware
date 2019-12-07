"""WKSoftware URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from Kampfrichter import views

urlpatterns = [
    path('kampfrichter/', views.kampfrichter, name="kampfrichter"),
    path('admin/', admin.site.urls),
    path('schiedsrichter/erstellung/', views.add, name="add"),
    path('schiedsrichter/bearbeitung/', views.editinglist, name="editlist"),
    path('schiedsrichter/bearbeitung/delete<int:runid>/', views.deleterun, name="deleterun"),
    path('schiedsrichter/bearbeitung/lauf<int:runid>/', views.specificrun, name="specificrun"),
    path('schiedsrichter/', views.schiedsrichter, name="schiedsrichter"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/confirmation/', views.logoutconfirmation, name='logoutconfirmation'),
    path('', views.index, name="index"),
]
