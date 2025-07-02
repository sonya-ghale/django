# here importing django function path and all of our views from the blog applications

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
  path("__reload__/", include("django_browser_reload.urls")),

    path('', views.post_list, name='post_list'),
    # create path after creating link in the posr_list title
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # the last name='posy_list' is the name of the url that will be used to identify the view 
    #path('', views.post_list, name='post_list'),

    path('post/new/', views.post_new, name='post_new'),

    path('post/<int:pk>/edit/', views.post_edit, name="post_edit"),

      path('accounts/login/', auth_views.LoginView.as_view(), name='login'),

      path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

]

