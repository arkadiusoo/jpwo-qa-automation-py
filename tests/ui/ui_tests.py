import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_go_to_main_by_logo(driver):
    driver.get("https://practicesoftwaretesting.com/product"
               "/01KA6SR9JG4P594K2BBFYFTG0E")
    wait = WebDriverWait(driver, 5)
    go_to_main = driver.find_element(By.ID, "Layer_1")
    go_to_main.click()

    time.sleep(2)
    current_url = driver.current_url
    print("Current URL after click:", current_url)
    assert current_url == "https://practicesoftwaretesting.com/"
    driver.quit()


def test_go_to_pliers(driver):
    driver.get("https://practicesoftwaretesting.com")
    time.sleep(2)
    wait = WebDriverWait(driver, 5)

    first_product = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".container a.card"))
    )
    first_product.click()

    time.sleep(2)
    current_url = driver.current_url
    print("Current URL after click:", current_url)

    assert current_url == ("https://practicesoftwaretesting.com"
                           "/product/01KA6X65BA07V2M7PMYABT38YV")

    driver.quit()

def test_login_success(driver):
    driver.get("https://practicesoftwaretesting.com/auth/login")

    wait = WebDriverWait(driver, 10)

    email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_input.send_keys("admin@practicesoftwaretesting.com")

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("welcome01")

    login_button = driver.find_element(By.CSS_SELECTOR, "input[data-test='login-submit']")
    login_button.click()

    sign_out_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='nav-sign-out']")))
    assert sign_out_btn.is_displayed()


def test_login_invalid_credentials(driver):
    driver.get("https://practicesoftwaretesting.com/auth/login")

    wait = WebDriverWait(driver, 10)

    email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_input.send_keys("wrong@mail.com")

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("badpassword")

    login_button = driver.find_element(By.CSS_SELECTOR, "input[data-test='login-submit']")
    login_button.click()

    error = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".alert.alert-danger")
        )
    )

    assert "Invalid email or password" in error.text

def test_add_to_cart_positive(driver):
    driver.get("https://practicesoftwaretesting.com/product"
               "/01KA6X65BES7CSX4Z0MJ7WVZ9V")
    wait = WebDriverWait(driver, 5)
    time.sleep(1)
    add_button = driver.find_element(By.ID, "btn-add-to-cart")
    add_button.click()
    time.sleep(1)
    driver.get("https://practicesoftwaretesting.com/checkout")
    time.sleep(1)
    proceed = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-success")))

    # Assert that the button is displayed
    assert proceed.is_displayed(), ("Proceed button is not visible on the "
                                    "checkout page")


def test_add_to_cart_negative(driver):
    driver.get("https://practicesoftwaretesting.com/product"
               "/01KA6X65BJ12S27D9YBQ3ZSMA8")
    wait = WebDriverWait(driver, 5)
    time.sleep(2)
    add_button = driver.find_element(By.ID, "btn-add-to-cart")
    assert not add_button.is_enabled(), ("Add to Cart button should be "
                                         "disabled for this product")
