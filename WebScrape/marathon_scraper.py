from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time
from config import config


def initial_driver_setup(website_url, button_css_selector) -> webdriver:
    """Initialize and set up WebDriver"""
    # Set up the WebDriver
    web_driver = webdriver.Chrome()
    # Navigate to the website
    web_driver.get(website_url)
    # Wait for the page to load
    WebDriverWait(web_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, button_css_selector))
    )
    return web_driver


def collect_data_from_page(webpage_table) -> []:
    """Fetch data from the current webpage"""
    site_array = []
    table_rows = webpage_table.find_elements(By.CSS_SELECTOR, ' tbody tr')
    # Extract the data from the page row by row
    for row in table_rows:
        temp_arr = []
        cell_elements = row.find_elements(By.TAG_NAME, 'td')
        for element in cell_elements:
            temp_arr.append(element.text)
        site_array.append(temp_arr)
    return np.array(site_array)


def scrape_website_data(website_url=config.DATA_URL, button_css_selector='a.paginate_button.next',
                        table_css_selector='table.hover.dataTable.no-footer') -> pd.DataFrame:
    """Collect all data from webpage"""
    # Create and setup webDriver
    driver = initial_driver_setup(website_url, button_css_selector)

    # Get the whole table from the webpage
    webpage_table = driver.find_element(By.CSS_SELECTOR, table_css_selector)

    # Create a table with columns names
    head_columns: [str] = []
    table_head = webpage_table.find_element(By.TAG_NAME, 'thead')
    table_row_heads = table_head.find_elements(By.XPATH, '//tr/th')
    for head in table_row_heads:
        head_columns.append(head.text)

    # Specify the final page number
    number_of_pages = driver.find_elements(By.CSS_SELECTOR, 'a.paginate_button')
    number_of_pages = int(number_of_pages[-2].text)

    # Create an array to store data from the webpage no. 1
    storage_array: np.ndarray = collect_data_from_page(webpage_table)
    while True:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.paginate_button.next')))
        next_button.click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table#tabModulos tbody tr'))
        )
        # Fetch data from webpage
        storage_array = np.vstack((storage_array, collect_data_from_page(webpage_table)))

        # Update active site variable to break loop at the end of the available data
        active_site = driver.find_element(By.CSS_SELECTOR, 'a.paginate_button.current')
        # Indicate the current page number
        # print('Active site:', active_site.text)

        # Finish fetching data after getting to the last page
        if int(active_site.text) == number_of_pages:
            print('Breaking on the last page')
            break

    # Convert list to NumPy ndarray and into DataFrame
    storage_array = np.array(storage_array)
    webpage_data = pd.DataFrame(data=storage_array, columns=head_columns)

    driver.quit()

    return webpage_data


def save_data_to_file(webpage_data):
    """Save stored data into .json and .csv files"""
    print(webpage_data)
    # webpage_data.to_json('valencia_marathon_2022.json')
    # webpage_data.to_csv('valencia_marathon_2022.csv', index=False)


if __name__ == '__main__':
    save_data_to_file(scrape_website_data())
