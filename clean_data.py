import pandas as pd
import numpy as np
import os

def clean_ecommerce_data(filepath):
    """
    Cleans and standardizes the UNCTAD e-commerce data.
    """
    print(f"Cleaning e-commerce data from: {filepath}")
    df = pd.read_csv(filepath)
    # Apply filters (CORRECTED: EnterpriseSize is an integer 0)
    ecom_filtered = df[
        (df['Market'] == 'C00001') &          # Total market
        (df['EnterpriseSize'] == 0) &         # All enterprise sizes
        (df['ECommerceSale'] == 'TOTURN') &   # Total turnover
        (df['IsicRev4ECommActivity'] == 'TOT') # Total ISIC activity
    ].copy()

    # Select and rename columns
    ecom_clean = ecom_filtered[['Economy Label', 'Economy', 'Year', 'Percentage in total turnover']].rename(
        columns={
            'Economy Label': 'country_name',
            'Economy': 'country_code',
            'Year': 'year',
            'Percentage in total turnover': 'ecom_share'
        }
    )
    
    ecom_clean['ecom_share'] = pd.to_numeric(ecom_clean['ecom_share'], errors='coerce')

    return ecom_clean

def clean_internet_users_data(filepath):
    """
    Cleans and standardizes the internet users and GDP data.
    """
    print(f"Cleaning internet users data from: {filepath}")
    df = pd.read_excel(filepath, engine='openpyxl')

    internet_filtered = df[df['Series Code'] == 'IT.NET.USER.ZS'].copy()

    id_vars = ['Country Name', 'Series Code']
    value_vars = [col for col in df.columns if 'YR' in col]
    internet_long = internet_filtered.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name='year',
        value_name='internet_users'
    )

    internet_long['year'] = internet_long['year'].str.extract(r'(\d{4})').astype(int)
    internet_long['internet_users'] = pd.to_numeric(internet_long['internet_users'], errors='coerce')

    internet_clean = internet_long[['Country Name', 'year', 'internet_users']].rename(
        columns={'Country Name': 'country_name'}
    )
    
    internet_clean = internet_clean.dropna(subset=['internet_users'])

    return internet_clean

def clean_classification_data(filepath):
    """
    Cleans and standardizes the country classification data.
    """
    print(f"Cleaning country classification data from: {filepath}")
    df = pd.read_excel(filepath, engine='openpyxl')

    class_filtered = df.dropna(subset=['Region']).copy()

    class_clean = class_filtered[['Code', 'Economy', 'Region', 'Income group']].rename(
        columns={
            'Code': 'country_code',
            'Economy': 'country_name',
            'Region': 'region',
            'Income group': 'income_group'
        }
    )

    class_clean['dev_status'] = np.where(class_clean['income_group'] == 'High income', 1, 0)

    return class_clean

def main():
    """
    Main function to run all cleaning operations.
    """
    DATA_DIR = 'diploma_project/diplom/datasets'
    ecom_file = os.path.join(DATA_DIR, 'US_ECommerceTotal.csv')
    internet_file = os.path.join(DATA_DIR, 'internet_users_to_GDP.xlsx')
    class_file = os.path.join(DATA_DIR, 'CLASS_2025_10_07.xlsx')

    ecom_clean = clean_ecommerce_data(ecom_file)
    internet_clean = clean_internet_users_data(internet_file)
    class_clean = clean_classification_data(class_file)

    ecom_clean.to_csv('ecom_clean.csv', index=False)
    internet_clean.to_csv('internet_clean.csv', index=False)
    class_clean.to_csv('class_clean.csv', index=False)
    print("\nSuccessfully saved cleaned data to CSV files.")

    print("\n--- Cleaned E-commerce Data ---")
    print(ecom_clean.head())
    print("\n--- Cleaned Internet Users Data ---")
    print(internet_clean.head())
    print("\n--- Cleaned Country Classification Data ---")
    print(class_clean.head())

if __name__ == "__main__":
    main()
