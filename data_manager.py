import pandas as pd
import numpy as np

def clean_stat_value(raw_text, index, is_percentage=False):
    """
    Cleans and converts a statistical value from a text string.
    
    Parameters:
    - raw_text (str): The full text from which to extract the value.
    - index (int): The index of the word in the split text to extract.
    
    Returns:
    - float: The cleaned and converted value.
    """
    # Extract the specific word based on the index and remove parentheses
    value_str = raw_text.split()[index]

    return value_str

def create_dataframe(teams_data):
    """
    Convert the structured dictionary into a pandas DataFrame with multi-level indexing
    and account for missing stats between field players and goalkeepers.

    Parameters:
    - teams_data (dict): The dictionary containing team and player data.

    Returns:
    - pd.DataFrame: The resulting DataFrame with teams and players as multi-level indices.
    """

    # Sample structure with all possible columns for both field players and goalkeepers
    columns = [
        # General stats (applicable to both field players and goalkeepers)
        'Games Played', 'Minutes Played',

        # Field player stats
        'Goals', 'Expected Goals (xG)', 'Shots Per Game', 'Shots on Target Per Game',
        'Assists', 'Expected Assists (xA)', 'Big Chances Created', 'Key Passes Per Game',
        'Passes Completed Per Game', 'Pass Completion Percentage', 'Successful Dribbles Per Game',
        'Total Duels Won Per Game', 'Total Duels Won Percentage', 'Ground Duels Won Per Game',
        'Ground Duels Won Percentage', 'Aerial Duels Won Per Game', 'Aerial Duels Won Percentage',
        'Possession Lost Per Game', 'Fouls Received Per Game', 'Offsides Per Game',
        
        # Goalkeeper stats
        'Goals Conceded Per Game', 'Penalties Saved', 'Saves Per Game', 'Saves Per Game Percentage',
        'Goals Conceded', 'Total Saves', 'Goals Prevented', 'Passes Completed', 
        'Percentage of Passes Completed', 'Clean Sheets', 'Errors leading to shot', 'Errors leading to goal'
    ]

    data = []

    for team_name, players in teams_data.items():
        for player_name, stats in players.items():
            # Ensure every player has the full set of columns with missing stats as NaN
            player_data = {col: stats.get(col, np.nan) for col in columns}
            player_data['Team'] = team_name
            player_data['Player Name'] = player_name
            data.append(player_data)
    
    # Create DataFrame and set multi-level index
    df = pd.DataFrame(data)
    df.set_index(['Team', 'Player Name'], inplace=True)
    return df
