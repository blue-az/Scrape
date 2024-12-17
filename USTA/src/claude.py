import re
import pandas as pd

def extract_tournament_matches(tournament):
    """
    Extract dates and scores from a tournament text, grouping scores into matches
    
    Args:
        tournament (str): Text describing a tennis tournament
    
    Returns:
        dict: A dictionary with tournament dates and grouped scores
    """
    # Extract dates
    date_pattern = r'(\w+ \d+ - \w+ \d+(?:, \d{4})?)'
    dates = re.findall(date_pattern, tournament)
    
    # Score pattern to match various score formats
    score_pattern = r'(\d+-\d+(?:\(\d+-\d+\))?)'
    scores = re.findall(score_pattern, tournament)
    
    # Group scores into matches
    grouped_matches = []
    current_match = []
    
    for score in scores:
        current_match.append(score)
        
        # Assume a new match when the number of scores reaches 2
        if len(current_match) == 2:
            grouped_matches.append(current_match)
            current_match = []
    
    # Add any remaining scores if not paired
    if current_match:
        grouped_matches.append(current_match)
    
    return {
        'dates': dates[0] if dates else 'Unknown Date',
        'matches': grouped_matches
    }

def parse_tournaments_to_dataframe(tournaments):
    """
    Parse multiple tournaments and create a DataFrame
    
    Args:
        tournaments (list): List of tournament texts
    
    Returns:
        pandas.DataFrame: DataFrame of tournament matches
    """
    all_matches = []
    
    for tournament in tournaments:
        tournament_data = extract_tournament_matches(tournament)
        
        # Create a DataFrame for this tournament
        tournament_df = pd.DataFrame({
            'Tournament Date': [tournament_data['dates']] * len(tournament_data['matches']),
            'Match Scores': tournament_data['matches']
        })
        
        all_matches.append(tournament_df)
    
    # Combine all tournament DataFrames
    return pd.concat(all_matches, ignore_index=True)

def main():
    # Example tournaments
    tournament1 = """
Las Sendas Turkey Bowl
NTRP 4.0 Men's 18 & over singles
November 29 - December 01, 2024
PL-F 
1-4 4-5(3-7) 
E-SF 
2-4 1-4 
E-QF 
3-5 4-1 4-0
    """
    
    tournament2 = """
Chandler Fall Classic - Level 6
NTRP 4.5 Men's 18 & over singles
November 22 - November 24, 2024
C-F
1-6 2-6
C-SF
7-6(7-4) 6-4
    """
    
    # Parse tournaments to DataFrame
    df = parse_tournaments_to_dataframe([tournament1, tournament2])
    
    # Display the DataFrame
    print(df)
    
    # Optional: Save to CSV
    df.to_csv('tennis_matches.csv', index=False)

if __name__ == "__main__":
    main()
