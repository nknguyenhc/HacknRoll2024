import base64
import grequests
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

IMAGE_WIDTH = 1216
IMAGE_HEIGHT = 832
SUBTITLE_HEIGHT = 720
SUBS_FONT_FILENAME = "./subs_font.ttf"
SUBS_FONT_SIZE = 24
SUBS_BORDER_COLOR = "blue"

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
    For example, image that corresponds to sentence index 9 must be named `9.png`.
    Note that index is 0-based.

    Some sentences may fail to generate images on Stable Diffusion.
    In that case, please make sure that another image is present for that index.
    """

    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('STABLE_DIFFUSION_KEY')}",
    }
    os.makedirs(os.path.join(os.path.dirname(__file__), f"images/{vid_id}"))

    # custom weights to important words
    requests = []
    for i, sentence in enumerate(lyrics):
        body = {
            "steps": 40,
            "width": IMAGE_WIDTH,
            "height": IMAGE_HEIGHT,
            "seed": 0,
            "cfg_scale": 10,
            "samples": 1,
            "text_prompts": [
                {
                    "text": sentence["text"]
                },
            ],
        }
        requests.append(grequests.post(
            url,
            headers=headers,
            json=body
        ))
    responses = grequests.map(requests)
    for i, response in enumerate(responses):
        if response is None:
            print("None response")
            copy_placeholder(vid_id, i)
            continue
        if response.status_code != 200:
            print(response.json())
            copy_placeholder(vid_id, i)
            continue
        
        data = response.json()
        image = data["artifacts"][0]
        filename = os.path.join(os.path.dirname(__file__), f'images/{vid_id}/{i}.png')
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
        add_subtitle(filename, lyrics[i]["text"])
        
    print("images ready")


def add_subtitle(filename, text):
    font = ImageFont.truetype(SUBS_FONT_FILENAME, SUBS_FONT_SIZE)
    output = Image.open(filename)
    image = ImageDraw.Draw(output)
    _, _, w, h = image.textbbox((0, 0), text, font)
    w_start = (IMAGE_WIDTH - w) / 2
    image.text((w_start-1, SUBTITLE_HEIGHT-1), text, font=font, fill=SUBS_BORDER_COLOR)
    image.text((w_start+1, SUBTITLE_HEIGHT-1), text, font=font, fill=SUBS_BORDER_COLOR)
    image.text((w_start-1, SUBTITLE_HEIGHT+1), text, font=font, fill=SUBS_BORDER_COLOR)
    image.text((w_start+1, SUBTITLE_HEIGHT+1), text, font=font, fill=SUBS_BORDER_COLOR)
    image.text((w_start, SUBTITLE_HEIGHT), text, fill=None, font=font)
    output.save(filename)


def copy_placeholder(vid_id, index):
    shutil.copy(
        os.path.join(os.path.dirname(__file__), 'placeholder/placeholder.png'), 
        os.path.join(os.path.dirname(__file__), f'images/{vid_id}/{index}.png'),
    )


def test():
    generate_images([
        {
            "start": 1.395,
            "duration": 4.931,
            "text": "Just gonna stand there and watch me burn"
        }, 
        {
            "start": 6.326,
            "duration": 5.000,
            "text": "Well, that's alright, because I like the way it hurts"
        },
    ], 'samplee')


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    test()
