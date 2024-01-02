import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture(scope="function")
def driver():
    # Setup the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # Implicit wait for 10 seconds
    yield driver
    # Teardown
    driver.quit()


def test_studios_ordering_by_name(driver):
    # Navigate to the Movies window
    driver.get("http://localhost:3307/studios/")

    # Function to select an order from the dropdown
    def get_studios_names(order_value):
        try:
            order_select = driver.find_element(By.ID, "order")
            order_select.click()
            driver.find_element(
                By.CSS_SELECTOR, f"option[value='{order_value}']"
            ).click()

            # Wait for the page to update with sorted studios
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "studio-item"))
            )

            # Fetch titles of the studios listed
            studio_items = driver.find_elements(By.CLASS_NAME, "studio-item")
            return [
                studio.find_element(By.TAG_NAME, "h3").text for studio in studio_items
            ]
        except NoSuchElementException:
            pytest.fail(f"Failed to find element, check if the UI has changed")

    # Verify ordering by name
    names_sorted_by_name = get_studios_names("name")
    assert names_sorted_by_name == sorted(
        names_sorted_by_name
    ), "studios are not sorted by name correctly"
