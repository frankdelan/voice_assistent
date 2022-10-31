from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from time import sleep


def scrap(title, video_num):
    """Scraping youtube and play video"""
    global driver  # browser doesn't close
    driver = webdriver.Chrome()

    driver.get('https://www.youtube.com/')
    input_element = driver.find_element(By.ID, 'center').find_element(By.ID, 'search-form').find_element(By.TAG_NAME,
                                                                                                         'input')
    input_element.send_keys(title)
    input_element.send_keys(Keys.ENTER)

    new_url = driver.current_url
    driver.get(new_url)
    sleep(2)
    contents = driver.find_elements(By.CSS_SELECTOR,
                                    '#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail')

    contents[video_num].click()
    # video_urls = []
    # for item in contents:
    #     video_urls.append(item.get_attribute('href'))
    #
    # my_video = video_urls[video_num]
    #
    # driver.get(my_video)
