import time
from ast import Bytes
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from behave import *
from selenium.webdriver.support.wait import WebDriverWait


@When("Wybiera pierwsze zamówienie")
def step_get_first_order(context):
    time.sleep(5)
    table = context.driver.find_element(By.TAG_NAME,
                                        "table")
    body = table.find_elements(By.TAG_NAME, "tbody")
    rows = body[0].find_elements(By.TAG_NAME, "tr")
    link = rows[0].find_element(By.TAG_NAME, "a")
    link.click()


@then("Numer powinien być widoczny")
def step_verify_number(context):
    number = context.wait.until(
        EC.visibility_of_element_located(
            (By.ID, "invoice_number")
        )
    )
    assert number.is_displayed()
    context.driver.quit()
