from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from uuid import uuid4
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from imagegen import generate_images
from videogen import generate_video
from youtube import get_caption, get_title
from utils import range_requests_response

load_dotenv()

app = FastAPI()

generating_videos = set() # A set of video ids that are currently being generated

async def generate_content(lyrics, vid_id):
    try:
        generate_images(lyrics, vid_id)
        generate_video(lyrics, vid_id)
    finally:
        generating_videos.remove(vid_id)

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

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "frontend/build/static")), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "frontend/build/index.html"))

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(os.path.dirname(__file__), "frontend/build/favicon.ico"))

# A GET endpoint which receives the url to a youtube video and return the title of the video
@app.get("/title")
async def title(url: str):
    try:
        title = get_title(url)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL")
    except ConnectionError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Failed to find the video")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
    return {"title": title}


# A GET endpoint which receives the url to a youtube video and return the generated video for streaming
@app.get("/video")
async def video(url: str, background_tasks: BackgroundTasks):
    vid_id = str(uuid4())
    try:
        title, lyrics = get_caption(url, vid_id)
        generating_videos.add(vid_id)
        background_tasks.add_task(generate_content, lyrics, vid_id)
        return {
            "id": vid_id,
            "title": title,
        }
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL or video is longer than 10 minutes")
    except ConnectionError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Failed to find the video")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


# A GET endpoint which returns the content of the video
@app.get("/content/{vid}")
async def video_content(vid: str, request: Request):
    if vid in generating_videos:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Video is still being generated")
    video_path = os.path.join(os.path.dirname(__file__), f"videos/{vid}.mp4")
    if not os.path.exists(video_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return range_requests_response(request, video_path, "video/mp4")


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse(os.path.join(os.path.dirname(__file__), "frontend/build/index.html"))
