import urllib.parse
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "lyrics": None})

@app.post("/lyrics", response_class=HTMLResponse)
async def get_lyrics(request: Request, artist: str = Form(...), title: str = Form(...)):
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    lyrics = "Lyrics not found."
    youtube_embed_url = None
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            lyrics = data.get("lyrics", lyrics)
    # Create YouTube search query
    query = urllib.parse.quote(f"{artist} {title} official audio")
    youtube_embed_url = f"https://www.youtube.com/embed?listType=search&list={query}"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "lyrics": lyrics,
        "artist": artist,
        "title": title,
        "youtube_embed_url": youtube_embed_url
    })
