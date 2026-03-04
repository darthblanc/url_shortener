from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from shorten import shorten_url
from redirect import get_url
from payload import Payload
from supabase_client import supabase

app = FastAPI(title="URL Shortener", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Hello from URL Shortener"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/shorten")
def shorten(payload: Payload):
    shortened_url = ""
    try:
        shortened_url = shorten_url(payload.url, supabase)
    except Exception as e:
        raise e
    return {"shortened_url": shortened_url}

@app.get("/{redirect_code}")
def redirect(redirect_code: str):
    url = ""
    try:
        url = get_url(redirect_code, supabase)
    except Exception as e:
        raise e
    return RedirectResponse(url)
