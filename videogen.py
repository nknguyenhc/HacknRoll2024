def generate_video(lyrics, vid_id):
    """Generate a parody video from the lyrics and the generated images.
    The `lyrics` is an array, each element is a dictionary representing a sentence in the music video, with the following keys:
    * `start`: The start of the sentence, in seconds.
    * `duration`: The duration of the sentence, in seconds.
    * `text`: The content of the sentence.
    For example:
    ```
    [
        {
            "start": 1.395,
            "duration": 4.931,
            "text": "\u266a Just gonna stand there\nand watch me burn \u266a"
        }, 
        {
            "start": 6.326,
            "duration": 5.000,
            "text": "\u266a Well, that's alright, because\nI like the way it hurts \u266a"
        },
    ]
    ```
    Most likely, the `text` key is not needed.
    The lyrics should be used to determine the time period that each image appears in the video.

    The `vid_id` is the ID of the video internally generated in this server. This should be used to:
    * Obtain the audio file. The audio file is named `f"{vid_id}.mp4"` located in `audio` folder.
    * Obtain images. The images are found in the folder `/images/{vid_id}`.
        Each frame is named after the index of the lyrics sentence.
        For example, image corresponding to frame 9 is named `9.png` or `9.jpg` (extension to be decided later).
    * Name the generated video. The video should be put in `video` folder and named `f"{vid_id}.mp4"`.
    """
    pass
