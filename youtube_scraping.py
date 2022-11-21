from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from functions import open_driver
from time import sleep


def search_video(driver, title):
    """Enter a search field and submit"""
    input_element = driver.find_element(By.ID, 'center').find_element(By.ID, 'search-form').find_element(By.TAG_NAME,
                                                                                                         'input')
    input_element.send_keys(title)
    input_element.send_keys(Keys.ENTER)


def check_current_link(driver, contents, video_num):
    """Check current link and if it changes close the browser"""
    while True:  # loop for playing video before link changes
        video_url = driver.current_url
        is_link_change = video_url != contents[video_num].get_attribute('href')
        if is_link_change:
            return False


def play_video(driver, video_num):
    """Get a video's link"""
    new_url = driver.current_url
    driver.get(new_url)
    sleep(0.1)
    contents = driver.find_elements(By.CSS_SELECTOR,
                                    '#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail')

    contents[video_num].click()
    return contents


def scrap_youtube(title, video_num):
    """Scraping youtube and play video"""
    driver = open_driver('https://www.youtube.com/')

    driver.implicitly_wait(10)

    search_video(driver, title)
    contents = play_video(driver, video_num)

    sleep(2)

    check_current_link(driver, contents, video_num)
