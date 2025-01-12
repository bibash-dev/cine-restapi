from django.urls import path
from .views import movie_list, movie_detail

urlpatterns = [
    path('movies_list/', movie_list, name='movies-list'),
    path('<int:pk>/', movie_detail, name='movie-detail'),
]