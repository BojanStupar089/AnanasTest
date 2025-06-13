import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time


@pytest.fixture()
def driver():
    chrome_options = Options()

    prefs = {
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    ch_driver = webdriver.Chrome(service=Service('C:/Windows/chromedriver-win64/chromedriver.exe'))
    ch_driver.maximize_window()
    ch_driver.get('https://ananas.rs/')
    wait=WebDriverWait(ch_driver, 50)

    yield ch_driver
    ch_driver.quit()

def accept_cookies(driver):
    wait=WebDriverWait(driver, 30)
    cookies =wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Slažem se']")))
    cookies.click()

def login(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys("bojanstupar089@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Celarevo44!")
    driver.find_element(By.ID, "login-submit").click()



def test_open_google_and_go_to_ananas(driver):

    accept_cookies(driver)
    img=driver.find_element(By.CSS_SELECTOR,"img[alt='Ananas E-Commerce']")
    assert img.is_displayed(),"Error"

def test_register_successful_on_ananas(driver):

    accept_cookies(driver)
    wait=WebDriverWait(driver, 30)
    login_link=wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,"Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[span[contains(text(), 'Registruj se')]]")))
    register_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID,"email").send_keys("minos23654@finfave.com")
    driver.find_element(By.ID,"firstName").send_keys("Bojan")
    driver.find_element(By.ID,"lastName").send_keys("Stupar")
    driver.find_element(By.NAME,"password").send_keys("Celarevo44!")
    checkbox = driver.find_element(By.NAME, "privacyPolicy")
    driver.execute_script("arguments[0].click();", checkbox)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    submit_button.click()

    heading = wait.until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Verifikuj svoju email adresu']"))).text
    assert "Verifikuj svoju email adresu" in heading, "Verification heading is not visible!"

def test_register_required_fields_validation_on_ananas(driver):
    accept_cookies(driver)
    wait=WebDriverWait(driver, 30)

    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[span[contains(text(), 'Registruj se')]]")))
    register_link.click()

    wait.until(EC.visibility_of_element_located((By.ID,"email")))

    driver.find_element(By.ID, "email").send_keys("")
    driver.find_element(By.ID, "firstName").send_keys("")
    driver.find_element(By.ID, "lastName").send_keys("")
    driver.find_element(By.NAME, "password").send_keys("")
    checkbox = driver.find_element(By.NAME, "privacyPolicy")
    driver.execute_script("arguments[0].click();", checkbox)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    submit_button.click()

    error_message = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//p[text()='Ovo polje je obavezno.']")
    ))


    assert error_message.is_displayed(), "Error message is not displayed!"

def test_register_email_already_exists(driver):
    accept_cookies(driver)
    wait=WebDriverWait(driver, 30)

    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[span[contains(text(), 'Registruj se')]]")))
    register_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("bojanstupar089@gmail.com")
    driver.find_element(By.ID, "firstName").send_keys("Bojan")
    driver.find_element(By.ID, "lastName").send_keys("Stupar")
    driver.find_element(By.NAME, "password").send_keys("Celarevo44!")
    checkbox = driver.find_element(By.NAME, "privacyPolicy")
    driver.execute_script("arguments[0].click();", checkbox)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    submit_button.click()

    email_taken = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//p[contains(text(), 'Email je zauzet.')]")
    ))


    assert email_taken.is_displayed()

def test_register_email_invalid_format(driver):
    accept_cookies(driver)
    wait=WebDriverWait(driver, 30)

    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[span[contains(text(), 'Registruj se')]]")))
    register_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("boki")

    driver.find_element(By.ID, "firstName").send_keys("Bojan")
    driver.find_element(By.ID, "lastName").send_keys("Stupar")
    driver.find_element(By.NAME, "password").send_keys("Celarevo44!")
    checkbox = driver.find_element(By.NAME, "privacyPolicy")
    driver.execute_script("arguments[0].click();", checkbox)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    submit_button.click()






    error_msg = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//p[contains(text(), 'Email adresa nije ispravna.')]")
    ))

    assert error_msg.is_displayed()

def test_register_first_name_and_last_name_invalid_format(driver):
    accept_cookies(driver)
    wait=WebDriverWait(driver, 30)

    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[span[contains(text(), 'Registruj se')]]")))
    register_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("bojanstupar1989+test1@gmail.com")

    driver.find_element(By.ID, "firstName").send_keys("B")
    driver.find_element(By.ID, "lastName").send_keys("S")
    driver.find_element(By.NAME, "password").send_keys("Celarevo44!")
    checkbox = driver.find_element(By.NAME, "privacyPolicy")
    driver.execute_script("arguments[0].click();", checkbox)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    submit_button.click()

    error_msg = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//p[contains(text(), 'Minimum 2 karaktera.')]")
    ))

    assert error_msg.is_displayed()

def test_register_password_invalid_format(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[span[contains(text(), 'Registruj se')]]")))
    register_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("bojanstupar1989+test1@gmail.com")

    driver.find_element(By.ID, "firstName").send_keys("Bojan")
    driver.find_element(By.ID, "lastName").send_keys("Stupar")
    driver.find_element(By.NAME, "password").send_keys("Cela")
    checkbox = driver.find_element(By.NAME, "privacyPolicy")
    driver.execute_script("arguments[0].click();", checkbox)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    submit_button.click()

    error_msg = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//p[contains(text(), 'Minimum 8 karaktera.')]")
    ))

    assert error_msg.is_displayed()

def test_register_button_is_disabled(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[span[contains(text(), 'Registruj se')]]")))
    register_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").send_keys("bojanstupar1989+test1@gmail.com")

    driver.find_element(By.ID, "firstName").send_keys("Bojan")
    driver.find_element(By.ID, "lastName").send_keys("Stupar")
    driver.find_element(By.NAME, "password").send_keys("Cela")

    register_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Registruj se')]")

    assert not register_button.is_enabled()

def test_login_successful(driver):

    login(driver)
    wait = WebDriverWait(driver, 30)

    username_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Bojan')]"))).text
    assert username_text == "Bojan", f"Expected username 'Bojan', but got '{username_text}'"

def test_login_required_fields(driver):

    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys("")
    driver.find_element(By.ID, "password").send_keys("")
    driver.find_element(By.ID, "login-submit").click()

    error = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//*[contains(text(), 'Ovo polje je obavezno.')]"
    )))
    assert "Ovo polje je obavezno." in error.text, f"Unexpected error message: {error.text}"

def test_login_email_invalid_format(driver):

    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys("bojan")
    driver.find_element(By.ID, "password").send_keys("Celarevo44!")
    driver.find_element(By.ID, "login-submit").click()

    error = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//*[contains(text(), 'Email adresa nije ispravna.')]"
    )))

    assert "Email adresa nije ispravna." in error.text, f"Unexpected error message: {error.text}"


def test_login_password_invalid_format(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys("bojanstupar089@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Cela")
    driver.find_element(By.ID, "login-submit").click()

    error = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//*[contains(text(), 'Minimum 8 karaktera.')]"
    )))

    assert "Minimum 8 karaktera." in error.text, f"Unexpected error message: {error.text}"

def test_login_bad_credentials(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys("bojanstupar089@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Celarevo89")
    driver.find_element(By.ID, "login-submit").click()

    error = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//*[contains(text(), 'Email ili lozinka nisu u redu.')]"
    )))

    assert "Email ili lozinka nisu u redu." in error.text, f"Unexpected error message: {error.text}"

def test_login_click_forget_password_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    login_link = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Napravi nalog")))
    driver.execute_script("arguments[0].click();", login_link)

    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys("bojan")

    forgot_password_link = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//a[.//span[text()='Zaboravili ste lozinku?']]"
    )))
    forgot_password_link.click()

    wait.until(EC.visibility_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, "email").send_keys("bojanstupar089@gmail.com")
    driver.find_element(By.ID, "login-submit").click()































