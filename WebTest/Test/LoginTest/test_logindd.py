from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start a new instance of Chrome WebDriver
driver = webdriver.Chrome()

# Navigate to the provided URL
url = "https://practicetestautomation.com/practice-test-login/"
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Find the username input field and enter the username
username_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='username']")))
username_input.send_keys("your_username_here")

# Find the password input field and enter the password
password_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='password']")))
password_input.send_keys("your_password_here")

# Find and click the submit button
submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='submit']")))
submit_button.click()

# Wait for a few seconds to see the result before closing the browser
driver.implicitly_wait(3)

# Close the browser
driver.quit()
