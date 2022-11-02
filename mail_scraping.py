from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
                                     '.compose-button.compose-button_white.compose-button_base.compose-button_with-dropdown.js-shortcut')
    driver.execute_script("arguments[0].click();", letter_btn)  # button can't be clickable because of popup window

    popup_mail = driver.find_element(By.CSS_SELECTOR, '.container--H9L5q.size_s--3_M-_')
    popup_mail.send_keys(mail)  # set a receiver

    popup_text = driver.find_element(By.CSS_SELECTOR, '.container--2Rl8H')
    outer_div = popup_text.find_elements(By.TAG_NAME, 'div')[0]
    upper_div = outer_div.find_element(By.XPATH, '//div[@role="textbox"]')
    upper_div.send_keys(text)  # write a text

    driver.find_element(By.CSS_SELECTOR, '.base-0-2-14.primary-0-2-28').click()  # click SEND button
    time.sleep(3)


def scrap_mail(login, password, mail, text):
    """Scraping mail and sending letter"""
    options = Options()
    options.add_argument("--start-maximized")  # fullscreen with borders
    driver = webdriver.Chrome(options=options)
    driver.get('https://e.mail.ru/login')

    driver.implicitly_wait(10)

    sign_in(driver, login, password)
    write_a_letter(driver, mail, text)


if __name__ == "__main__":
    scrap_mail()