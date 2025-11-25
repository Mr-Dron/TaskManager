from arq import cron
from arq.connections import RedisSettings
from app.workers.tasks import send_message
from app.config.settings import settings

async def check_notifications(ctx):

    #Проходит по таблице с задачами у которых deadline <= now() и is_sent = False
    print("Checking notifications ...")

class WorkerSettings:
    redis_settings = RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        database=0,
    )

    functions = [check_notifications, send_message]

    cron_jobs = [
        cron(check_notifications, second=10)
    ]