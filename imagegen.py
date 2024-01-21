import base64
import grequests
import os
import shutil
import textwrap
from PIL import Image, ImageDraw, ImageFont

IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 576
SUBS_CENTER_HEIGHT = 510
SUBS_FONT_FILENAME = os.path.join(os.path.dirname(__file__), "subs_font.ttf")
SUBS_FONT_SIZE = 20
SUBS_MAX_CHARS_PER_LINE = 70
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

    url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
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
            "cfg_scale": 12,
            "samples": 1,
            "text_prompts": [
                {
                    "text": sentence["text"],
                    "weight": 1
                },
                {
                    "text": "blurry, bad, text, horror, disgusting, NSFW, disfigured, nude",
                    "weight": -1
                }
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
            print(f"For prompt: {lyrics[i]['text']}")
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
    filepath = os.path.join(os.path.dirname(__file__), filename)
    output = Image.open(filepath)
    image = ImageDraw.Draw(output)
    lines = textwrap.wrap(text, SUBS_MAX_CHARS_PER_LINE)
    _, _, _, line_h = font.getbbox(lines[0])
    total_h = line_h * len(lines)
    start_h = SUBS_CENTER_HEIGHT - total_h / 2
    curr_h = start_h
    for line in lines:
        _, _, w, _ = font.getbbox(line)
        start_w = (IMAGE_WIDTH - w) / 2
        image.text((start_w-1, curr_h-1), text=line, font=font, fill=SUBS_BORDER_COLOR)
        image.text((start_w+1, curr_h-1), text=line, font=font, fill=SUBS_BORDER_COLOR)
        image.text((start_w-1, curr_h+1), text=line, font=font, fill=SUBS_BORDER_COLOR)
        image.text((start_w+1, curr_h+1), text=line, font=font, fill=SUBS_BORDER_COLOR)
        image.text((start_w, curr_h), text=line, font=font, fill=None)
        curr_h += line_h
    output.save(filepath)


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
