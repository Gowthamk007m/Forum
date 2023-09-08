from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='main'),

    path('Home', views.home, name='home'),
    path('post/new/', views.new_post, name='new_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('comment/<int:comment_id>/remove/',views.remove_comment, name='remove_comment'),
    path('<int:post_id>/add_comment/',views.add_comment_to_post, name='add_comment_to_post'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.LogoutUser, name='logout'),

]
