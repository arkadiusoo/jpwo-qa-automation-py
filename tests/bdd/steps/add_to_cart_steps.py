import time

from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@When("Wybiera pierwszy produkt")
def choose_first_item(context):
    time.sleep(2)
    items = context.driver.find_elements(By.CLASS_NAME, "card")
    items[0].click()


@When("Nie powinien widzieć koszyka")
def step_verify_no_cart(context):
    time.sleep(2)
    cart_button = context.driver.find_element(By.CLASS_NAME, "nav-link")
    assert not cart_button.is_displayed()


@When("Dodaje produkt do koszyka")
def add_to_cart(context):
    time.sleep(2)
    button = context.driver.find_element(By.ID, "btn-add-to-cart")
    button.click()


@Then("Powinien widzieć koszyk")
def step_verify_cart(context):
    time.sleep(2)
    cart_button = context.driver.find_element(By.CLASS_NAME, "nav-link")
    assert cart_button.is_displayed()
    context.driver.quit()
