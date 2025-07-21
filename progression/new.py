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
CLASS = "9"
# Section for which Progression is being done.
SECTION = "A"
# New Section to promote student
NEW_SECTION = "A"

# Setup WebDriver
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def launch_browser():
    """
    open and Maximize Browser window
    """
    driver.get(URL)
    driver.maximize_window()

# Login
def login_user():

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

def select_academic_year():

    # Click on current Acedamic Year
    #ac_year = driver.find_element(By.XPATH, "//ul/li/div/div[2]/p")
    ac_year = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//ul/li/div/div[2]/p"))
    )
    ac_year.click()
    #time.sleep(5)
    close_school_info()

def close_school_info():

    # Close the School Information pop up.
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div/div/div/div[3]/button"))).click()
    time.sleep(1)

def init_student_progression():

    # Select Student Movement and Progression option
    driver.find_element(By.XPATH, "//ul/li[8]/div/div/h2/button").click()
    time.sleep(5)

    # Select  Progression Activity from the list
    driver.find_element(By.XPATH, "//ul/li[8]/div/div/div/div/ul/li[1]/span").click()
    time.sleep(5)

    # Go to Progression Module
    driver.find_element(By.XPATH, '//*[@id="page-content-wrapper"]/main/div/div/div/app-module-choice/div/div/div[1]/div/a').click()
    time.sleep(1)

    select_class_section()
    perform_progression()

def select_class_section():

    # Select Class for Progression
    Select(driver.find_element(By.XPATH, "//ul/li[1]/select")).select_by_value(CLASS)
    #time.sleep(0.1)

    # Select Section for Progression
    Select(driver.find_element(By.XPATH, "//ul/li[2]/select")).select_by_value(SECTIONS[SECTION])
    #time.sleep(0.1)

    # Go to Student List for Progression of selected class and section
    driver.find_element(By.XPATH, "//ul/li[3]/button").click()
    time.sleep(5)

def is_progression_done(student):

    progression_done = False

    student_status = student.find_element(By.XPATH, "./td[4]/span").get_attribute("innerHTML").strip()
    # Skip if Progression is done for the student.
    if student_status.lower() == "done":
        progression_done = True
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", student)

    return progression_done

def select_progression_status(student):

    # Progression Status
    Select(student.find_element(By.XPATH, ".//td[2]/ul/li[1]/select")).select_by_index(1)
    time.sleep(0.1)

def enter_student_percent(student):
    
    # Generate a random number between 55 and 85 for Marks in %
    percentage_marks = random.randint(55, 85)
    input_field = student.find_element(By.XPATH, ".//td[2]/ul/li[2]/input")
    input_field.clear()
    input_field.send_keys(str(percentage_marks))
    time.sleep(0.1)
    
    return percentage_marks

def enter_school_attended_days(student):

    # Generate a random number between 190 and 225 for No. of Days School attended
    days_school_attend = random.randint(190, 225)
    input_field = student.find_element(By.XPATH, ".//td[2]/ul/li[3]/input")
    input_field.clear()
    input_field.send_keys(str(days_school_attend))
    time.sleep(0.1)
    
    return days_school_attend

def select_schooling_status(student):

    # Schooling Status
    Select(student.find_element(By.XPATH, ".//td[2]/ul/li[4]/select")).select_by_index(1)
    time.sleep(0.1)

def select_new_section(student):
    
    # Section status
    Select(student.find_element(By.XPATH, "./td[3]/ul[2]/li[2]/select")).select_by_value(SECTIONS[NEW_SECTION])

def update_and_confirm_progression(student):

    # Click Update
    student.find_element(By.XPATH, ".//td[6]/button[1]").click()
    time.sleep(1)
                    
    # Click on confirm
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[6]/button[3]"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@role="dialog"]//button[@class="swal2-confirm swal2-styled"]'))).click()
    time.sleep(1)
                    
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[6]/button[1]"))).click()
    #time.sleep(1)

def perform_progression():

    # Initialize a counter and a flag to control the loop
    # Setup WebDriver (as you have already done)
    # [...]

    progression_done = 0
    row_count = 0
    restart_loop = True

    while restart_loop:
        restart_loop = False  # Reset the flag at the start of each iteration

        try:
            # Re-find all students dynamically in case of page change
            students = driver.find_elements(By.XPATH, "//tbody/tr")

            # Total number of students
            total_students = len(students)
            print(f"\n\t\tPerforming Progression for {total_students} Students of Class {CLASS}-{SECTION}")

            for student in students:
                try:
                    student_name = student.find_element(By.XPATH, "./td[1]/p[1]/span[2]").get_attribute("innerHTML").strip()
                    student_pen = student.find_element(By.XPATH, "./td[1]/p[2]/span[2]").get_attribute("innerHTML").strip()

                    # Skip if Progression is done for the student.
                    if is_progression_done(student):
                        print(f"\n\tProgression already done for {student_name}, {student_pen}")
                        continue

                    select_progression_status(student)
                    percentage_marks = enter_student_percent(student)
                    days_school_attend = enter_school_attended_days(student)
                    select_schooling_status(student)
                    select_new_section(student)
                    update_and_confirm_progression(student)

                    print(f"\n\t\tStudent Name: {student_name}, Student PEN No.: {student_pen}, Marks in Percentage (%): {percentage_marks}, No. of Days School attended: {days_school_attend}")
                    
                    # Increment the row counter
                    row_count += 1
                    progression_done += 1

                    # Pause for 10 seconds after every 100 students
                    if row_count > 0 and row_count % 100 == 0:
                        print(f"Processed {row_count} students. Pausing for 10 seconds...")
                        time.sleep(10)
                        restart_loop, students, is_error = go_to_next_page()
                        if is_error:
                            break
                except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException) as e:
                    print(f"Error processing row {row_count}: {e}")
                    restart_loop = True  # Set flag to restart loop in case of error
                    break  # Exit the for loop to re-find elements

        except Exception as e:
            print(f"Error: {e}")
            break  # Exit the while loop if a major error occurs
        finally:
            print(f"\n\t\tCompleted Progression for {progression_done} Students of Class {CLASS} - {SECTION}")

def go_to_next_page():
    
    restart_loop = True
    is_error = False

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
    except NoSuchElementException:
        print("No more pages. Script completed.")
        restart_loop = False
        is_error = True
    finally:
        # Recollect students from the next page, if no next page found then use current page
        students = driver.find_elements(By.XPATH, "//tbody/tr")

    time.sleep(1)
    return (restart_loop, students, is_error)

launch_browser()
login_user()
select_academic_year()
init_student_progression()

print("Script completed.")
