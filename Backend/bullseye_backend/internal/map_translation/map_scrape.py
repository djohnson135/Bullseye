from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BUTTON_XPATH = "//button[text()='store map']"
STORE_MAP_ID = "content"


def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(chrome_options=chrome_options)


def navigate_to_store_map(driver: webdriver.Chrome):
    WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, BUTTON_XPATH))
    )

    driver.find_element(By.XPATH, BUTTON_XPATH).click()

    WebDriverWait(driver, 50).until(
        EC.presence_of_all_elements_located((By.ID, STORE_MAP_ID))
    )


def get_store_map_web_element(driver):
    return driver.find_element(By.ID, STORE_MAP_ID)


def scrape_map(url):
    driver = setup_chrome_driver()
    driver.get(url)
    navigate_to_store_map(driver)
    map_content = get_store_map_web_element(driver)

    return map_content.get_attribute("innerHTML")
