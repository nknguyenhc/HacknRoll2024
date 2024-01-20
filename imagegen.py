import base64
import grequests
import os
import shutil
#import time

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
    os.makedirs(f"images/{vid_id}")

    # custom weights to important words
    #t0 = time.time()
    requests = []
    for i, sentence in enumerate(lyrics):
        body = {
            "steps": 40,
            "width": 1216,
            "height": 832,
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
    # t1 = time.time()
    # print("{} seconds used to generate images".format(t1 - t0))
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
        with open(f'images/{vid_id}/{i}.png', "wb") as f:
            f.write(base64.b64decode(image["base64"]))
    print("images ready")


def copy_placeholder(vid_id, index):
    shutil.copy('placeholder/placeholder.png', f'images/{vid_id}/{index}.png')


def test():
    generate_images([
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
    ], 'sample')


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    test()
