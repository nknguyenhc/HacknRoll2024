from youtube import get_caption
from imagegen import generate_images
from videogen import generate_video

LOVE_THE_WAY_YOU_LIE_URL = 'https://www.youtube.com/watch?v=uelHwf8o7_U'
HAPPY_NEW_YEAR_URL = 'https://www.youtube.com/watch?v=3Uo0JAUWijM'
INTO_THE_UNKNOWN_URL = 'https://www.youtube.com/watch?v=gIOyB9ZXn8s'
SNOWMAN_URL = 'https://www.youtube.com/watch?v=gset79KMmt0'
COUNTING_STARS_URL = 'https://www.youtube.com/watch?v=hT_nvWreIhg'
ANIMALS_URL = 'https://www.youtube.com/watch?v=qpgTC9MDx1o'
PERFECT_URL = 'https://www.youtube.com/watch?v=2Vv-BfVoq4g'
SEE_YOU_AGAIN_URL = 'https://www.youtube.com/watch?v=RgKAFK5djSk'
FLY_AWAY_URL = 'https://www.youtube.com/watch?v=cMg8KaMdDYo'
CLOSE_TO_THE_SUN_URL = 'https://www.youtube.com/watch?v=oJuGlqO85YI'
IMPOSTER_IMPERCEPTIBLE_URL = 'https://www.youtube.com/watch?v=KByREO4gB0M'
LEGENDS_NEVER_DIE_URL = 'https://www.youtube.com/watch?v=r6zIGXun57U'
THE_NIGHTS_URL = 'https://www.youtube.com/watch?v=UtF6Jej8yb4'

def from_yt(yt_link, vid_id):
    """Generate a parody video based on the Youtube video and the video ID.
    The ID is internally generated in this server.

    The video is named `f"vidoes/{vid_id}.mp4"`.
    """

    title, lyrics = get_caption(yt_link, vid_id)
    generate_images(lyrics, vid_id)
    print("generate_video")
    generate_video(lyrics, vid_id)


def test():
    from_yt(THE_NIGHTS_URL, 'sample15')


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    test()
