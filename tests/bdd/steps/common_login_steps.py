from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@when('wpisze email "{email}"')
def step_enter_email(context, email):
    email_input = context.wait.until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_input.send_keys(email)


@when('wpisze hasło "{password}"')
def step_enter_password(context, password):
    password_input = context.driver.find_element(By.ID, "password")
    password_input.send_keys(password)


@when("kliknie przycisk Log in")
def step_click_login(context):
    login_button = context.driver.find_element(
        By.CSS_SELECTOR, "input[data-test='login-submit']"
    )
    login_button.click()
