import time
from time import thread_time

from behave import Then, When, Given
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@Given("Wybiera stronę główną")
def step_main_page(context):
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)
    context.wait = WebDriverWait(context.driver, 10)
    context.driver.get("https://practicesoftwaretesting.com")


@When("Wybiera tylko młotki")
def step_choose_hammers(context):
    time.sleep(1)
    checkboxes = context.driver.find_elements(By.CLASS_NAME, "icheck")
    hammer = checkboxes[1]
    hammer.click()


@Then("Powinien widzieć 7 młotków")
def step_verify_hammers(context):
    time.sleep(1)
    items = context.driver.find_elements(By.CLASS_NAME, "card")
    assert len(items) == 7
    context.driver.quit()
