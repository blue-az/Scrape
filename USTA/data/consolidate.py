import pandas as pd

# Read the text file, handling potential whitespace issues
def read_custom_file(filepath):
    # Use regex to split on multiple whitespaces
    df = pd.read_csv(filepath, sep=r'\s+', engine='python', 
                     dtype={'Match': str, 'Date': str, 'Player1': str, 'Opponent': str, 'Year': str})
    return df

# Convert dates to datetime format
def convert_dates(df):
    def parse_date(row):
        try:
            # Combine month, date, and year
            month = row['Match'].strip()
            day = row['Date'].strip()
            year = row['Year'].strip()
            
            # Create full date string
            full_date_str = f"{month} {day} {year}"
            
            # Parse the date
            return pd.to_datetime(full_date_str, format='%b %d %Y')
        except Exception as e:
            print(f"Error parsing date: {full_date_str} - {e}")
            return pd.NaT

    # Apply date parsing
    df['Date'] = df.apply(parse_date, axis=1)
    
    # Drop the Year column and Match column (since month info is now in Date)
    df = df.drop(columns=['Year', 'Match'])
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df

# Main processing function
def process_file(filepath):
    # Read the file
    df = read_custom_file(filepath)
    
    # Convert dates
    df = convert_dates(df)
    
    return df

# Example usage
filepath = 'full.txt'
processed_df = process_file(filepath)

# Display the processed DataFrame
print(processed_df)

# Optional: Save to a new CSV if needed
processed_df.to_csv('processed_full.csv', index=False)
