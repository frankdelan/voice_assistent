from functions import open_driver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time


def sign_in(driver, login, password):
    """Login to @mail.ru service"""
    frame = driver.find_element(By.CSS_SELECTOR, 'iframe')
    driver.switch_to.frame(frame)

    login_elem = driver.find_element(By.NAME, 'username')
    login_elem.send_keys(login)
    login_elem.send_keys(Keys.ENTER)

    password_elem = driver.find_element(By.NAME, 'password')
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.ENTER)
    driver.switch_to.default_content()


def write_a_letter(driver, mail, text):
    """Find elements for enter receiver and text"""
    new_window = driver.current_url
    driver.get(new_window)

    letter_btn = driver.find_element(By.CSS_SELECTOR,
                                     '.compose-button.compose-button_white.compose-button_base'
                                     '.compose-button_with-dropdown.js-shortcut')

    driver.execute_script("arguments[0].click();", letter_btn)  # button can't be clickable because of popup window

    popup_mail = get_popup_mail_field(driver)
    popup_mail.send_keys(mail)  # set a receiver

    outer_div = get_popup_text_field(driver)
    outer_div.send_keys(text)  # write a text

    driver.find_element(By.XPATH, "//div[@data-test-id='underlay-wrapper']/button").click()  # click SEND button
    time.sleep(3)


def get_popup_mail_field(driver):
    popup_mail = driver.find_element(By.CSS_SELECTOR, '.container--H9L5q.size_s--3_M-_')
    return popup_mail


def get_popup_text_field(driver):
    popup_text = driver.find_element(By.CSS_SELECTOR, '.container--2Rl8H')
    outer_div = popup_text.find_elements(By.TAG_NAME, 'div')[0].find_element(By.XPATH, '//div[@role="textbox"]')
    return outer_div


def scrap_mail(login, password, mail, text):
    """Scraping mail and sending letter"""
    driver = open_driver('https://e.mail.ru/login')

    driver.implicitly_wait(10)

    sign_in(driver, login, password)
    time.sleep(0.5)
    write_a_letter(driver, mail, text)
