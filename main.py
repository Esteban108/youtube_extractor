from config import *
from selenium import webdriver

from pytube import YouTube
import os
import pyperclip
import traceback

from moviepy.editor import VideoFileClip


def video_to_mp3(video_name):
    v = VideoFileClip(os.path.join(PATH_MP4, f"{video_name}.mp4"))
    v.audio.write_audiofile(os.path.join(PATH_MP3, f"{video_name}.mp3"))


def download_video(video_yt, only_audio=False, title=None):
    if title is None:
        title = video_yt.title
    video_yt.streams.filter(only_audio=only_audio, file_extension='mp4').first().download(PATH_MP4, filename=title)

    return title


def download_and_convert(yt_video, only_audio, save_mp3=True, title=None):
    print("start download")
    title = download_video(yt_video, only_audio=only_audio, title=title)
    print("end download")
    if save_mp3:
        video_to_mp3(title)
    print("new video save")


def read_clipboard_and_detect_video():
    text = pyperclip.paste()

    if "https://www.youtube.com/" in text:
        return text
    else:
        return None


def check_not_exist_video(title):

    return not bool(os.path.isfile(f'{PATH_MP4}/{title}.mp4'))


def main(only_audio):
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com/")
    last_url = None
    black_list = ["https://www.youtube.com/"]
    while True:
        try:
            url = driver.current_url

            if last_url != url and "https://www.youtube.com/watch?v=" in url:
                if url not in black_list:
                    yt = YouTube(url)
                    title = yt.title.replace(" ", "_").replace("-", "_").lower()
                    print(f"detect new video: {title}")
                    last_url = url
                    if check_not_exist_video(title):
                        download_and_convert(yt, only_audio, save_mp3=False, title=title)

                    else:
                        print(f"video: {title} exist")

        except KeyError:
            print(f"impossible download {url}")
            print("solution here https://github.com/nficano/pytube/issues/467")
            black_list.append(url)

        except Exception as ex:
            traceback.print_exc()
            print(ex)


main(False)
