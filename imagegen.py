def generate_images(lyrics, vid_id):
    """Generate images based on given lyrics.
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
    Most likely, only the `text` key is needed.

    The ID `vid_id` is internally generated in this server, and must be used to name the folder that stores the generated images.

    The images generated must be located in `images/{vid_id}` folder, that is,
    the folder must be named after the ID `vid_id` and must be located in the folder `images`.
    Each image must be named by the index of the lyrics sentence that it corresponds to.
    For example, image that corresponds to sentence index 9 must be named `9.jpg` or `9.png` (extension to be decided later).
    Note that index is 0-based.

    Some sentences may fail to generate images on Stable Diffusion.
    In that case, please make sure that another image is present for that index.
    """
    pass
