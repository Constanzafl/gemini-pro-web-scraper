```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://www.capology.com/club/belgrano/salaries/2024/"

# Element ID to find
element_id = "annual-avg"

try:
    # Navigate to the URL
    driver.get(url)

    # Find the element with the specified ID
    value = driver.find_element(By.ID, element_id).text

    # Print the extracted text
    print(value)

except NoSuchElementException:
    print("Element with ID '{}' not found on the page.".format(element_id))

# Close the browser
driver.quit()
```

**Explanation:**

1. **Imports:** Import necessary libraries:
   - `selenium` for browser automation
   - `Service` and `ChromeDriverManager` for managing ChromeDriver
   - `By` for locating elements
   - `NoSuchElementException` for handling element not found errors

2. **WebDriver Initialization:**
   - `service = Service(ChromeDriverManager().install())`: Download and initialize ChromeDriver.
   - `driver = webdriver.Chrome(service=service)`: Create a Chrome WebDriver instance.

3. **URL and Element ID:**
   - `url`: Define the target website URL.
   - `element_id`: Define the ID of the element you want to extract text from.

4. **Exception Handling:**
   - `try...except NoSuchElementException`: Use a try-except block to catch the `NoSuchElementException` in case the element is not found on the page.

5. **Scraping:**
   - `driver.get(url)`: Open the specified URL in the browser.
   - `driver.find_element(By.ID, element_id)`: Locate the element with the specified ID using `By.ID`.
   - `value = ... .text`: Extract the text content of the found element and store it in the `value` variable.

6. **Printing the Value:**
   - `print(value)`: Print the extracted text value.

7. **Closing the Browser:**
   - `driver.quit()`: Close the browser window after the scraping is complete.

**Output:**
The code will print the text content of the element with the ID "annual-avg" from the given URL. If the element is not found, it will print an error message indicating that.