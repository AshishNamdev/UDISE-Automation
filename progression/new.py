from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random


URL = "https://sdms.udiseplus.gov.in/p0/v1/login"
USER_NAME = "10140601611"
PASSWORD = "xde75RN#"

# Section name maaping to value.
SECTIONS = {"A":"1", "B":"2", "C":"3", "D":"4", "E":"5", "F":"6"}

# Class for which Progression is being done.
CLASS = "7"
# Section for which Progression is being done.
SECTION = "B"

# Setup WebDriver
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(URL)
driver.maximize_window()

# Login
input_element = driver.find_element(By.CLASS_NAME, "form-control")
input_element.send_keys(USER_NAME)

input_element = driver.find_element(By.ID, "password-field")
input_element.send_keys(PASSWORD)

time.sleep(10)

login_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.ID, "submit-btn"))
)
login_button.click()

time.sleep(15)

# Click on current Acedamic Year
#ac_year = driver.find_element(By.XPATH, "//ul/li/div/div[2]/p")
ac_year = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//ul/li/div/div[2]/p"))
)
ac_year.click()
time.sleep(5)

# Close the School Information pop up.
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div/div/div/div[3]/button"))).click()
time.sleep(5)

# Select Student Movement and Progression option
driver.find_element(By.XPATH, "//ul/li[8]/div/div/h2/button").click()
time.sleep(5)

# Select  Progression Activity from the list
driver.find_element(By.XPATH, "//ul/li[8]/div/div/div/div/ul/li[1]/span").click()
time.sleep(10)

# Go to Progression Module
driver.find_element(By.XPATH, '//*[@id="page-content-wrapper"]/main/div/div/div/app-module-choice/div/div/div[1]/div/a').click()
time.sleep(5)

# Select Class for Progression
Select(driver.find_element(By.XPATH, "//ul/li[1]/select")).select_by_value(CLASS)
time.sleep(1)

# Select Section for Progression
Select(driver.find_element(By.XPATH, "//ul/li[2]/select")).select_by_value(SECTIONS[SECTION])
time.sleep(1)

# Go to Student List for Progression of selected class and section
driver.find_element(By.XPATH, "//ul/li[3]/button").click()
time.sleep(5)


# Initialize a counter and a flag to control the loop
# Setup WebDriver (as you have already done)
# [...]

row_count = 0
restart_loop = True

while restart_loop:
    restart_loop = False  # Reset the flag at the start of each iteration

    try:
        # Re-find all rows dynamically in case of page change
        rows = driver.find_elements(By.XPATH, "//tbody/tr")
        
        # Total number of rows
        total_rows = len(rows)
        print(f"\n\t\tPerforming Progression for {total_rows} Students of Class {CLASS} - {SECTION}")

        for row in rows:
            try:
                student_name = row.find_element(By.XPATH, "./td[1]/p[1]/span[2]").get_attribute("innerHTML").strip()
                student_pen = row.find_element(By.XPATH, "./td[1]/p[2]/span[2]").get_attribute("innerHTML").strip()

                # Progression Status
                Select(row.find_element(By.XPATH, ".//td[2]/ul/li[1]/select")).select_by_index(1)

                time.sleep(0.1)
                # Generate a random number between 55 and 85 for Marks in %
                percentage_marks = random.randint(55, 85)
                input_field = row.find_element(By.XPATH, ".//td[2]/ul/li[2]/input")
                input_field.clear()
                input_field.send_keys(str(percentage_marks))

                time.sleep(0.1)
                # Generate a random number between 190 and 225 for No. of Days School attended
                days_school_attend = random.randint(200, 230)
                input_field = row.find_element(By.XPATH, ".//td[2]/ul/li[3]/input")
                input_field.clear()
                input_field.send_keys(str(days_school_attend))
                time.sleep(0.1)

                time.sleep(0.1)
                # Schooling Status
                Select(row.find_element(By.XPATH, ".//td[2]/ul/li[4]/select")).select_by_index(1)
                
                time.sleep(0.1)
                # Section status
                Select(row.find_element(By.XPATH, "./td[3]/ul[2]/li[2]/select")).select_by_value(SECTIONS[SECTION])

                # Click Update
                row.find_element(By.XPATH, ".//td[6]/button[1]").click()
                time.sleep(1)
                
                # Click on confirm
                #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[6]/button[3]"))).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@role="dialog"]//button[@class="swal2-confirm swal2-styled"]'))).click()
                time.sleep(1)
                
                #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[6]/button[1]"))).click()
                #time.sleep(1)

                print(f"\n\t\tStudent Name: {student_name}, Student PEN No.: {student_pen}, Marks in Percentage (%): {percentage_marks}, No. of Days School attended: {days_school_attend}")
                # Increment the row counter
                row_count += 1

                # Pause for 10 seconds after every 100 rows
                if row_count > 0 and row_count % 100 == 0:
                    print(f"Processed {row_count} rows. Pausing for 10 seconds...")
                    time.sleep(10)

                    # Scroll to the top of the page
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
                    time.sleep(1)

                    # Find and click the "Next Page" button
                    try:
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-admin-dashboard/div[2]/div[2]/main/div/div/div/app-promotion/div[3]/div/table/tbody/tr[1]/following::button[2]"))
                        )
                        next_button.click()

                        # Wait for the next page to load
                        time.sleep(5)

                        # Recollect rows from the next page
                        rows = driver.find_elements(By.XPATH, "//tbody/tr")

                    except NoSuchElementException:
                        print("No more pages. Script completed.")
                        restart_loop = False
                        break

                    time.sleep(1)

            except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Error processing row {row_count}: {e}")
                restart_loop = True  # Set flag to restart loop in case of error
                break  # Exit the for loop to re-find elements

    except Exception as e:
        print(f"Error: {e}")
        break  # Exit the while loop if a major error occurs

print("Script completed.")
