import logging
import os
import sys
import traceback

from pytube import YouTube
from selenium.common.exceptions import NoSuchWindowException

from app.config import PATH_MP4, get_driver

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))


def download_video(video_yt, only_audio=False, title=None):
    if title is None:
        title = video_yt.title
    video_yt.streams.filter(only_audio=only_audio, file_extension='mp4').first().download(PATH_MP4, filename=title)

    return title


def check_not_exist_video(title):
    return not bool(os.path.isfile(f'{PATH_MP4}/{title}.mp4'))


def main(only_audio):
    logger.debug(f"init module")
    driver = get_driver()
    driver.get("https://www.youtube.com/")
    last_url = None
    black_list = ["https://www.youtube.com/"]
    bar = True
    logger.debug(f"ok load driver")
    while bar:
        try:
            url = driver.current_url

            if last_url != url and "https://www.youtube.com/watch?v=" in url:
                if url not in black_list:
                    yt = YouTube(url)
                    title = yt.title.replace(" ", "_").replace("-", "_").lower().replace("__", "_")

                    logger.debug(f"detect new video: {title}")
                    last_url = url
                    if check_not_exist_video(title):
                        download_video(yt, only_audio, title=title)
                        logger.debug(f"video: {title} save")
                    else:
                        logger.debug(f"video: {title} exist")

        except KeyError:
            logger.error(f"impossible download {url}")
            black_list.append(url)

        except NoSuchWindowException:
            bar = False

        except Exception as ex:
            traceback.print_exc()
            logger.error(ex)
