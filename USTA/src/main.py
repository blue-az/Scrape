import re
import pandas as pd

def extract_raw_scores(filepath):
    """
    Extract Player1 and opponent score_id pairs from a text file,
    while skipping matches marked as "walkover" or "defaulted".
    """
    with open(filepath, 'r') as file:
        content = file.read()

    # Regex to capture matches with Player1 and opponent, and their "score_id"
    pattern = r'\| ([^\n]+)\n.*?Erik Fehn\n.*?\d+\.\d+\n(\d+)\n.*?(?:xx|UR).*?\n(\d+)\n'
    # pattern = r'\| ([^\n]+)\n.*?Erik Fehn\n.*?\d+\.\d+\n(\d+)\n.*?(?:xx|UR).*?\n(\d+)\n'
    # pattern = r'\| ([^\n]+)\n.*?Erik Fehn\n.*?\d+\.\d+\n(\d+)\n.*?xx.*?\n(\d+)\n'

    # Find all matches
    matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

    # Normalize the Tournament Date (remove "| E-QF", etc.)
    normalized_matches = [(re.sub(r'\|.*', '', date).strip(), player1_score, opponent_score) 
                          for date, player1_score, opponent_score in matches]

    # Check for "walkover" or "defaulted" in the raw content
    valid_matches = []
    for match in normalized_matches:
        date, player1_score, opponent_score = match
        match_content = content.split(date)[1]  # Get content after the date
        if "walkover" in match_content.lower() or "defaulted" in match_content.lower():
            continue  # Skip the match if it's a walkover or defaulted
        valid_matches.append(match)

    # Create DataFrame
    df = pd.DataFrame(valid_matches, columns=['Tournament Date', 'Player1 Score', 'Opponent Score'])

    return df

# File path
filepath = '/home/blueaz/Python/Scrape/USTA/data/2023.txt'

# Extract raw scores
raw_scores_df = extract_raw_scores(filepath)
print(raw_scores_df)

