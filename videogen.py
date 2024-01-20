from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
from cv2 import imread
import os

# TODO: add subtitles
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
        For example, image corresponding to frame 9 is named `9.png`.
    * Name the generated video. The video should be put in `video` folder and named `f"{vid_id}.mp4"`.
    """
    audio = AudioFileClip(os.path.join(os.path.dirname(__file__), f"audio/{vid_id}.mp4"))
    fps = 5

    # create individual clips from images
    curr_point = lyrics[0]["duration"] + lyrics[0]["start"]
    clips = [ImageClip(imread(os.path.join(os.path.dirname(__file__), f"images/{vid_id}/0.png"))).set_duration(curr_point).set_fps(fps)]
    for i, sentence in enumerate(lyrics):
        if i == 0 or i == len(lyrics) - 1:
            continue
        next_point = sentence["duration"] + sentence["start"]
        print(i, next_point, curr_point)
        clips.append(ImageClip(imread(os.path.join(os.path.dirname(__file__), f"images/{vid_id}/{i}.png"))).set_start(curr_point).set_duration(next_point - curr_point).set_fps(fps))
        curr_point = next_point
    clips.append(ImageClip(imread(os.path.join(os.path.dirname(__file__), f"images/{vid_id}/{len(lyrics) - 1}.png"))).set_start(curr_point).set_duration(audio.duration - curr_point).set_fps(fps))
    
    # combine clips and add audio
    video_clip = CompositeVideoClip(clips).set_audio(audio)
    video_clip.write_videofile(os.path.join(os.path.dirname(__file__), f"videos/{vid_id}.mp4"))
    return video_clip


def test():
    generate_video([
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
    ], "sample")


if __name__ == '__main__':
    test()
