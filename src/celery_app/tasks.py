from celery import Celery
from os import getenv
from tasks import grainger_scraper
import asyncio

REDIS_URI = getenv('REDIS_URI')
REDIS_BACKEND_DBINDEX = getenv('REDIS_BACKEND_DBINDEX')
REDIS_BROKER_DBINDEX = getenv('REDIS_BROKER_DBINDEX')

celery_app = Celery(main='scraper', broker=f'{REDIS_URI}/{REDIS_BROKER_DBINDEX}', backend=f'{REDIS_URI}/{REDIS_BACKEND_DBINDEX}')

@celery_app.task
def scrape_grainger_url(url, zipcode):
    loop = asyncio.get_event_loop()
    try:
        result = loop.run_until_complete(grainger_scraper.run_scrape(url, zipcode))
        return result
    except Exception as ex:
        return None, None
    