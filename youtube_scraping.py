from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep


def open_driver(link) -> WebDriver:
    options = Options()
    options.add_argument("--start-maximized")  # full-screen with borders
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    return driver


def search_video(driver: WebDriver, title: str):
    """Enter a search field and submit"""
    input_element: WebElement = driver.find_element(By.ID, 'center').find_element(By.ID, 'search-form').find_element(By.TAG_NAME,
                                                                                                         'input')
    input_element.send_keys(title)
    input_element.send_keys(Keys.ENTER)


def check_current_link(driver: WebDriver, contents: list[WebElement], video_num: int) -> bool:
    """Check current link and if it changes close the browser"""
    while True:  # loop for playing video before link changes
        video_url: str = driver.current_url
        is_link_changes: bool = video_url != contents[video_num].get_attribute('href')
        if is_link_changes:
            return False


def play_video(driver, video_num) -> list[WebElement]:
    """Get a video's link"""
    new_url: str = driver.current_url
    driver.get(new_url)
    sleep(0.1)
    contents: list[WebElement] = driver.find_elements(By.CSS_SELECTOR,
                                    '#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail')

    contents[video_num].click()
    return contents


def scrap_youtube(title, video_num):
    """Scraping youtube and play video"""
    driver: WebDriver = open_driver('https://www.youtube.com/')

    driver.implicitly_wait(10)

    search_video(driver, title)
    contents: list[WebElement] = play_video(driver, video_num)

    sleep(2)

    check_current_link(driver, contents, video_num)
