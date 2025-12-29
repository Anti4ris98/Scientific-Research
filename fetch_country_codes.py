import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_and_save_country_codes():
    """Fetches the country code table from the World Bank website and saves it to a CSV file."""
    url = "https://wits.worldbank.org/wits/wits/witshelp/content/codes/country_codes.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    
    data = []
    headers = ["country", "iso3", "code"]

    # Iterate over table rows, skipping the header row
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        # Ensure we have at least 3 columns to avoid errors with malformed rows
        if len(cols) >= 3:
            country_name = cols[0].get_text(strip=True)
            iso3_code = cols[1].get_text(strip=True)
            numeric_code = cols[2].get_text(strip=True)
            data.append([country_name, iso3_code, numeric_code])

    df = pd.DataFrame(data, columns=headers)
    df['code'] = pd.to_numeric(df['code']) # Convert numeric code to integer for matching
    
    output_path = 'country_codes.csv'
    df.to_csv(output_path, index=False)
    print(f"Successfully fetched and saved country codes to {output_path}")

if __name__ == "__main__":
    fetch_and_save_country_codes()
