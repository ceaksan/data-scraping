from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from urllib.parse import urlsplit
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")

# set the URL components
url = 'https://t24.com.tr/yazarlar/hasan-gogus'
hostname, path, columnist = urlsplit(url).netloc, urlsplit(url).path.lstrip('/'), urlsplit(url).path.rsplit('/', 1)[-1]

# create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# navigate to the page
driver.get(f'https://{hostname}/{path}')

# find all the content containers
content_containers = driver.find_elements(By.CSS_SELECTOR, 'div._2Mepd')

while True:
    try:
        # check if there is a MoreButton element
        if not driver.find_elements(By.ID, 'MoreButton'):
            break

        # scroll down to the bottom of the page
        driver.execute_script("document.documentElement.scrollTop += 500;")

        # wait for the new content to load
        time.sleep(2)

        # click the MoreButton element to load more content
        more_button = driver.find_element(By.ID, 'MoreButton')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'MoreButton')))
        driver.execute_script("arguments[0].click();", more_button)

        # wait for the new content to load
        time.sleep(2)

        # find all the content containers
        content_containers = driver.find_elements(By.CSS_SELECTOR, 'div._2Mepd')

    except:
        # if there is no MoreButton element, break out of the loop
        break

# loop through the content containers and extract the data
results = []
for container in content_containers:
    # create a BeautifulSoup object from the HTML content of the container
    soup = BeautifulSoup(container.get_attribute('innerHTML'), 'html.parser')

    # find all the content elements
    elements = soup.select('div._1fE_V')

    # loop through the content elements and extract the data
    for element in elements:
        h3 = element.select_one('div._31Tbh > h3')
        h3_text = h3.text if h3 else ''
        a = element.select_one('div._31Tbh a')
        href = a['href'] if a else ''
        p = element.select_one('div._31Tbh p')
        p_text = p.text if p else ''
        second_p = element.select_one('._2J9OF p:nth-of-type(2)')
        second_p_text = second_p.text if second_p else ''
        result = {
            'title': h3_text,
            'path': f'https://{hostname}' + href,
            'description': p_text,
            'date': second_p_text
        }
        results.append(result)

# write the results to a JSON file
with open(f'{columnist}.json', 'w', encoding='utf-8') as f:
    # write the results to the file in JSON format
    json.dump(results, f, ensure_ascii=False)
    
# close the browser
driver.quit()
