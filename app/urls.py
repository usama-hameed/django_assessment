from django.urls import path, include
from .views import MovieView, SortedMovies

urlpatterns = [
    path('/movies', MovieView.as_view(), name='movies'),
    path('/movies/<int:pk>', MovieView.as_view(), name='movie'),
    path('/movies-list', SortedMovies.as_view(), name='movies-list')
]
