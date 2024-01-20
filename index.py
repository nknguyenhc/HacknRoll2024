from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from dotenv import load_dotenv
from uuid import uuid4
import os

from imagegen import generate_images
from videogen import generate_video
from youtube import get_caption, get_title
from utils import range_requests_response

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
    try:
        title = get_title(url)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid URL")
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to find the video")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    return {"title": title}


# A GET endpoint which receives the url to a youtube video and return the generated video for streaming
@app.get("/video")
async def video(url: str):
    vid_id = str(uuid4())
    try:
        title, lyrics = get_caption(url, vid_id)
        generate_images(lyrics, vid_id)
        video = generate_video(lyrics, vid_id)
        return {
            "id": vid_id,
            "title": title,
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid URL or video does not have caption")
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to generate the video")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# A GET endpoint which returns the content of the video
@app.get("/content/{vid}")
async def video_content(vid: str, request: Request):
    video_path = f"videos/{vid}.mp4"
    if not os.path.exists(video_path):
        raise HTTPException(status_code=400, detail="Video does not exist")

    # video_size = os.path.getsize(video_path)
    # with open(video_path, 'rb') as f:
    #     chunk_size = 10 ** 6
    #     start = int(re.sub(r'[^0-9]', '', request.headers["Range"]))
    #     end = min(start + chunk_size, video_size - 1)
    #     content_length = end - start + 1
    #     f.seek(start)
    #     data = f.read(end - start)
    #     headers = {
    #         "Content-Range": f"bytes {start}-{end}/{video_size}",
    #         "Accept-Ranges": "bytes",
    #         "Content-Length": str(end - start),
    #         "Content-Type": "video/mp4",
    #     }
    #     response = Response(data, headers=headers, media_type="video/mp4")
    #     response.status_code = 206
    #     return response
    return range_requests_response(request, video_path, "video/mp4")
