import pandas as pd
import os

def clean_column_names(df):
    """Cleans and standardizes DataFrame column names."""
    df.columns = df.columns.str.strip().str.lower().str.replace('[^a-zA-Z0-9_]', '_', regex=True)
    return df

def load_and_process_class(filepath):
    """Loads and processes the country classification data."""
    df = pd.read_excel(filepath, engine='openpyxl')
    df = clean_column_names(df)
    df = df[['economy', 'code', 'income_group']]
    df = df.rename(columns={'economy': 'country', 'code': 'country_code'})
    df['country'] = df['country'].astype(str)
    return df

def load_and_process_ged(filepath):
    """Loads and aggregates the conflict data."""
    df = pd.read_excel(filepath, engine='openpyxl')
    df = clean_column_names(df)
    df['country'] = df['country'].astype(str)
    conflict_df = df.groupby(['country', 'year'])['best'].sum().reset_index()
    conflict_df = conflict_df.rename(columns={'best': 'total_deaths'})
    return conflict_df

def load_and_process_internet_users(filepath):
    """Loads and melts the internet users data from wide to long format."""
    df = pd.read_excel(filepath, engine='openpyxl')
    df = clean_column_names(df)
    df = df.rename(columns={'country_name': 'country'})
    df['country'] = df['country'].astype(str)
    df_melted = df.melt(id_vars=['country', 'series_name', 'series_code'],
                        var_name='year',
                        value_name='internet_users_pct')
    df_melted['year'] = df_melted['year'].str.extract(r'(\d{4})').astype(int)
    df_melted['internet_users_pct'] = pd.to_numeric(df_melted['internet_users_pct'], errors='coerce')
    df_melted = df_melted.dropna(subset=['internet_users_pct'])
    return df_melted[['country', 'year', 'internet_users_pct']]

def load_and_process_ecommerce(total_filepath, international_filepath, country_codes_df):
    """Loads, combines, and processes e-commerce data, mapping numeric codes to country names."""
    df_total = pd.read_csv(total_filepath)
    df_int = pd.read_csv(international_filepath)
    df = pd.concat([df_total, df_int], ignore_index=True)
    df = clean_column_names(df)
    
    # Merge with country codes to get country names
    merged_df = pd.merge(df, country_codes_df, left_on='economy', right_on='code', how='left')
    
    unmapped_codes = merged_df[merged_df['country'].isnull()]['economy'].unique()
    if len(unmapped_codes) > 0:
        print("\n--- WARNING: Unmapped E-commerce Country Codes ---")
        print(f"The following {len(unmapped_codes)} numeric codes could not be mapped and will be excluded:")
        print(unmapped_codes)
        print("--------------------------------------------------\n")
    
    # Exclude unmapped rows
    merged_df = merged_df.dropna(subset=['country'])

    merged_df = merged_df[['year', 'country', 'us__at_current_prices_in_millions']]
    merged_df = merged_df.rename(columns={'us__at_current_prices_in_millions': 'ecommerce_usd_millions'})
    merged_df['country'] = merged_df['country'].astype(str)
    merged_df['ecommerce_usd_millions'] = pd.to_numeric(merged_df['ecommerce_usd_millions'], errors='coerce')
    df_agg = merged_df.groupby(['country', 'year'])['ecommerce_usd_millions'].sum().reset_index()
    return df_agg

def main():
    """Main function to orchestrate the data merging process."""
    DATA_DIR = 'diploma_project/diplom/datasets'
    
    # File paths
    class_file = os.path.join(DATA_DIR, 'CLASS_2025_10_07.xlsx')
    ged_file = os.path.join(DATA_DIR, 'GEDEvent_v25_1.xlsx')
    internet_users_file = os.path.join(DATA_DIR, 'internet_users_to_GDP.xlsx')
    ecommerce_total_file = os.path.join(DATA_DIR, 'US_ECommerceTotal.csv')
    ecommerce_int_file = os.path.join(DATA_DIR, 'US_ECommerceInternational.csv')
    country_codes_file = 'country_codes.csv'
    
    print("Loading country codes mapping...")
    country_codes_df = pd.read_csv(country_codes_file)
    
    print("Processing country classification data...")
    class_df = load_and_process_class(class_file)
    
    print("Processing conflict data...")
    ged_df = load_and_process_ged(ged_file)
    
    print("Processing internet users data...")
    internet_users_df = load_and_process_internet_users(internet_users_file)
    
    print("Processing e-commerce data...")
    ecommerce_df = load_and_process_ecommerce(ecommerce_total_file, ecommerce_int_file, country_codes_df)

    print("Merging datasets...")
    merged_df = pd.merge(ecommerce_df, internet_users_df, on=['country', 'year'], how='outer')
    merged_df = pd.merge(merged_df, ged_df, on=['country', 'year'], how='left')
    final_df = pd.merge(merged_df, class_df, on='country', how='left')

    final_df['total_deaths'] = final_df['total_deaths'].fillna(0)
    
    final_df = final_df.dropna(subset=['country']) # Final cleanup for any remaining NaNs in country column

    final_df = final_df[['country', 'country_code', 'year', 'income_group', 
                         'ecommerce_usd_millions', 'internet_users_pct', 'total_deaths']]

    output_path = 'compiled_dataset.csv'
    final_df.to_csv(output_path, index=False)
    print(f"Successfully created the compiled dataset at: {output_path}")
    print("\nFinal DataFrame head:")
    print(final_df.head())
    print("\nFinal DataFrame info:")
    final_df.info()

if __name__ == "__main__":
    main()
