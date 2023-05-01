from celery import Celery
from app.mongodb_config import collection
app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672/vhost')


@app.task
def scheduler():
    collection.update_many({"status": "upcoming"}, {"$inc": {"ranking": 10}})


app.conf.beat_schedule = {
    "update_ranking": {
        "task": "celery_config.scheduler",
        "schedule": 10.0
    }
}
