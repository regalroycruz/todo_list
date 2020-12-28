"""todolist URL Configuration

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
from todo_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('signup/', views.sign_up_user, name='sign_up_user_alias'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='login_alias'),

    # Todos
    path('current/', views.current_to_do, name='current_to_do_alias'),
    path('', views.home, name = 'home'),
    path('create/', views.createtodo, name = 'createtodo'),
    path('todo/<int:todo_pk>', views.view_to_do, name='view_to_do_alias'),
    path('todo/<int:todo_pk>/complete', views.complete_to_do, name='complete_to_do'),
    path('todo/<int:todo_pk>/delete', views.delete_to_do, name='delete_to_do'),

    path('completed/', views.show_completed, name='show_completed'),


]
