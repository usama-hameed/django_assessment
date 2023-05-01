from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from datetime import date
from app.models import Movies
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_create_movie_valid_data():
    client = APIClient()
    url = reverse('movies')
    data = {
        "name": "Fight Club",
        "protagonists": ["Brad Pitt"],
        "poster": 'poster.jpg',
        "start_date": date.today().strftime('%Y-%m-%d'),
        "status": "upcoming",
        "ranking": 0
    }
    response = client.post(url, data, format='multipart')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_movie_invalid_data():
    client = APIClient()
    url = reverse('movies')
    data = {
        "name": "Fight Club",
        "start_date": date.today().strftime('%Y-%m-%d'),
        "status": "upcoming",
        "ranking": 0
    }
    response = client.post(url, data, format='json')
    assert response.data['status'] == 400


@pytest.mark.django_db
def test_create_movie_update():
    image = Image.new('RGB', (100, 100))
    image_file = io.BytesIO()
    image.save(image_file, 'JPEG')
    image_file.seek(0)
    image_data = SimpleUploadedFile("image.jpg", image_file.read(), content_type="image/jpeg")
    client = APIClient()
    # url = reverse('movie/pk')
    movie = Movies.objects.create(name='Fight Club', protagonists=['Brad Pitt'], poster=image_data,
                                  status='upcoming', ranking=0)

    updated_data = {
        "name": "Top Gun",
        "protagonists": ["Tom Cruise"],
        "poster": 'poster.jpg',
        "start_date": date.today().strftime('%Y-%m-%d'),
        "status": "upcoming",
        "ranking": 0
    }

    response = client.put(f'/app/movies/{movie.id}', updated_data, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_movie_delete():
    image = Image.new('RGB', (100, 100))
    image_file = io.BytesIO()
    image.save(image_file, 'JPEG')
    image_file.seek(0)
    image_data = SimpleUploadedFile("image.jpg", image_file.read(), content_type="image/jpeg")
    client = APIClient()
    # url = reverse('movie/pk')
    movie = Movies.objects.create(name='Fight Club', protagonists=['Brad Pitt'], poster=image_data,
                                  status='upcoming', ranking=0)

    updated_data = {
        "name": "Top Gun",
        "protagonists": ["Tom Cruise"],
        "poster": 'poster.jpg',
        "start_date": date.today().strftime('%Y-%m-%d'),
        "status": "upcoming",
        "ranking": 0
    }

    response = client.delete(f'/app/movies/{movie.id}', updated_data, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_sorted_movies():
    client = APIClient()
    response = client.get('/app/movies-list')
    assert response.status_code == 200
