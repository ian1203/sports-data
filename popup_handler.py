from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

class PopupHandler:
    """
    A class to handle popups that may appear during web scraping.

    Attributes:
        driver (webdriver.Chrome): The WebDriver instance to interact with the browser.
    """

    def __init__(self, driver):

        """
        Initializes the PopupHandler with a WebDriver.

        Parameters:
            driver (webdriver.Chrome): The WebDriver instance to manage browser interactions.
        """
        self.driver = driver

    def cerrar_popup(self):
        """
        Closes a popup if it is present on the page.

        This method attempts to locate the popup close button, scrolls it into view,
        and clicks it if it appears. If the popup is not present, it will continue
        without an error. It waits until the popup becomes invisible to ensure it was
        successfully closed if it was present.

        Exceptions Handled:
            NoSuchElementException: If the popup or close button is not found.
            TimeoutException: If the popup does not disappear within the specified timeout.
            ElementNotInteractableException: If the element is not interactable.
        """
        try:
            # Wait for the close button to be clickable; if it doesn't appear, skip
            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="portals"]/div/div/div/div/div/div[1]/div/div[5]/button[1]'))
            )
            
            # Scroll into view and try clicking
            self.driver.execute_script("arguments[0].scrollIntoView();", close_button)
            
            try:
                close_button.click()
            except ElementNotInteractableException:
                self.driver.execute_script("arguments[0].click();", close_button)
            
            # Wait until the popup disappears
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, '//*[@id="portals"]/div/div/div/div/div/div[1]/div/div[5]/button[1]'))
            )
        except (TimeoutException, NoSuchElementException):
            # If popup doesn't appear, proceed without clicking
            pass

