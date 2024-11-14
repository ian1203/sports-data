from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SofaScoreScraper:
    """
    A class to scrape team and player information from SofaScore.

    Attributes:
        driver (webdriver.Chrome): The WebDriver instance to interact with the website.
        popup_handler (PopupHandler): Instance to manage popups during scraping.
        league_url (str): The URL of the LaLiga league page on SofaScore.
    """
    def __init__(self, driver, popup_handler):
        """
        Initializes the SofaScoreScraper with a WebDriver, popup handler, and league URL.

        Parameters:
            driver (webdriver.Chrome): The WebDriver instance for browser automation.
            popup_handler (PopupHandler): An instance to handle popups during scraping.
        """
        self.driver = driver
        self.popup_handler = popup_handler
        self.league_url = "https://www.sofascore.com/en-us/tournament/soccer/spain/laliga/8#id:61643"
    
    def get_teams(self):
        """
        Retrieves a list of teams in the LaLiga league.

        Navigates to the LaLiga league page, closes any popups, and collects team names and URLs.

        Returns:
            list[dict]: A list of dictionaries containing team names and URLs.

        Raises:
            TimeoutException: If the teams element takes too long to load.
        """

        self.driver.get(self.league_url)
        self.popup_handler.cerrar_popup()
        teams = []
        try:
            standings_element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/div[2]')
                )
            )
            rows = standings_element.find_elements(By.XPATH, ".//a[@data-testid='standings_row']")
            for row in rows:
                team_name = row.find_element(By.CLASS_NAME, "Box.ljKzDM").text
                team_url = row.get_attribute('href')
                teams.append({'name': team_name, 'url': team_url})
        except TimeoutException:
            print("Error: el elemento no estuvo disponible a tiempo")
        return teams
    
    def switch_to_list_view(self, team_url):
        """
        Switches the page view to list view for a specific team.

        Parameters:
            team_url (str): The URL of the team's page.

        Raises:
            TimeoutException: If the list view button takes too long to load or click.
        """
        
        self.driver.get(team_url)
        try:
            list_view_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[5]/div[1]/div[2]/label[2]/div')
                )
            )
            list_view_button.click()
        except Exception as e:
            print(f"Error al cambiar a 'List View': {e}")
