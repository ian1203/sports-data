from browser_manager import BrowserManager
from popup_handler import PopupHandler
from sofascore_scraper import SofaScoreScraper
from player_scraper import PlayerScraper
from data_manager import create_dataframe

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

    for i, team in enumerate(teams):
        print(f"Scraping players from: {team['name']}")
        team_name = team['name']
        driver.get(team['url'])
        popup_handler.cerrar_popup()
        
        try:
            sofascore_scraper.switch_to_list_view(team['url'])
        except Exception as e:
            print(f"Error switching to list view: {e}")
            popup_handler.cerrar_popup()
            
        player_scraper.scrape_players_data(team_name)

        # Convert partial data to DataFrame and display every iteration for debugging
        partial_df = create_dataframe(player_scraper.teams_data)
        print(f"Data after scraping {team_name}:")
        print(partial_df.head())  # Adjust head() to view more or fewer rows as neededt
        # Optional: display after a set number of teams for larger data collections
        if (i + 1) % 2 == 0:
            print(f"Data after scraping {i + 1} teams:")
            print(partial_df)
            partial_df.to_csv("partial_player_data.csv", index=True)
    
    # Convert collected data into a DataFrame
    players_df = create_dataframe(player_scraper.teams_data)
    print(players_df)  # Display the DataFrame or save it as needed
    players_df.to_csv("players_data.csv", index=True)  # Index=True to keep the team and player names as index columns

    browser_manager.quit()

if __name__ == "__main__":
    main()
