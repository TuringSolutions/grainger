from fastapi import FastAPI, Response
from pydantic import BaseModel
from scraper import grainger_scraper

class ScrapeBody(BaseModel):
    url : str
    zipcode: str
    token : str


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
        prod_content, ship_content = await grainger_scraper.run_scrape(url, zipcode)
        return {
            "product": prod_content,
            "shipping": ship_content
        }
    except:
        res.status_code = 500
        return None
    