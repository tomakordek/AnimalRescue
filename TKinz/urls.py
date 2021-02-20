"""TKinz URL Configuration

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
from django.urls import path
from index import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='index'),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('<int:ToDo_id>/', views.detail, name='detail'),
    path('<int:ToDo_id>/delete', views.deletetodo, name='deletetodo'),
    path('current/', views.currents, name='currents'),
    path('current/found/', views.currentsfound, name='currentsfound'),
    path('current/lost/', views.currentslost, name='currentslost'),
    path('current/done/', views.currentsdone, name='currentsdone'),
    path('current/other/', views.currentsother, name='currentsother'),
    path('create/', views.createtodo, name='createtodo'),
    path('user/', views.UserTodo, name='UserTodo'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
