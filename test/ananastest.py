import pytest
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
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

def close_popup(driver):
    wait = WebDriverWait(driver, 30)
    try:
        close_btn=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dy-lb-close[aria-label='Close']")))
        driver.execute_script("arguments[0].click();", close_btn)

    except Exception as e:
        print(e)



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

    driver.find_element(By.ID,"email").send_keys("charde2@townpostmail.com")
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

def test_ananas_click_contact_us_form(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    contact_us_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Piši nam")))
    contact_us_link.click()
    time.sleep(0.5)
    contact_us_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Korisnička podrška" in contact_us_heading, "Error"

def test_ananas_click_order_status(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    delivery_status_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Status porudžbine")))
    driver.execute_script("arguments[0].click();", delivery_status_link)
    time.sleep(1)

    delivery_status_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h1"))).text
    assert "Porudžbine i reklamacije" in delivery_status_heading, f"❌ Expected 'Porudžbine i reklamacije' in: '{delivery_status_heading}'"

def test_ananas_click_order_status_logged_in(driver):
    login(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)
    time.sleep(1)
    delivery_status_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Status porudžbine")))
    driver.execute_script("arguments[0].click();", delivery_status_link)
    time.sleep(1)

    element = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//span[contains(@class, 'MuiTab-wrapper') and contains(text(), 'Moje porudžbine')]")
    ))


    assert "Moje porudžbine" in element.text, "❌ 'Moje porudžbine' text not found"

def test_ananas_click_wishlist_functionality(driver):
    login(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    wishlist_link = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[contains(@href, 'lista-zelja')]")
    ))

    driver.execute_script("arguments[0].click();", wishlist_link)

    time.sleep(2)

    wish_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Poželi želju']")))

    # Click the button
    wish_button.click()

    result_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h1"))).text
    assert "Sve kategorije" in result_heading, "Error"

def test_ananas_click_cart_link(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)
    cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/korpa']")))
    cart.click()

    time.sleep(0.5)

    cart_link_result=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h6"))).text
    assert "Tvoja korpa je prazna." in cart_link_result, "Error"

def test_ananas_navigate_to_laptopovi_via_it_shop_dropdown(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    menu_button=wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Sve kategorije')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'start',inline:'start'});", menu_button)
    actions=ActionChains(driver)
    actions.move_to_element(menu_button).perform()
    time.sleep(1)
    it_shop = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='IT Shop']")))


    actions = ActionChains(driver)
    actions.move_to_element(it_shop).perform()

    # Now you can wait for and click one of the submenu items, e.g.
    submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Laptopovi']")))  # adjust text
    submenu.click()

    submenu_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Laptopovi" in submenu_heading, f"Expected heading 'Laptopovi' not found{submenu_heading}"

def test_ananas_navigate_to_sport_and_recreation_and_click_football_jersey(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    menu_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Sve kategorije')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'start',inline:'start'});", menu_button)
    actions = ActionChains(driver)
    actions.move_to_element(menu_button).perform()
    time.sleep(1)

    sar_el = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Sport i rekreacija']")))
    actions = ActionChains(driver)
    actions.move_to_element(sar_el).perform()

    submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Dresovi za fudbal']")))  # adjust text
    submenu.click()

    sar_el_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Dresovi za fudbal" in sar_el_heading, f"Expected heading 'Dresovi za fudbal' not found{sar_el_heading}"

def test_ananas_add_payment_cart(driver):
    login(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)
    username = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Bojan')]")))

    actions = ActionChains(driver)
    actions.move_to_element(username).perform()
    time.sleep(1)

    payment_cart =wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Platne kartice')]")))
    driver.execute_script("arguments[0].click();", payment_cart)
    time.sleep(1)

    add_cart=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"sc-17u2v5y-4")))
    driver.execute_script("arguments[0].click();", add_cart)
    time.sleep(1)

    cart_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h6"))).text
    assert "Dodaj novu karticu" in cart_heading, "Expected 'Dodaj novu karticu' text not found on the page"

def test_ananas_settings_my_profile(driver):
    login(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)
    username = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Bojan')]")))

    actions = ActionChains(driver)
    actions.move_to_element(username).perform()
    time.sleep(1)

    account = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Podešavanje naloga')]")))
    driver.execute_script("arguments[0].click();", account)
    time.sleep(1)

    edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Izmeni podatke']")))
    edit_button.click()
    time.sleep(1)

    phone=driver.find_element(By.ID, "phone")
    phone.clear()
    phone.send_keys("123456")
    time.sleep(1)
    day=driver.find_element(By.ID,"day")
    day.clear()
    day.send_keys("10")

    month=driver.find_element(By.ID, "month")
    month.clear()
    month.send_keys("02")
    year=driver.find_element(By.ID, "year")
    year.clear()
    year.send_keys("1989")
    year.send_keys(Keys.TAB)

    time.sleep(0.5)

    radio = driver.find_element(By.CSS_SELECTOR, "input[name='gender'][value='male']")
    driver.execute_script("arguments[0].click();", radio)

    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sačuvaj izmene')]")))
    save_button.click()

def test_ananas_search_trambolina(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    search_input=wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'aa-Input')))
    search_input.send_keys("trambolina")

    search_input.send_keys(Keys.ENTER)

    result_title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.sc-1thjabt-0.gnAzSX")))
    assert 'Rezultati za "trambolina"' in result_title.text

def test_ananas_click_products_on_sale(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    akcija_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Akcija")))
    driver.execute_script("arguments[0].click()",akcija_link)

    heading = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//h1[contains(text(), 'Proizvodi na akciji')]"
    )))
    assert "Proizvodi na akciji" in heading.text, f"Expected heading to contain 'Proizvodi na akciji', but got: '{heading.text}'"

def test_ananas_click_pools_shows_pools_page(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    bazeni_link=wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"Bazeni")))
    bazeni_link.click()
    time.sleep(1)
    bazeni_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h1"))).text

    assert "Bazeni" in bazeni_heading,"Expected 'Bazeni' in bazeni_heading"

def test_ananas_click_newest_products_shows_newest_page(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    najnovije_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Najnovije")))
    driver.execute_script("arguments[0].click()",najnovije_link)
    time.sleep(1)
    najnovije_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text

    assert "Najnoviji Proizvodi" in najnovije_heading, "Expected 'Najnoviji proizvodi' in najnovije_heading"

def test_ananas_click_all_products_shows_all_page(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    all_products_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Svi proizvodi")))
    driver.execute_script("arguments[0].click()", all_products_link)
    time.sleep(1)
    all_products_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text

    assert "Svi proizvodi" in all_products_heading, f"Expected 'Svi proizvodi' in {all_products_heading}"

def test_ananas_click_best_sellers_shows_best_sellers_page(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    najprodavanije_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Najprodavanije")))
    driver.execute_script("arguments[0].click()",najprodavanije_link)
    time.sleep(1)
    najprodavanije_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text

    assert "Najprodavanije" in najprodavanije_heading, "Expected 'Najprodavanije' in najprodavanije_heading"

def test_ananas_click_sell_on_ananas(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    sell_ananas_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Prodaj na Ananasu")))
    driver.execute_script("arguments[0].click()", sell_ananas_link)
    sell_ananas_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text

    assert "Želiš da prodaješ na Ananasu?" in sell_ananas_heading, f"Expected 'Želiš da prodajes na Ananasu?' in sell_ananas_heading"

def test_search_simpo_click_miran_san_add_to_cart(driver):
    login(driver)
    close_popup(driver)

    wait = WebDriverWait(driver, 30)

    search_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'aa-Input')))
    search_input.clear()
    search_input.send_keys("simpo krevet")
    search_input.send_keys(Keys.ENTER)

    product_link = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//h3[contains(text(),'SIMPO Krevet Miran san 200x140 fiksni, Bež')]/ancestor::a"
    )))

    # Scroll into view (optional but good practice)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product_link)

    driver.execute_script("arguments[0].click();", product_link)

    time.sleep(1)
    add_to_cart_button = wait.until(EC.visibility_of_element_located((By.XPATH,"//button[text()='Dodaj u korpu']")))
    driver.execute_script("arguments[0].click()", add_to_cart_button)

    product_added_to_cart = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//p[contains(text(), 'Proizvod je dodat u korpu.')]")
    ))

    assert product_added_to_cart.is_displayed()

def test_search_inverter_aircondition_click_and_remove_from_cart(driver):
    login(driver)
    close_popup(driver)

    wait = WebDriverWait(driver, 30)

    search_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'aa-Input')))
    search_input.clear()
    search_input.send_keys("inverter klima")
    search_input.send_keys(Keys.ENTER)

    product_link = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//h3[contains(text(),'FOX FAC-12INTC52, Inverter klima, Wi-Fi, bela')]/ancestor::a"
    )))

    # Scroll into view (optional but good practice)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product_link)

    driver.execute_script("arguments[0].click();", product_link)

    time.sleep(1)
    add_to_cart_button = wait.until(EC.visibility_of_element_located((By.XPATH,"//button[text()='Dodaj u korpu']")))
    driver.execute_script("arguments[0].click()", add_to_cart_button)


    view_cart_button=wait.until(EC.visibility_of_element_located((By.XPATH,"//button[text()='Pregledaj korpu']")))
    driver.execute_script("arguments[0].click()", view_cart_button)

    remove_button = wait.until(EC.visibility_of_element_located((By.XPATH,"//button[text()='Ukloni proizvod']")))
    driver.execute_script("arguments[0].click()", remove_button)



    product_remove_from_cart_msg = wait.until(EC.visibility_of_element_located(
         (By.XPATH, "//p[contains(text(), 'Proizvod je uklonjen iz korpe.')]")
     ))

    assert product_remove_from_cart_msg.is_displayed()

def test_click_delivery_info_link(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    delivery_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Dostava robe i načini plaćanja")))

    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", delivery_link)

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Dostava robe i načini plaćanja")))


    driver.execute_script("arguments[0].click();", delivery_link)
    delivery_info_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Dostava robe i načini plaćanja" in delivery_info_heading,"Error"

def test_ananas_click_about_us_link(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    about_us_click=wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"O nama")))
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", about_us_click)

    driver.execute_script("arguments[0].click();", about_us_click)
    time.sleep(1)

    about_us=wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Klik! Bum! Tras! Svi smo mi Ananas!" in about_us,f"❌ Expected slogan not found! Got: '{about_us}'"

def test_ananas_click_ananas_club_link(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    ananas_club_click = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "ānanas+ klub")))
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", ananas_club_click)

    driver.execute_script("arguments[0].click();", ananas_club_click)
    time.sleep(1)

    ananas_club_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Ananas + klub" in ananas_club_heading,f"❌ Expected heading not found! Got: '{ananas_club_heading}'"

def test_ananas_click_brands_link(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    brands_click = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Brendovi")))
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", brands_click)

    driver.execute_script("arguments[0].click();", brands_click)
    time.sleep(1)

    brands_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Brendovi na Ananasu" in brands_heading, f"❌ Expected slogan not found! Got: '{brands_heading}'"

def test_ananas_click_delivery_and_payment_options_link(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    dap_click = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Dostava robe i načini plaćanja")))
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", dap_click)

    driver.execute_script("arguments[0].click();", dap_click)
    time.sleep(1)

    dap_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Dostava robe i načini plaćanja" in dap_heading, f"❌ Expected heading not found! Got: '{dap_heading}'"

def test_ananas_click_youtube_link(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    youtube_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[aria-label='Youtube']")))
    driver.execute_script("arguments[0].click();", youtube_link)

def test_ananas_click_linkedin_link(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    linkedIn_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='LinkedIn']")))

    actions = ActionChains(driver)
    actions.move_to_element(linkedIn_link).perform()
    linkedIn_link.click()

def test_ananas_click_ananas_seller_academy_link(driver):
    accept_cookies(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)

    seller_click = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Ananas Seller Akademija")))
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", seller_click)

    driver.execute_script("arguments[0].click();", seller_click)
    time.sleep(1)

    dap_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Unapredi svoje poslovanje sa Ananas Seller Akademijom" in dap_heading, f"❌ Expected heading not found! Got: '{dap_heading}'"

def test_ananas_logout(driver):
    login(driver)
    close_popup(driver)
    wait = WebDriverWait(driver, 30)
    username = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Bojan')]")))

    actions = ActionChains(driver)
    actions.move_to_element(username).perform()
    time.sleep(1)

    logout = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Odjavi se')]")))
    driver.execute_script("arguments[0].click();", logout)
    time.sleep(1)

    logout_result = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH,
             "//*[contains(normalize-space(.), 'Napravi nalog') and contains(normalize-space(.), 'Prijavi se')]")
        )
    ).text

    assert "Napravi nalog" in logout_result, "❌ Logout failed — text not found"




































