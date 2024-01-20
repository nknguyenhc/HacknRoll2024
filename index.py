from fastapi import FastAPI, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from dotenv import load_dotenv

from imagegen import generate_images
from videogen import generate_video
from youtube import get_caption, get_title

load_dotenv()

vid_id = 0

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
    global vid_id
    vid_id += 1
    try:
        title, lyrics = get_caption(url, vid_id)
        video = generate_video(lyrics, title)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid URL")
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Failed to generate the video")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    # file_like = open(video, mode="rb")
    # return StreamingResponse(file_like, media_type="video/mp4")