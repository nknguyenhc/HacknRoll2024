from pytube import YouTube

def get_caption(yt_link, vid_id):
    """Given a YouTube link, downloads the audio of the video, and returns the lyrics of the song.

    The link `yt_link` should start with `https://`, and can be in the form `https://youtube.com/watch` or `https://youtu.be/`.
    For example: `https://youtu.be/u9Dg-g7t2l4` or `https://youtube.com/watch?v=u9Dg-g7t2l4`.

    The ID `vid_id` is internally created in this server. This must be used to name the audio downloaded from Youtube.

    The downloaded audio must be a `.mp4` file located in `audio` folder.
    The name of the audio file must be the `vid_id` given, i.e. `f"{vid_id}.mp4"`.

    The returned value must be a tuple of two values: `(Youtube title, lyrics)`.

    The `lyrics` must be an array, each element represents a sentence in the song.
    Each element must have the following keys:
    * `start`: The starting time of the sentence, in seconds.
    * `duration`: The duration of the sentence, in seconds.
    * `text`: The content of the sentence.
    Note that this info is readily available in Youtube xml caption tree.
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

    (if time permits) raise ValueError if the Youtube video duration > 10min.
    This is to prevent users from clogging the server with a very long Youtube video.
    """

    return "Eminem - Love The Way You Lie ft. Rihanna", [
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
