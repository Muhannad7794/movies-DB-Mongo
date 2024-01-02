from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import pytest

# Import the exception
from selenium.webdriver.chrome.options import Options
import os


@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


def test_studios_search(driver):
    driver.get("http://localhost:3307/studios/")
    search_bar = driver.find_element(By.CLASS_NAME, "search-bar")
    search_bar.clear()
    search_bar.send_keys("warner")
    search_button = driver.find_element(By.CLASS_NAME, "search-button")
    search_button.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".studio-item"))
    )

    retries = 3
    for _ in range(retries):
        try:
            studio_cards = driver.find_elements(By.CSS_SELECTOR, ".studio-item h3")
            studio_names = [card.text for card in studio_cards]
            print("Studio Names:", studio_names)
            assert any("warner" in name.lower() for name in studio_names)
            break
        except StaleElementReferenceException:
            if _ == retries - 1:
                raise

    studio_cards[0].click()

    studio_details = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "studio-details-text"))
    )

    # Assert the studio details are displayed
    assert "Warner Bros." in studio_details.text
    assert "1923" in studio_details.text
    assert "Burbank, California, USA" in studio_details.text
