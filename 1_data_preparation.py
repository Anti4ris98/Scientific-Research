
import pandas as pd
import os
import openpyxl  # Required for pandas to read xlsx files

def prepare_conflict_data(input_path, output_path):
    """
    Reads raw conflict data, aggregates it by country and year,
    and saves the processed data.
    """
    try:
        print("Processing conflict data...")
        df = pd.read_excel(input_path, sheet_name='GEDEvent_v25_1')

        # Select relevant columns
        df = df[['country', 'year', 'best']]

        # Rename columns for clarity
        df.rename(columns={'best': 'deaths_total'}, inplace=True)

        # Aggregate data by country and year, summing the deaths
        df_agg = df.groupby(['country', 'year'])['deaths_total'].sum().reset_index()

        df_agg.to_csv(output_path, index=False)
        print(f"Conflict data saved to {output_path}")
    except Exception as e:
        print(f"Error processing conflict data: {e}")

def prepare_internet_usage_data(input_path, output_path):
    """
    Reads raw ICT data from the 'By urban-rural area' sheet, extracts total internet usage percentage by region,
    cleans it, and saves the processed data.
    """
    try:
        print("Processing internet usage data from 'By urban-rural area' sheet...")
        df = pd.read_excel(input_path, sheet_name='By urban-rural area', header=4)

        # Rename the first column to 'country'.
        df.rename(columns={df.columns[0]: 'country'}, inplace=True)

        # Find the block with internet usage data
        # We need to find where the internet usage block starts. It is identified by a specific string.
        start_index = df[df['country'].str.contains('Percentage of individuals using the Internet', na=False)].index[0]

        # Get the relevant slice of the dataframe
        df_internet = df.iloc[start_index:].copy()
        df_internet.reset_index(drop=True, inplace=True)

        # The first row now contains the metric, let's clean the 'country' column
        df_internet['country'] = df_internet['country'].str.replace('Percentage of individuals using the Internet, total', '').str.strip()
        df_internet = df_internet.iloc[1:].copy() # Remove the header row

        # Identify year columns
        year_cols = [col for col in df_internet.columns if str(col).isdigit() or (isinstance(col, str) and '.' in col and col.replace('.', '', 1).isdigit())]

        # Select the relevant columns
        df_internet = df_internet[['country'] + year_cols]

        # Clean up year column names
        cleaned_year_cols = [str(col).split('.')[0] for col in year_cols]
        df_internet.columns = ['country'] + cleaned_year_cols

        # Melt to long format
        internet_long = pd.melt(df_internet, id_vars=['country'], var_name='year', value_name='internet_usage_percent')

        # Clean data
        internet_long.dropna(subset=['internet_usage_percent', 'country'], inplace=True)
        internet_long = internet_long[internet_long['country'] != '']
        internet_long['year'] = internet_long['year'].astype(int)

        internet_long.to_csv(output_path, index=False)
        print(f"Internet usage data saved to {output_path}")

    except Exception as e:
        print(f"Error processing internet usage data: {e}")


def prepare_ecommerce_data(total_path, international_path, output_path):
    """
    Reads total and international e-commerce data, combines them,
    cleans the data, and saves the result.
    """
    try:
        print("Processing e-commerce data...")
        df_total = pd.read_csv(total_path)
        df_intl = pd.read_csv(international_path)

        # Combine the two datasets
        df = pd.concat([df_total, df_intl], ignore_index=True)

        # Select relevant columns
        df = df[['Year', 'Economy Label', 'US$ at current prices in millions']]

        # Rename columns
        df.rename(columns={
            'Year': 'year',
            'Economy Label': 'country',
            'US$ at current prices in millions': 'ecommerce_sales_usd_millions'
        }, inplace=True)

        # Drop rows with missing sales data
        df.dropna(subset=['ecommerce_sales_usd_millions'], inplace=True)

        # Aggregate by country and year to sum up sales from different categories
        df_agg = df.groupby(['country', 'year'])['ecommerce_sales_usd_millions'].sum().reset_index()

        df_agg.to_csv(output_path, index=False)
        print(f"E-commerce data saved to {output_path}")
    except Exception as e:
        print(f"Error processing e-commerce data: {e}")


def main():
    # Define file paths
    conflict_data_path = 'datasets/GEDEvent_v25_1.xlsx'
    internet_data_path = 'datasets/ITU_regional_global_Key_ICT_indicator_aggregates_Nov_2025.xlsx'
    ecommerce_total_path = 'datasets/US_ECommerceTotal.csv'
    ecommerce_intl_path = 'datasets/US_ECommerceInternational.csv'

    output_dir = 'processed_data'

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each dataset
    prepare_conflict_data(conflict_data_path, f'{output_dir}/conflicts.csv')
    prepare_internet_usage_data(internet_data_path, f'{output_dir}/internet_usage.csv')
    prepare_ecommerce_data(ecommerce_total_path, ecommerce_intl_path, f'{output_dir}/ecommerce_sales.csv')

if __name__ == '__main__':
    main()
