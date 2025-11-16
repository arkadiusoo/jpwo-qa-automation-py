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
    wait = WebDriverWait(driver, 15)
    go_to_main = driver.find_element(By.ID, "Layer_1")
    go_to_main.click()

    time.sleep(2)
    current_url = driver.current_url
    print("Current URL after click:", current_url)
    assert current_url == "https://practicesoftwaretesting.com/"
    driver.quit()


def test_go_to_pliers(driver):
    driver.get("https://practicesoftwaretesting.com")

    wait = WebDriverWait(driver, 25)

    # Wait for the container to be present
    container = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "container")))

    # Wait for the first <a> with class 'card' inside the container
    first_product = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".container a.card"))
    )
    first_product.click()

    # Wait for the URL to include the product path
    wait.until(EC.url_contains("/product/01KA6SR9JG4P594K2BBFYFTG0E"))

    current_url = driver.current_url
    print("Current URL after click:", current_url)

    assert current_url.rstrip(
        '/') == ("https://practicesoftwaretesting.com/product"
                 "/01KA6SR9JG4P594K2BBFYFTG0E")

    driver.quit()
