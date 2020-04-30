from django.urls import path, re_path
from . import views

app_name = 'account'
urlpatterns = [
    path('signup/', views.signupUser, name= 'signupUser'),
    path('login/', views.loginUser, name= 'loginUser'),
    path('logout/', views.logoutUser, name= 'logoutUser'),
    path('dashboard/<int:user_id>/', views.dashboard, name= 'dashboard'),
    path('editprofile/<int:user_id>/', views.edit_profile, name= 'edit_profile'),
    path('follow/', views.follow, name= 'follow'),
    path('unfollow/', views.unfollow, name= 'unfollow'),
]