from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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
        and clicks it. It waits until the popup becomes invisible to ensure it was
        successfully closed.

        Exceptions Handled:
            NoSuchElementException: If the popup or close button is not found.
            TimeoutException: If the popup does not disappear within the specified timeout.
        """
        try:
            close_button = self.driver.find_element(By.XPATH, '//*[@id="portals"]/div/div/div/div/div/div[1]/div/div[5]/button[1]')
            self.driver.execute_script("arguments[0].scrollIntoView();", close_button)
            close_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, '//*[@id="portals"]/div/div/div/div/div/div[1]/div/div[5]/button[1]'))
            )
        except (NoSuchElementException, TimeoutException):
            pass
