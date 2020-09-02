import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PATH_MP4 = f"{os.getcwd()}/videos"


def get_driver() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/brave"
    remote = os.environ.get('SELENIUM', None)
    if remote:
        return webdriver.Remote(os.environ['SELENIUM'], chrome_options.to_capabilities())

    return webdriver.Chrome(options=chrome_options)
