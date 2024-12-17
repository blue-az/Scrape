import pandas as pd

# Load your data from a file
df = pd.read_csv('full.txt', delimiter="\t")

# Function to convert 'Month Day' to 'YYYY-MM-DD' based on 'Year'
def convert_to_date(row):
    # Map month names to month numbers
    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
        'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10',
        'Nov': '11', 'Dec': '12'
    }
    
    # Split the 'Month Day' into month and day
    month, day = row['Tournament Date'].split()
    
    # Ensure day is two digits (e.g., '9' becomes '09')
    day = day.zfill(2)
    
    # Look up the month number and construct the full date
    month_num = month_map.get(month, 'InvalidMonth')
    if month_num == 'InvalidMonth':
        return None
    
    # Format the date in 'YYYY-MM-DD'
    return f"{row['Year']}-{month_num}-{day}"

# Apply the conversion function to create a new 'Date' column
df['Date'] = df.apply(convert_to_date, axis=1)

# Display the updated dataframe
print(df[['Date', 'Tournament Date', 'Year']])

