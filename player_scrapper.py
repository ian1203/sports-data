from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from data_manager import clean_stat_value

import time

class PlayerScraper:
    """
    A class to scrape player information from a sports website.

    Attributes:
        driver (webdriver.Chrome): The WebDriver instance to interact with the website.
        popup_handler (PopupHandler): The popup handler instance to close unwanted popups.
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

            current_competition = self.driver.find_element(
                By.XPATH, "//div[@class='Box Flex ggRYVx qjBwj']//div[1]//button[1]"
            ).text

            if "LaLiga" not in current_competition:
                dropdown_button.click()
                la_liga_option = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//bdi[@class='Text jFxLbA'][normalize-space()='LaLiga']"))
                )
                la_liga_option.click()
                time.sleep(5)  # Allow time for the page to update after changing competition
        except TimeoutException:
            print("Error: Competition selection dropdown took too long to load.")
        except Exception as e:
            print(f"Error selecting competition: {e}")

    def scrape_goalkeeper_data(self, player_link):
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
            print(games)
            print("Amount of games played:", amount_games)

            minutes_played = self.driver.find_element(By.XPATH,
                                                 "//div[@class='Box kNZKNS']//div[4]//div[1]//div[2]//div[4]").text
            amount_minutes_played = clean_stat_value(minutes_played, 3)
            print("Amount of minutes played:", amount_minutes_played)

            goals_conceded_per_game = self.driver.find_element(By.XPATH,
                                                          "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[1]").text
            print(goals_conceded_per_game)
            amount_goals_conceded_per_game = clean_stat_value(goals_conceded_per_game, 4)
            print("Amount of goals conceded per game:", amount_goals_conceded_per_game)

            penalties_saved = self.driver.find_element(By.XPATH,
                                                  "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[2]").text
            amount_penalties_saved = clean_stat_value(penalties_saved, 2)
            print("Amount of penalties saved:", amount_penalties_saved)

            saves_per_game = self.driver.find_element(By.XPATH,
                                                 "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[3]").text
            amount_saves_per_game = clean_stat_value(saves_per_game, 3)
            print("Amount of saves per game:", amount_saves_per_game)

            saves_per_game_percentage = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[3]").text
            amount_saves_per_game_percentage = clean_stat_value(saves_per_game_percentage, 4)
            print("Percentage of saves per game:", amount_saves_per_game_percentage)

            goals_conceded = self.driver.find_element(By.XPATH,
                                                 "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[5]").text
            amount_goals_conceded = clean_stat_value(goals_conceded, 2)
            print("Amount of total goals conceded:", amount_goals_conceded)

            total_saves = self.driver.find_element(By.XPATH,
                                              "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[8]").text
            amount_total_saves = clean_stat_value(total_saves, 2)
            print("Amount of total saves:", amount_total_saves)

            goals_prevented = self.driver.find_element(By.XPATH,
                                                  "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[8]").text
            amount_goals_prevented = clean_stat_value(goals_prevented, 2)
            print("Amount of goals prevented:", amount_goals_prevented)

            passes_completed = self.driver.find_element(By.XPATH,
                                                   "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[6]").text
            amount_passes_completed = clean_stat_value(passes_completed, 3)
            print("Amount of passes completed:", amount_passes_completed)

            passes_completed_percentage = self.driver.find_element(By.XPATH,
                                                              "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[6]").text
            amount_passes_completed_percentage = clean_stat_value(passes_completed_percentage, 4, is_percentage=True)
            print("Percentage of passes completed:", amount_passes_completed_percentage)

            clean_sheets = self.driver.find_element(By.XPATH,
                                               "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[1]").text
            amount_clean_sheets = clean_stat_value(clean_sheets, 2)
            print("Amount of clean sheets:", amount_clean_sheets)

            error_leading_to_shot = self.driver.find_element(By.XPATH,
                                                        "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[8]").text
            amount_error_leading_to_shot = clean_stat_value(error_leading_to_shot, 4)
            print("Amount of erros leading to shot:", amount_error_leading_to_shot)

            error_leading_to_goal = self.driver.find_element(By.XPATH,
                                                        "//div[@class='Box kNZKNS']//div[7]//div[1]//div[2]//div[8]").text
            amount_error_leading_to_goal = clean_stat_value(error_leading_to_goal, 4)
            print("Amount of errors leading to goal:", amount_error_leading_to_goal)
            
        except TimeoutException:
            print("Error: Element took too long to load.")
        except Exception as e:
            print(f"Error extracting {player_name}'s data: {e}")

    def scrape_field_player_data(self, player_link):
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
            print("Amount of games played:", amount_games)

            minutes_played = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[4]//div[1]//div[2]//div[4]").text
            amount_minutes_played = clean_stat_value(minutes_played, 3)
            print("Amount of minutes played:", amount_minutes_played)

            goals = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[1]").text
            amount_goals = clean_stat_value(goals, 1)
            print("Amount of goals:", amount_goals)

            xG_element = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[2]").text
            if "Expected Goals (xG)" in xG_element:
                amount_xG = clean_stat_value(xG_element, 3)
                print("Amount of xG:", amount_xG)

                shots_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[5]").text
                amount_shots_per_game = shots_per_game.split()[3]
                print("Amount of shots per game:", amount_shots_per_game)

                shots_target_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[5]//div[1]//div[2]//div[6]").text
                amount_shots_target_per_game = clean_stat_value(shots_target_per_game, 5)
                print("Amount of shots on target per game:", amount_shots_target_per_game)

            assists = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[1]").text
            amount_assists = clean_stat_value(assists, 1)
            print("Amount of assists:", amount_assists)

            xA = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[2]").text
            amount_xA = clean_stat_value(xA, 3)
            print("Amount of xA:", amount_xA)

            big_chances_created = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[4]").text
            amount_big_chances_created = clean_stat_value(big_chances_created, 3)
            print("Amount of big chances created:", amount_big_chances_created)

            key_passes_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[5]").text
            amount_key_passes_per_game = clean_stat_value(key_passes_per_game, 2)
            print("Amount of key passes per game:", amount_key_passes_per_game)

            passes_completed_per_game = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[6]").text
            amount_passes_completed_per_game = clean_stat_value(passes_completed_per_game, 3)
            print("Amount of passes completed per game:", amount_passes_completed_per_game)

            passes_completed_per_game_percentage = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[6]//div[1]//div[2]//div[6]").text
            amount_passes_completed_per_game_percentage = clean_stat_value(passes_completed_per_game_percentage, 4)
            print("Pass completion percentage:", amount_passes_completed_per_game_percentage)

            succesful_dribles = self.driver.find_element(By.XPATH, "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[1]").text
            amount_succesful_dribles = clean_stat_value(succesful_dribles, 2)
            print("Successful dribbles per game:", amount_succesful_dribles)

            total_duels_won_per_game = self.driver.find_element(By.XPATH,
                                                        "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[2]").text
            amount_total_duels_won_per_game = clean_stat_value(total_duels_won_per_game, 3)
            print("Total duels won per game:", amount_total_duels_won_per_game)

            total_duels_won_percentage = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[2]").text
            amount_total_duels_won_percentage = clean_stat_value(total_duels_won_percentage, 4)
            print("Percentage of total duels won per game:", amount_total_duels_won_percentage)

            ground_duels_won_per_game = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[3]").text
            amount_ground_duels_won_per_game = clean_stat_value(ground_duels_won_per_game, 3)
            print("Ground duels won per game:", amount_ground_duels_won_per_game)

            ground_duels_won_per_game_percentage = self.driver.find_element(By.XPATH,
                                                                    "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[3]").text
            amount_ground_duels_won_per_game_percentage = clean_stat_value(ground_duels_won_per_game_percentage, 4)
            print("Percentage of ground duels won per game:", amount_ground_duels_won_per_game_percentage)

            aerial_duels_won_per_game = self.driver.find_element(By.XPATH,
                                                                "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[4]").text
            amount_aerial_duels_won_per_game = clean_stat_value(aerial_duels_won_per_game, 3)
            print("Aerial duels won per game:", amount_aerial_duels_won_per_game)

            aerial_duels_won_per_game_percentage = self.driver.find_element(By.XPATH,
                                                                        "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[4]").text
            amount_aerial_duels_won_per_game_percentage = clean_stat_value(aerial_duels_won_per_game_percentage, 4)
            print("Percentage of aerial duels won per game:", amount_aerial_duels_won_per_game_percentage)

            possession_lost_per_game = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[5]").text
            amount_possession_lost_per_game = clean_stat_value(possession_lost_per_game, 2)
            print("Possession lost per game:", amount_possession_lost_per_game)

            fouls_received_per_game = self.driver.find_element(By.XPATH,
                                                            "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[7]").text
            amount_fouls_received_per_game = clean_stat_value(fouls_received_per_game, 2)
            print("Fouls received per game:", amount_fouls_received_per_game)

            offside_per_game = self.driver.find_element(By.XPATH,
                                                    "//div[@class='Box kNZKNS']//div[8]//div[1]//div[2]//div[8]").text
            amount_offside_per_game = clean_stat_value(offside_per_game, 1)
            print("Offsides per game:", amount_offside_per_game)

        except TimeoutException:
            print("Error: Element took too long to load.")
        except Exception as e:
            print(f"Error extracting {player_name}'s data: {e}")

    def scrape_players_data(self):
        """
        Scrapes player data from a table on the webpage.

        This method waits for the player data table to be present, retrieves each row 
        in the table, and extracts information about each player. The extracted data is 
        stored in a list, which can later be processed or saved.

        Raises:
            TimeoutException: If the table or its rows take too long to load.
            Exception: For any other error that may occur while scraping player data.
        """

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
                if player['position'].lower() == "goalkeeper":
                    self.scrape_goalkeeper_data(player['link'])
                else:
                    self.scrape_field_player_data(player['link'])
        except Exception as e:
            print(f"Error: {e}")
