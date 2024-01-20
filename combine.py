from youtube import get_caption
from imagegen import generate_images
from videogen import generate_video

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
    from_yt('https://www.youtube.com/watch?v=uelHwf8o7_U', 'sample')


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    test()
