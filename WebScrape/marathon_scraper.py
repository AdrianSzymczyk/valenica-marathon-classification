from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time


# Method to fetch data from the current webpage
def collect_data_from_page(table) -> []:
    site_array = []
    table_rows = table.find_elements(By.CSS_SELECTOR, ' tbody tr')
    # Extract the data from the page row by row
    for row in table_rows:
        temp_arr = []
        cell_elements = row.find_elements(By.TAG_NAME, 'td')
        for element in cell_elements:
            temp_arr.append(element.text)
        site_array.append(temp_arr)
    return np.array(site_array)


# Data URL
marathon_2022 = 'https://resultados.valenciaciudaddelrunning.com/en/maraton-clasificados.php?y=2022'

# Set up the WebDriver
driver = webdriver.Chrome()
# Navigate to the website
driver.get(marathon_2022)
# Wait for the page to load
WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.paginate_button.next'))
)

# Get the whole table from the webpage
table = driver.find_element(By.CSS_SELECTOR, 'table.hover.dataTable.no-footer')

# Create a table with columns names
columns: [str] = []
table_head = table.find_element(By.TAG_NAME, 'thead')
table_row_heads = table_head.find_elements(By.XPATH, '//tr/th')
for head in table_row_heads:
    columns.append(head.text)

# Define final page number
number_of_pages = driver.find_elements(By.CSS_SELECTOR, 'a.paginate_button')
number_of_pages = int(number_of_pages[-2].text)

# Create an array to store data from the webpage
storage_array: np.ndarray = collect_data_from_page(table)
while True:
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.paginate_button.next')))
    next_button.click()
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table#tabModulos tbody tr'))
    )
    # Fetch data from webpage
    storage_array = np.vstack((storage_array, collect_data_from_page(table)))

    # Update active site variable to break loop at the end of the available data
    active_site = driver.find_element(By.CSS_SELECTOR, 'a.paginate_button.current')
    print('Active site:', active_site.text)

    # Finish fetching data after getting to the last page
    if int(active_site.text) == number_of_pages:
        print('Breaking on the last page')
        break

# Convert list to NumPy ndarray
storage_array = np.array(storage_array)
webpage_data = pd.DataFrame(data=storage_array, columns=columns)
# print(webpage_data)
webpage_data.to_json('valencia_marathon_2022.json')
webpage_data.to_csv('valencia_marathon_2022.csv', index=False)

driver.quit()
