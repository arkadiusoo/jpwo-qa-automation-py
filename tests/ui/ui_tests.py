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
    return driver


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
