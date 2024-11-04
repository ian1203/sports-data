from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

class BrowserManager:
    """
    A class to manage a Chrome WebDriver instance for browser automation using Selenium.

    Attributes:
        driver (webdriver.Chrome): The active WebDriver instance.
    """

    def __init__(self):
        """
        Initializes the BrowserManager class.

        This sets up the WebDriver with Chrome options and a local ChromeDriver,
        configured to start maximized, disable extensions, and use eager page load strategy.
        Also, sets timeouts for page load and implicit waits.

        Raises:
            WebDriverException: If the ChromeDriver fails to initialize.
        """
        # Set WDM_LOCAL to use the cached ChromeDriver without checking for updates
        os.environ["WDM_LOCAL"] = "1"


        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.page_load_strategy = 'eager'

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Set timeouts to manage long load times
        self. driver.set_page_load_timeout(30)  # Page load timeout
        self.driver.implicitly_wait(10)  # Element load wait
    
    def get_driver(self):
        """
        Returns the active WebDriver instance.

        Returns:
            webdriver.Chrome: The WebDriver instance initialized in the constructor.
        """

        return self.driver
    
    def quit(self):
        """
        Closes the WebDriver instance and quits the browser session.

        This should be called to free up resources after completing browser interactions.
        """
        self.driver.quit()

