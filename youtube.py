from pytube import YouTube
import xml.etree.ElementTree as ET

def get_title(yt_link):
    """Returns the title of the Youtube video in the given link.
    """
    try :
        yt = YouTube(yt_link)
    except:
        raise ValueError("Invalid URL")
    return yt.title

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

    yt = YouTube(yt_link)

    audio_streams = yt.streams.filter(only_audio=True, subtype="mp4")
    if len(audio_streams) == 0:
        raise ValueError("Video does not have any MP4 stream.")
    if len(yt.captions) == 0:
        raise ValueError("Video does not have any caption")
    
    # download video
    filename = f"{vid_id}.mp4"
    audio_streams[0].download(output_path="audio", filename=filename)

    # extract caption
    xml = list(yt.captions)[0].xml_captions
    tree = ET.ElementTree(ET.fromstring(xml))
    body = tree.getroot()[1]
    captions = preprocess_lines(body)
    lyrics = ""
    for line in captions:
        lyrics = lyrics + line["text"] + "\n"
    print(lyrics)

    return yt.title, captions


# TODO: avoid wordy comics
def preprocess_lines(body):
    '''
    Combine lines shorter than 5 seconds / 3 words.
    If it's last line, combine with previous line.
    '''
    lines = []
    line_template = {
        "start": 0,
        "duration": 0,
        "text": ""
    }
    shortest_duration_threshold = 3 # 3 seconds
    shortest_text_length_threshold = 2
    curr_line = line_template.copy()
    for line_dict in body:
        if curr_line["duration"] == 0:
            curr_line["start"] = float(line_dict.attrib['t']) / 1000
        curr_line["duration"] += float(line_dict.attrib['d']) / 1000

        text = line_dict.text.replace('♪', '').replace('\n', ' ').replace('  ', ' ').strip()
        if curr_line["text"] != "":
            curr_line["text"] += " " + text
        else:
            curr_line["text"] = text
        
        if curr_line["duration"] < shortest_duration_threshold or len(curr_line["text"].split(" ")) < shortest_text_length_threshold:
            continue
        else:
            lines.append(curr_line)
            curr_line = line_template.copy() 
    if curr_line["duration"] != 0:
        lines[-1]["duration"] += curr_line["duration"]
        lines[-1]["text"] += " " + curr_line["text"]
    return lines


def test():
    print(get_caption('https://www.youtube.com/watch?v=3Uo0JAUWijM', 'sample'))


if __name__ == '__main__':
    test()
