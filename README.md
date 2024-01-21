# HacknRoll2024

Generate music parody in one step

## Inspiration

The inspiration behind Parody Generator lies in our desire to revolutionise the music video industry. Imagine if you could generate an entire music video just at the touch of your fingers. We observed that there was a demand for such services, but there was no convenient way of doing so and the user has to have a certain level of coding knowledge. Hence, we decided to create and deploy a website that will allow the user to automate this entire process. 

## What it does

The user can simply upload a youtube link, confirm the video title, and wait! Our website will then generate a full music video with accompanying subtitles for the user to view and download. 

## How we built it

Upon receiving a video URL, the following happens:

* Audio and lyrics are obtained from Youtube, using `pytube`.
* In the case that lyrics is not available for the specified video, audio is sent to OpenAI to transcribe lyrics.
* Lyrics are sent to Stable Diffusion to generate images.
* Subtitles are added to the images, using `pillow`.
* Images and audio are combined into a single video, using `moviepy`.

### Techstacks

1. FastAPI

This is the Python framework that powers our backend.

2. Pytube

This is the Python library we used to download Youtube video information, including the audio and lyrics.

3. OpenAI

OpenAI speech-to-text capability was used to transcribe our audio with lyrics, in the case that the lyrics is not readily available in a given Youtube video.

4. Stable Diffusion

This is the main generative AI algorithm that we used to generate images for our videos. One sentence is translated to one image.

5. Moviepy

A Python library we used to combine our images and audio into a complete video.

6. React.js

Our frontend is powered by React.js and Material UI.

7. Docker

Docker is used to generate the image and deployed onto Azure.

8. Azure

We used Azure Container Registry to store our Docker image. We used Azure AppService to deploy our website from the same image.

## Challenges we ran into

We had trouble with deploying our Docker image and deploy our website on Azure. We fixed the problem by fixing the authentication issue and add extra error handling to our webapp.

## Accomplishments that we're proud of

We are proud that we can generate a parody video from just a Youtube link. This was unprecedented, while only making use of available generative AIs.

## What we learned

We have learnt to use various APIs to make our app works. This includes the generative AI APIs that help with lyrics transcription and image generation.

## What's next for Parody Generator

* Make sharable links, so that user can share videos that they generated with others.
* Users can specify an overall theme for their video.

## Development

### Backend

1. Install Python dependencies.

```
pip install -r requirements.txt
```

2. Start the development server.

```
uvicorn index:app --reload
```

3. When finished, indicate the new Python dependencies.

```
pip freeze > requirements.txt
```

WARNING: Please do not put any secrets (API key, etc) in your code!
Put secrets in a `.env` file and place the file in the root directory.
The server has been configured to load environment variables on start.

### Frontend

1. Start the backend development server (see above).

2. On a new terminal, navigate to the frontend folder.

```
cd frontend
```

3. Install the Node.js dependencies.

```
npm i
```

4. Start the React development server.

```
npm start
```

## Contributors

* [Duy](https://github.com/ncduy0303)
* [Jiale](https://github.com/Singa-Pirate)
* [Nguyen](https://github.com/nknguyenhc)
* [Yiqiao](https://github.com/fuyiqiao)
