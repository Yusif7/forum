"""
URL configuration for myForum project.

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
from forum import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('posts/', views.allposts, name='allposts'),
    path('myposts/', views.ownerposts, name='ownerposts'),
    path('сontrol/', views.controlposts, name='controlposts'),
    path('create/', views.createpost, name='createpost'),
    path('completed/', views.completedposts, name='completedposts'),
    path('viewpost/<int:post_pk>/', views.viewpost, name='viewpost'),
    path('viewpost/<int:post_pk>/complete/', views.completepost, name='completepost'),
    path('viewpost/<int:post_pk>/delete/', views.deletepost, name='deletepost'),
    path('viewpost/<int:post_pk>/comment/', views.viewpost, name='addcomment'),
    path('viewpost/<int:post_pk>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),



    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('owner/', views.owneruser, name='owneruser'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)