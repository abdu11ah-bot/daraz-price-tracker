import os
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.logger import setup_logger
from app.data_process import (
    save_price,
    get_old_price,
    compare_price,
    get_all_product_data,
    delete_product_by_url,
    delete_product_by_id,
)
from app.database import engine
from app.model import Base
from app.webscraper import Webscraper

Base.metadata.create_all(bind=engine)
setup_logger()

app = FastAPI(title="Price Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ── Track / update a product price ──────────────────────────────────────────

@app.get("/track/{url:path}")
def track_price(url: str):
    """
    Scrape the product at the given URL, compare against the stored price,
    and return the result with price change info.
    """
    logging.info(f"Tracking URL: {url}")
    result = Webscraper(url)
    if result is None:
        raise HTTPException(
            status_code=422,
            detail="Could not scrape product data from the provided URL.",
        )

    name, price = result
    price = float(price)

    old_price_raw = get_old_price(name)
    [name, new_price, old_price] = compare_price(name, price, url)

    difference = round(new_price - old_price, 2)

    if old_price_raw is None:
        status = "new"
    elif new_price > old_price:
        status = "increased"
    elif new_price < old_price:
        status = "decreased"
    else:
        status = "no_change"

    return {
        "status": status,
        "name": name,
        "url": url,
        "new_price": new_price,
        "last_price": old_price,
        "difference": difference,
        "percent_change": round((difference / old_price) * 100, 2) if old_price else 0,
    }


# ── List all tracked products ────────────────────────────────────────────────

@app.get("/products")
def list_products():
    products = get_all_product_data()
    return {"products": products, "count": len(products)}


# ── Delete by URL ─────────────────────────────────────────────────────────────

class DeleteByUrlRequest(BaseModel):
    url: str


@app.delete("/products/by-url")
def remove_product_by_url(body: DeleteByUrlRequest):
    """Delete a tracked product by its URL."""
    deleted = delete_product_by_url(body.url)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Product with that URL not found."
        )
    return {"message": "Product deleted successfully.", "url": body.url}


# ── Delete by ID ──────────────────────────────────────────────────────────────

@app.delete("/products/{product_id}")
def remove_product_by_id(product_id: int):
    """Delete a tracked product by its database ID."""
    deleted = delete_product_by_id(product_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail=f"Product with id {product_id} not found."
        )
    return {"message": "Product deleted successfully.", "id": product_id}
