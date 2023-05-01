from bson import Binary
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import Movies
from .mongodb_config import collection
import datetime


def clean_data(data):
    state = None
    if '_state' in data:
        state = data.pop('_state', None)
    data['start_date'] = datetime.datetime.combine(data['start_date'], datetime.time.min)
    return data, state


@receiver(post_save, sender=Movies)
def post_signal(sender, instance, created, **kwargs):
    if created:
        data = instance.__dict__
        data, state = clean_data(data)
        collection.insert_one(data)
        data['_state'] = state


@receiver(pre_save, sender=Movies)
def put_signal(sender, instance, **kwargs):
    if instance.pk:
        data = instance.__dict__
        data, state = clean_data(data)
        # original_poster = data.pop('poster', None)
        # if 'poster' in data:
        #     poster = data['poster']
        #     if isinstance(poster, InMemoryUploadedFile):
        #         poster_data = poster.read()
        #         data['poster'] = Binary(poster_data)
        # data['poster'] = str(data['poster'])
        collection.update_one({"id": data['id']}, {"$set": data})
        data['_state'] = state
        # data['poster'] = original_poster


@receiver(pre_delete, sender=Movies)
def delete_signal(sender, instance, **kwargs):
    data = instance.__dict__
    collection.delete_one({"id": data['id']})
