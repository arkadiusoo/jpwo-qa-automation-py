from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@given("administrator otwiera stronę logowania")
def step_open_login_page(context):
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)
    context.wait = WebDriverWait(context.driver, 10)
    context.driver.get("https://practicesoftwaretesting.com/auth/login")


@when("otworzy menu użytkownika")
def step_open_user_menu(context):
    menu_button = context.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-menu']"))
    )
    menu_button.click()


@when("przejdzie do dashboardu administratora")
def step_go_to_admin_dashboard(context):
    dashboard_link = context.wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-test='nav-admin-dashboard']"))
    )
    dashboard_link.click()


@then("wykres raportów powinien być widoczny")
def step_chart_visible(context):
    chart = context.wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "canvas.chart"))
    )
    assert chart.is_displayed(), "Wykres raportów nie jest widoczny!"
    context.driver.quit()