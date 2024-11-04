from browser_manager import BrowserManager
from popup_handler import PopupHandler
from sofascore_scrapper import SofaScoreScraper
from player_scrapper import PlayerScraper

def main():
    """
    Main function to execute the web scraping process.

    This function initializes necessary browser and scraper components, navigates to team URLs, 
    and scrapes player data. It also manages popup handling and error handling for different
    page views. Upon completion, it closes the browser session.

    Workflow:
        - Initializes browser, popup handler, and scraper instances.
        - Retrieves teams and iterates over them to scrape player information.
        - Switches to list view for each team page if available.
        - Handles any popups encountered during the scraping process.
        - Closes the browser instance after scraping.

    Raises:
        Exception: If errors occur during page view switching or data scraping.
    """
    browser_manager = BrowserManager()
    driver = browser_manager.get_driver()
    
    popup_handler = PopupHandler(driver)
    sofascore_scraper = SofaScoreScraper(driver, popup_handler)
    player_scraper = PlayerScraper(driver, popup_handler)
    
    teams = sofascore_scraper.get_teams()
    for team in teams:
        print(f"Scraping players from: {team['name']}")
        driver.get(team['url'])
        popup_handler.cerrar_popup()
        
        try:
            sofascore_scraper.switch_to_list_view(team['url'])
        except Exception as e:
            print(f"Error switching to list view: {e}")
            popup_handler.cerrar_popup()
            
        player_scraper.scrape_players_data()

    browser_manager.quit()

if __name__ == "__main__":
    main()
