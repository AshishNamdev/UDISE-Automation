from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random


def generate_random_integer(start, end):
    return str(random.randint(start, end))

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://sdms.udiseplus.gov.in/p0/v1/login?state-id=110")
driver.maximize_window()

input_element = driver.find_element(By.CLASS_NAME, "form-control")
input_element.send_keys("BR71392670")

input_element = driver.find_element(By.ID, "password-field")
input_element.send_keys("ODdgp53#")
time.sleep(15)

login_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.ID, "submit-btn"))
)
login_button.click()
time.sleep(2)

time.sleep(25)

student_count = 1
while True:
    try:
        print(f"Processing student #{student_count}")
        time.sleep(2)

        first_digit = str(random.choice([6, 7, 8, 9]))
        remaining_digits = ''.join(str(random.randint(0, 9)) for _ in range(9))
        random_10_digit = first_digit + remaining_digits

        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='primaryMobile']"))
        )
        input_box.clear()
        time.sleep(2)
        input_box.send_keys(random_10_digit)
        time.sleep(2)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        blood_group_select = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//select[@formcontrolname="bloodGroup"]'))
        ))
        blood_group_select.select_by_value("9")
        time.sleep(2)

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(span/text())='Save']"))
        ).click()
        time.sleep(2)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.swal2-actions > button.swal2-confirm"))
        ).click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and @matsteppernext]'))
        ).click()
        time.sleep(2)

        dropdown_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@formcontrolname='languageGroup']"))
        )
        select = Select(dropdown_element)
        option_values = [option.get_attribute("value") for option in select.options]

        if "1002" in option_values:
            select.select_by_value("1002")
        else:
            select.select_by_value("1005")
        time.sleep(2)

        date_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@formcontrolname="admnStartDate"]'))
        )
        driver.execute_script("arguments[0].click();", date_input)
        date_input.send_keys("04/04/2023", Keys.ENTER)
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "swal2-cancel"))
        ).click()
        time.sleep(2)

        olympiad_radio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="radio" and @value="2" and @formcontrolname="olympdsNlc"]'))
        )
        olympiad_radio.click()
        time.sleep(2)

        distance_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//select[@formcontrolname="distanceFrmSchool"]'))
        )
        Select(distance_dropdown).select_by_value("2")
        time.sleep(2)

        parent_education_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//select[@formcontrolname="parentEducation"]'))
        )
        Select(parent_education_dropdown).select_by_value("5")
        time.sleep(2)

        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="cdk-step-content-0-2"]//form//div[2]/div/button[2]'))
        )
        save_button.click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@type="button" and contains(@class, "swal2-cancel swal2-styled")]'))
        ).click()
        time.sleep(2)

        # body = driver.find_element(By.TAG_NAME, "body")
        # body.send_keys(Keys.END)
        # time.sleep(2)

        # Wait for the button to be present
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "btnsave") and contains(@class, "float-end")]'))
        )

        # Scroll to the button 7 times
        for _ in range(7):
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", button)
            time.sleep(0.3)  # small delay to allow the scroll to complete

        # Click when clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "btnsave") and contains(@class, "float-end")]'))
        ).click()

        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@type="button" and contains(@class, "swal2-cancel")]'))
        ).click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@type="button" and contains(text(), "Next Student")]'))
        ).click()
        time.sleep(2)

        student_count += 1

    except Exception as e:
        print(f"Failed at student #{student_count}: {e}")
        break
