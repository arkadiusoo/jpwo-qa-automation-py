from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@given("użytkownik otwiera stronę logowania")
def step_open_login_page(context):
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)
    context.wait = WebDriverWait(context.driver, 10)

    context.driver.get("https://practicesoftwaretesting.com/auth/login")


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


@then("powinien zobaczyć menu użytkownika")
def step_verify_logged_in(context):
    menu = context.wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-test='nav-menu']"))
    )
    assert menu.is_displayed()
    context.driver.quit()


@then("powinien zobaczyć komunikat o błędnych danych")
def step_verify_invalid_login(context):
    error = context.wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".alert.alert-danger")
        )
    )
    assert "Invalid email or password" in error.text
    context.driver.quit()