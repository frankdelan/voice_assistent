from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from functions import open_driver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time


def sign_in(driver: WebDriver, login: str, password: str) -> None:
    """Login to @mail.ru service"""
    frame: WebElement = driver.find_element(By.CSS_SELECTOR, 'iframe')
    driver.switch_to.frame(frame)

    login_elem = driver.find_element(By.NAME, 'username')
    login_elem.send_keys(login)
    login_elem.send_keys(Keys.ENTER)

    password_elem = driver.find_element(By.NAME, 'password')
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.ENTER)
    driver.switch_to.default_content()


def write_a_letter(driver: WebDriver, mail: str, text: str) -> None:
    """Find elements for enter receiver and text"""
    new_window: str = driver.current_url
    driver.get(new_window)

    letter_btn: WebElement = driver.find_element(By.CSS_SELECTOR,
                                                 '.compose-button.compose-button_white.compose-button_base'
                                                 '.compose-button_with-dropdown.js-shortcut')

    driver.execute_script("arguments[0].click();", letter_btn)

    popup_mail: WebElement = get_popup_mail_field(driver)
    popup_mail.send_keys(mail)

    outer_div: WebElement = get_popup_text_field(driver)
    outer_div.send_keys(text)

    driver.find_element(By.XPATH, "//div[@data-test-id='underlay-wrapper']/button").click()
    time.sleep(3)


def get_popup_mail_field(driver: WebDriver) -> WebElement:
    popup_mail: WebElement = driver.find_element(By.CSS_SELECTOR, '.container--H9L5q.size_s--3_M-_')
    return popup_mail


def get_popup_text_field(driver: WebDriver) -> WebElement:
    popup_text: WebElement = driver.find_element(By.CSS_SELECTOR, '.container--2Rl8H')
    outer_div: WebElement = popup_text.find_elements(By.TAG_NAME, 'div')[0].find_element(By.XPATH,
                                                                                         '//div[@role="textbox"]')
    return outer_div


def scrap_mail(data: dict, mail: str, text: str) -> None:
    """Scraping mail and sending letter"""
    driver: WebDriver = open_driver('https://e.mail.ru/login')

    driver.implicitly_wait(10)

    sign_in(driver, data['login'], data['password'])
    time.sleep(0.5)
    write_a_letter(driver, mail, text)
