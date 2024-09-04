# Importing necessary libraries
import google.generativeai as gemini
import sys
import os
from dotenv import load_dotenv
from mpmath import mp, mpf
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

mp.pretty = True

# Creating static functions to be used in this application.

def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False

def list_to_words(a_list: list) -> str:
    if len(a_list) == 0:
        return ""
    elif len(a_list) == 1:
        return str(a_list[0])
    elif len(a_list) == 2:
        return str(a_list[0]) + " and " + str(a_list[1])
    else:
        return ", ".join(a_list[:-1]) + ", and " + a_list[-1]

def clear():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def scrape_capology(url, element_id):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
        element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
        
        if element:
            value = element.text.strip()
            return value
        else:
            return "Elemento no encontrado"

    except Exception as e:
        return f"Error: {e}"

def main() -> int:
    load_dotenv()
    gemini.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Ask user for configuration
    temperature = 0
    top_p = 0
    top_k = 1
    max_output_tokens = 8100

    float_temperature = float(temperature)
    float_top_p = float(top_p)
    float_top_k = int(top_k)
    int_max_output_tokens = int(max_output_tokens)

    generation_config = {
        "temperature": float_temperature,
        "top_p": float_top_p,
        "top_k": float_top_k,
        "max_output_tokens": int_max_output_tokens,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    ]

    model = gemini.GenerativeModel(
        model_name="gemini-1.5-flash-001",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    convo = model.start_chat(history=[])

    while True:
        clear()
        url = 'https://www.capology.com/club/belgrano/salaries/2024/'
        contents = 'futbol players salaries'
        elements = []
        selectors = []
        element_plurals = []
        num_elements = 1

        for i in range(int(num_elements)):
            element = input("Name the element you want to scrape: ")
            selector = input("What is the ID of the element " + str(element) + "? ")
            elements.append(element)
            selectors.append(selector)
            convo.send_message("What is the plural of \"" + str(element) + "\" (one word response only, no punctuation)?")
            element_plurals.append(str(convo.last.text))

        prompt = f"""
Write a web scraper using Python and Selenium (please include code only in your response)!

Sample Target: {url}
Rationale: Scrape the {list_to_words(element_plurals)} of all the {contents} on the target page.

IDs are as follows:
"""

        for i in range(len(elements)):
            prompt += f"""
{i + 1}. {elements[i]}: {selectors[i]}
"""

        prompt += f"""
Output: Save all the {list_to_words(element_plurals)} of all the {contents} in a CSV file.
Place the CSV file inside "csvs" directory. Include the {list_to_words(element_plurals)} as the headers of
the table in the CSV file.

Additional Instructions: Handle character encoding and only include the code in your response.
"""

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        code = '\n'.join(str(convo.last.text).split('\n')[1:-1])
        file_name = input("Please enter the name of the file you want the code to be in (no extension please): ")

        # Writing the code to a file
        code_file = open(os.path.join("scrapers", str(file_name) + ".py"), "w")
        code_file.write(code)
        code_file.close()

        # Executing the dynamically generated file.
        os.system("python3 " + str(os.path.join("scrapers", str(file_name) + ".py")))

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_scraping = input("Do you want to continue scraping a website? ")
        if continue_scraping != "Y":
            return 0

if __name__ == '__main__':
    # Configuración del navegador
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecuta el navegador en segundo plano
    service = Service('C:/chromedriver/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    main()
    driver.quit()
