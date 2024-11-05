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

