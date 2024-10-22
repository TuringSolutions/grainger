from fastapi import FastAPI, Response
from pydantic import BaseModel
from celery_app import tasks
import asyncio


class ScrapeBody(BaseModel):
    url: str
    zipcode: str
    token: str


app = FastAPI()


@app.post("/scrape/grainger")
async def scrape_grainger(body: ScrapeBody, res: Response):
    url = body.url
    zipcode = body.zipcode
    token = body.token

    if token != "Scrape Grainger":
        res.status_code = 403
        return None

    try:
        result = tasks.scrape_grainger_url.delay(url, zipcode)
        await asyncio.sleep(20)
        prod_content, ship_content, status_code = result.get()
        if status_code == 404:
            return {"product": prod_content, "shipping": ship_content, "status": 404}
        if prod_content is None or ship_content is None:
            res.status_code = 500
            return None
        return {"product": prod_content, "shipping": ship_content, "status": 200}
    except:
        res.status_code = 500
        return None
