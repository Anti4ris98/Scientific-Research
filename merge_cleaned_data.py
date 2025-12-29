import pandas as pd

def build_panel_dataset():
    """
    Loads cleaned data, standardizes country names, merges into a country-year panel,
    calculates growth rates, and saves the final dataset.
    """
    # 1. Load the cleaned datasets
    try:
        ecom_df = pd.read_csv('ecom_clean.csv')
        internet_df = pd.read_csv('internet_clean.csv')
        class_df = pd.read_csv('class_clean.csv')
        print("Successfully loaded all cleaned CSV files.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure all cleaned CSV files are in the current directory.")
        return

    # 2. Standardize country names for robust merging
    country_name_map = {
        'Republic of Korea': 'Korea, Rep.',
        'United States of America': 'United States'
    }
    ecom_df['country_name'] = ecom_df['country_name'].replace(country_name_map)
    internet_df['country_name'] = internet_df['country_name'].replace(country_name_map)
    print("Standardized country names across datasets.")

    # 3. Merge the datasets
    panel = pd.merge(
        ecom_df,
        internet_df,
        on=['country_name', 'year'],
        how='outer'
    )
    
    panel = pd.merge(
        panel,
        class_df,
        on='country_name',
        how='left'
    )
    print("Successfully merged the datasets.")
    
    # 4. Restrict year and data based on available data
    panel = panel.dropna(subset=['ecom_share', 'internet_users', 'country_code_y'])
    
    panel['year'] = panel['year'].astype(int)
    
    min_year = int(panel['year'].min())
    max_year = int(panel['year'].max())
    print(f"Restricted dataset to the common period of {min_year}–{max_year}.")

    # 5. Create the e-commerce growth column
    panel = panel.sort_values(by=['country_name', 'year'])
    panel['ecom_growth'] = panel.groupby('country_name')['ecom_share'].pct_change()
    print("Calculated year-over-year e-commerce growth.")

    # 6. Finalize the DataFrame structure and data types
    panel['dev_status'] = panel['dev_status'].astype(int)
    
    final_cols = [
        'country_code_y', 'country_name', 'year', 'region', 'income_group', 'dev_status',
        'ecom_share', 'internet_users', 'ecom_growth'
    ]
    panel = panel[final_cols]
    panel = panel.rename(columns={'country_code_y': 'country_code'})

    # 7. Save the final dataset
    output_path = 'panel_dataset.csv'
    panel.to_csv(output_path, index=False)
    print(f"\nSuccessfully saved the final panel dataset to {output_path}")

    # 8. Print requested outputs
    print("\n--- Final Panel Dataset Head ---")
    print(panel.head())
    
    print("\n--- Unique Income Groups ---")
    print(panel['income_group'].unique())
    
    print("\n--- Panel Dimensions ---")
    num_countries = panel['country_name'].nunique()
    num_years = panel['year'].nunique()
    print(f"Number of countries: {num_countries}")
    print(f"Number of years: {num_years} (from {min_year} to {max_year})")
    
    return panel

if __name__ == "__main__":
    panel_dataset = build_panel_dataset()
