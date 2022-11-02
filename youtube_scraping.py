from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep


def search_video(driver, title):
    """Enter a search field and submit"""
    input_element = driver.find_element(By.ID, 'center').find_element(By.ID, 'search-form').find_element(By.TAG_NAME,                                                                             'input')
    input_element.send_keys(title)
    input_element.send_keys(Keys.ENTER)


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
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.youtube.com/')

    driver.implicitly_wait(10)

    search_video(driver, title)
    contents = play_video(driver, video_num)

    sleep(2)

    while True:  # loop for playing video before link changes
        video_url = driver.current_url
        if video_url == contents[video_num].get_attribute('href'):
            pass
        else:
            return False


if __name__ == "__main__":
    scrap_youtube()