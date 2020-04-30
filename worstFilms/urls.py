from django.urls import path, re_path
from . import views


app_name = 'worstFilms'
urlpatterns = [
    path('create/' , views.create_worst , name = 'create'),
    path('edit/<int:id>' , views.edit_worst , name = 'edit'),
    path ('' , views.home_page , name = 'home'),
    path('detail/<int:id>/', views.detail_worst , name = 'detail'),
    path('delete/<int:id>/', views.delete_worst , name = 'delete'),
    path('reply/<int:film_id>/<int:comment_id>/', views.reply_worst, name= 'reply'),
    path('like/<int:film_id>/', views.like_film, name= 'like_film'),
]

