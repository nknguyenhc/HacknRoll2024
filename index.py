from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from imagegen import generate_images
from videogen import generate_video
from youtube import get_caption, get_title

load_dotenv()

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:3000",  # React app address
    # Add any other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# A GET endpoint which receives the url to a youtube video and return the title of the video
@app.get("/title")
async def title(url: str):
    title = get_title(url)
    return {"title": title}