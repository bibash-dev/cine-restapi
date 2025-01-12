from django.urls import path
# from .views import movie_list, movie_detail
from .views import MovieListAV, MovieDetailAV

urlpatterns = [
    path('movies_list/', MovieListAV.as_view(), name='movies-list'),
    path('<int:pk>/', MovieDetailAV.as_view(), name='movie-detail'),
]