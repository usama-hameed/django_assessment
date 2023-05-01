from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Movies
from .serializers import MovieSerializer
from rest_framework import status
from .mongodb_config import collection
# Create your views here.


class MovieView(APIView):
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Movie Added', 'status': status.HTTP_200_OK})
        else:
            return Response({'messgae': str(serializer.errors), 'status': status.HTTP_400_BAD_REQUEST})

    def put(self, request, pk):
        try:
            movie = Movies.objects.get(pk=pk)
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_404_NOT_FOUND})
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=movie, validated_data=request.data)

            return Response({'message': 'Movie Updated', 'status': status.HTTP_200_OK})
        else:
            return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})

    def delete(self, request, pk):
        try:
            movie = Movies.objects.get(pk=pk)
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_404_NOT_FOUND})
        movie.delete()
        return Response({'message': 'Movie Deleted', 'status': status.HTTP_200_OK})


class SortedMovies(APIView):
    def get(self, request):
        movies = collection.find().sort("ranking", 1)
        all_movies = list(map(lambda movie: dict(movie, _id=str(movie['_id'])), movies))
        return Response({'data': all_movies})
