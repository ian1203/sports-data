from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from data_manager import clean_stat_value
from competition_error import CompetitionNotAvailableException


import time

class PlayerScraper:
    """
    A class to scrape player information from a sports website.

    Attributes:
        teams_data (dict): A dictionary to store scraped team and player data.
    """

    def __init__(self, driver, popup_handler):
        """
        Initializes the PlayerScraper with a WebDriver and popup handler.

        Parameters:
            driver (webdriver.Chrome): The WebDriver instance for browser automation.
            popup_handler (PopupHandler): An instance to handle popups during scraping.
        """

        self.driver = driver
        self.popup_handler = popup_handler
        self.teams_data = {}

    def select_competition(self):
        """
        Selects 'LaLiga' in the competition dropdown if not already selected.

        This function waits for the competition dropdown to become clickable,
        checks if 'LaLiga' is already selected, and if not, selects it. 
        Handles exceptions for timeouts and other errors.

        Raises:
            TimeoutException: If the dropdown or LaLiga option takes too long to load.
            Exception: For any other error that may occur during element selection.
        """
        
        try:
            dropdown_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='Box Flex ggRYVx qjBwj']//div[1]//button[1]"))
            )
            current_competition = dropdown_button.text

            if "LaLiga" in current_competition:
                return True  # LaLiga is already selected

            dropdown_button.click()
            la_liga_option = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//bdi[@class='Text jFxLbA'][normalize-space()='LaLiga']"))
            )
            la_liga_option.click()
            time.sleep(2)  # Pause to ensure page loads after selecting competition
            return True

        except TimeoutException:
            print("'LaLiga' option not available in the menu for this player. Skipping to te next player...")
            return False  # Return False if LaLiga is not found or clickable

        except Exception as e:
            print(f"Error selecting competition: {e}")
            return False
        
        

    def scrape_goalkeeper_data(self, player_link, team_name):
        """
        Scrapes data for a goalkeeper from the player's profile page.

        Parameters:
            player_link (str): URL link to the player's profile page.
        """

        try:
            self.driver.get(player_link)
            self.popup_handler.cerrar_popup()
        
            # Ensure 'LaLiga' competition is selected
            self.select_competition()

            player_name = self.driver.find_element(By.XPATH, "//h2[@class='Text cuNqBu']").text
            print(f"Scraping {player_name}")

            games = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[4]//div[1]//div[2]//div[1]").text
            amount_games = clean_stat_value(games, 2)
            
            minutes_played = self.driver.find_element(By.XPATH,
                                                 "//div[@class='Box kNZKNS']//div[4]//div[1]//div[2]//div[4]").text
            amount_minutes_played = clean_stat_value(minutes_played, 3)

            goals_conceded_per_game = self.driver.find_element(By.XPATH,
                                                          "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[1]").text
            amount_goals_conceded_per_game = clean_stat_value(goals_conceded_per_game, 4)

            try:
                penalties_saved = self.driver.find_element(By.XPATH,
                                                    "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[2]").text
                amount_penalties_saved_and_faced = clean_stat_value(penalties_saved, 2)
                if '/' in amount_penalties_saved_and_faced:
                    penalty_saved, penalties_faced = map(int, amount_penalties_saved_and_faced.split('/'))
                else:
                    # If it's a single number, assume it represents penalties faced with 0 penalties saved
                    penalties_faced = int(amount_penalties_saved_and_faced)
                    penalty_saved = 0
            except Exception as e:
                print(f"Error retrieving penalties saved data: {e}")
                penalties_faced = 0
                penalty_saved = 0

            saves_per_game = self.driver.find_element(By.XPATH,
                                                 "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[3]").text
            amount_saves_per_game = clean_stat_value(saves_per_game, 3)
            

            saves_per_game_percentage = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[3]").text
            amount_saves_per_game_percentage = clean_stat_value(saves_per_game_percentage, 4)
            

            goals_conceded = self.driver.find_element(By.XPATH,
                                                 "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[5]").text
            amount_goals_conceded = clean_stat_value(goals_conceded, 2)

            total_saves = self.driver.find_element(By.XPATH,
                                              "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[8]").text
            amount_total_saves = clean_stat_value(total_saves, 2)

            goals_prevented = self.driver.find_element(By.XPATH,
                                                  "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[9]").text
            amount_goals_prevented = clean_stat_value(goals_prevented, 2)

            passes_completed = self.driver.find_element(By.XPATH,
                                                   "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[6]").text
            amount_passes_completed = clean_stat_value(passes_completed, 3)

            passes_completed_percentage = self.driver.find_element(By.XPATH,
                                                              "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[6]").text
            amount_passes_completed_percentage = clean_stat_value(passes_completed_percentage, 4)

            clean_sheets = self.driver.find_element(By.XPATH,
                                               "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[1]").text
            amount_clean_sheets = clean_stat_value(clean_sheets, 2)

            error_leading_to_shot = self.driver.find_element(By.XPATH,
                                                        "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[8]").text
            amount_error_leading_to_shot = clean_stat_value(error_leading_to_shot, 4)

            error_leading_to_goal = self.driver.find_element(By.XPATH,
                                                        "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[9]").text
            amount_error_leading_to_goal = clean_stat_value(error_leading_to_goal, 4)

            if team_name not in self.teams_data:
                self.teams_data[team_name] = {}
            self.teams_data[team_name][player_name] = {
            'Games Played': amount_games,
            'Minutes Played': amount_minutes_played,
            'Goals Conceded Per Game': amount_goals_conceded_per_game,
            'Penalties Saved': penalty_saved,
            'Penalties Faced': penalties_faced,
            'Saves Per Game': amount_saves_per_game,
            'Saves Per Game Percentage': amount_saves_per_game_percentage,
            'Goals Conceded': amount_goals_conceded,
            'Total Saves': amount_total_saves,
            'Goals Prevented': amount_goals_prevented,
            'Passes Completed': amount_passes_completed,
            'Percentage of Passes Completed': amount_passes_completed_percentage,
            'Clean Sheets': amount_clean_sheets,
            'Errors leading to shot': amount_error_leading_to_shot,
            'Errors leading to goal': amount_error_leading_to_goal
            }
            
        except TimeoutException:
            print("Error: Element took too long to load.")
        except Exception as e:
            print(f"Error extracting {player_name}'s data: {e}")
        

    def scrape_field_player_data(self, player_link, team_name):
        """
        Scrapes data for a general player from the player's profile page.

        Parameters:
            player_link (str): URL link to the player's profile page.
        """

        try:
            self.driver.get(player_link)
            self.popup_handler.cerrar_popup()

            # Ensure 'LaLiga' competition is selected
            self.select_competition()

            player_name = self.driver.find_element(By.XPATH, "//h2[@class='Text cuNqBu']").text
            print(f"Scraping {player_name}")

            games = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[4]//div[1]//div[2]//div[1]").text
            amount_games = clean_stat_value(games, 2)

            minutes_played = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[4]//div[1]//div[2]//div[4]").text
            amount_minutes_played = clean_stat_value(minutes_played, 3)

            goals = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[1]").text
            amount_goals = clean_stat_value(goals, 1)

            amount_xg = 0
            amount_shots_per_game = 0
            amount_shots_target_per_game = 0
            amount_big_chances_missed = 0    

            try:
                xg_element = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[2]").text
                if "Expected Goals (xG)" in xg_element:
                    amount_xg = clean_stat_value(xg_element, 3)
                    

                    shots_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[5]").text
                    amount_shots_per_game = clean_stat_value(shots_per_game, 3)

                    shots_target_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[6]").text
                    amount_shots_target_per_game = clean_stat_value(shots_target_per_game, 5)

                    big_chances_missed  = self.driver.find_element(By.XPATH,
                                                    "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[7]").text
                    amount_big_chances_missed = clean_stat_value(big_chances_missed, 3)

            except Exception as e:
                print(f"Error retrieving {player_name}'s xG related data: {e}")
            
            
            assists = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[1]").text
            amount_assists = clean_stat_value(assists, 1)

            xa = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[2]").text
            amount_xa = clean_stat_value(xa, 3)

            big_chances_created = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[4]").text
            amount_big_chances_created = clean_stat_value(big_chances_created, 3)

            key_passes_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[5]").text
            amount_key_passes_per_game = clean_stat_value(key_passes_per_game, 2)

            passes_completed_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[6]").text
            amount_passes_completed_per_game = clean_stat_value(passes_completed_per_game, 3)

            passes_completed_per_game_percentage = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[6]").text
            amount_passes_completed_per_game_percentage = clean_stat_value(passes_completed_per_game_percentage, 4)

            succesful_dribles = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[1]").text
            amount_succesful_dribles = clean_stat_value(succesful_dribles, 2)

            total_duels_won_per_game = self.driver.find_element(By.XPATH,
                                                        "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[2]").text
            amount_total_duels_won_per_game = clean_stat_value(total_duels_won_per_game, 3)

            total_duels_won_percentage = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[2]").text
            amount_total_duels_won_percentage = clean_stat_value(total_duels_won_percentage, 4)

            ground_duels_won_per_game = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[3]").text
            amount_ground_duels_won_per_game = clean_stat_value(ground_duels_won_per_game, 3)

            ground_duels_won_per_game_percentage = self.driver.find_element(By.XPATH,
                                                                    "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[3]").text
            amount_ground_duels_won_per_game_percentage = clean_stat_value(ground_duels_won_per_game_percentage, 4)

            aerial_duels_won_per_game = self.driver.find_element(By.XPATH,
                                                                "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[4]").text
            amount_aerial_duels_won_per_game = clean_stat_value(aerial_duels_won_per_game, 3)

            aerial_duels_won_per_game_percentage = self.driver.find_element(By.XPATH,
                                                                        "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[4]").text
            amount_aerial_duels_won_per_game_percentage = clean_stat_value(aerial_duels_won_per_game_percentage, 4)

            possession_lost_per_game = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[5]").text
            amount_possession_lost_per_game = clean_stat_value(possession_lost_per_game, 2)

            fouls_received_per_game = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[7]").text
            amount_fouls_received_per_game = clean_stat_value(fouls_received_per_game, 2)

            offside_per_game = self.driver.find_element(By.XPATH,
                                                    "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[8]").text
            amount_offside_per_game = clean_stat_value(offside_per_game, 1)

            succesful_passes_opp_half = self.driver.find_element(By.XPATH,
                                                    "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[8]").text
            amount_succesful_passes_opp_half = clean_stat_value(succesful_passes_opp_half, 3)

            succesful_passes_opp_half_percentage = self.driver.find_element(By.XPATH,
                                                    "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[8]").text
            amount_succesful_passes_opp_half_percentage = clean_stat_value(succesful_passes_opp_half_percentage, 4)

            succesful_long_balls = self.driver.find_element(By.XPATH,
                                                    "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[9]").text
            amount_succesful_long_balls = clean_stat_value(succesful_long_balls, 3)

            succesful_long_balls_percentage = self.driver.find_element(By.XPATH,
                                                    "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[9]").text
            amount_succesful_long_balls_percentage = clean_stat_value(succesful_long_balls_percentage, 4)


            first_element = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[1]").text
            first_element_verification = clean_stat_value(first_element, 0)


            if 'Clean' in first_element_verification:
                interceptions_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[2]").text
                tackles_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[3]").text
                possession_won_opp_half_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[4]").text
                balls_recovered_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[5]").text
                dribbled_past_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[6]").text
                clearances_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[7]").text
            else:
                interceptions_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[1]").text
                tackles_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[2]").text
                possession_won_opp_half_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[3]").text
                balls_recovered_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[4]").text
                dribbled_past_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[5]").text
                clearances_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[6]").text

            amount_intercepctions_per_game = clean_stat_value(interceptions_per_game, 3)
            amount_tackles_per_game = clean_stat_value(tackles_per_game, 3)
            amount_possession_won_opp_half_per_game = clean_stat_value(possession_won_opp_half_per_game, 2)
            amount_balls_recovered_per_game = clean_stat_value(balls_recovered_per_game, 4)                
            amount_dribbled_past_per_game = clean_stat_value(dribbled_past_per_game, 4)
            amount_clearances_per_game = clean_stat_value(clearances_per_game, 3)


            fouls_per_game = self.driver.find_element(By.XPATH,
                                                    "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[6]").text
            amount_fouls_per_game = clean_stat_value(fouls_per_game, 1)



        
            if team_name not in self.teams_data:
                self.teams_data['Team'] = {}
            self.teams_data[team_name][player_name] = {
                'Games Played': amount_games,
                'Minutes Played': amount_minutes_played,
                'Goals': amount_goals,
                'Expected Goals (xG)': amount_xg,
                'Big Chances Missed': amount_big_chances_missed,
                'Shots Per Game': amount_shots_per_game,
                'Shots on Target Per Game': amount_shots_target_per_game,
                'Assists': amount_assists,
                'Expected Assists (xA)': amount_xa,
                'Big Chances Created': amount_big_chances_created,
                'Key Passes Per Game': amount_key_passes_per_game,
                'Passes Completed Per Game': amount_passes_completed_per_game,
                'Pass Completion Percentage': amount_passes_completed_per_game_percentage,
                'Succesful Passes Opp. Half': amount_succesful_passes_opp_half,
                'Succesful Passes Opp. Half Percentage':amount_succesful_passes_opp_half_percentage,
                'Succesful Long Balls':amount_succesful_long_balls,
                'Succesful Long Balls Percentage':amount_succesful_long_balls_percentage,
                'Successful Dribbles Per Game': amount_succesful_dribles,
                'Total Duels Won Per Game': amount_total_duels_won_per_game,
                'Total Duels Won Percentage': amount_total_duels_won_percentage,
                'Ground Duels Won Per Game': amount_ground_duels_won_per_game,
                'Ground Duels Won Percentage': amount_ground_duels_won_per_game_percentage,
                'Aerial Duels Won Per Game': amount_aerial_duels_won_per_game,
                'Aerial Duels Won Percentage': amount_aerial_duels_won_per_game_percentage,
                'Interceptions Per Game':amount_intercepctions_per_game,
                'Tackles Per Game':amount_tackles_per_game,
                'Possession Won Opp. Half':amount_possession_won_opp_half_per_game,
                'Balls Recovered Per Game':amount_balls_recovered_per_game,
                'Dribbled Past Per Game':amount_dribbled_past_per_game,
                'Clearances Per Game':amount_clearances_per_game,
                'Possession Lost Per Game': amount_possession_lost_per_game,
                'Fouls Committed Per Game':amount_fouls_per_game,
                'Fouls Received Per Game': amount_fouls_received_per_game,
                'Offsides Per Game': amount_offside_per_game
                }   

        except TimeoutException:
            print("Error: Element took too long to load.")
        except Exception as e:
            print(f"Error extracting {player_name}'s data: {e}")


    def scrape_players_data(self, team_name):
        """
        Scrapes player data from a table on the webpage.

        This method waits for the player data table to be present, retrieves each row 
        in the table, and extracts information about each player. The extracted data is 
        stored in a list, which can later be processed or saved.

        Raises:
            TimeoutException: If the table or its rows take too long to load.
            Exception: For any other error that may occur while scraping player data.
        """
        
        if team_name not in self.teams_data:
            self.teams_data[team_name] = {}  # Creates a new dictionary for this team

        try:
            table_xpath = "//table[contains(@class, 'fEUhaC')]"
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, table_xpath))
            )
            rows = self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fEUhaC')]//tr[@class='TableRow ygnhC']")
            players = []
            for row in rows:
                try:
                    player_link = row.find_element(By.XPATH, ".//td[1]//a").get_attribute("href")
                    position = row.find_element(By.XPATH, ".//td[2]").text
                    players.append({'link': player_link, 'position': position})
                except Exception as e:
                    print(f"Error extracting row data: {e}")

            for player in players:
                self.driver.get(player['link'])
                if not self.select_competition():
                    print("'LaLiga' not available for this player. Skipping to the next player.")
                    continue  # Skip this player if LaLiga is not available

                try:
                    season_element = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "Text.jFxLbA"))
                    )                    
                    current_season = season_element.text
                    if '24/25' != current_season:
                        print("Season '24/25' not available for this player. Skipping to the next player...")
                        continue  
                except TimeoutException:
                    print("No season selector was found. Skipping to the next player.")
                    continue

                # Proceed to scrape player data if LaLiga is selected
                try:
                    if player['position'].lower() == "goalkeeper":
                        self.scrape_goalkeeper_data(player['link'], team_name)
                    else:
                        self.scrape_field_player_data(player['link'], team_name)
                except Exception as e:
                    print(f"Error scraping player data: {e}")
        except Exception as e:
            print(f"Error: {e}")
