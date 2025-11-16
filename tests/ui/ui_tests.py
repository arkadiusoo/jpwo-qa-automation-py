import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pytest


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def test_go_to_main(driver):
    driver.get("https://practicesoftwaretesting.com/product"
               "/01KA6SR9JG4P594K2BBFYFTG0E")
    wait = WebDriverWait(driver, 15)
    go_to_main = driver.find_element(By.ID, "Layer_1")
    go_to_main.click()

    time.sleep(2)
    current_url = driver.current_url
    print("Current URL after click:", current_url)
    assert current_url == "https://practicesoftwaretesting.com/"
    # Close the browser
    driver.quit()
