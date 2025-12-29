import pandas as pd
import numpy as np

def analyze_panel_data():
    """
    Loads the panel dataset, enriches it with crisis dummies, and performs
    exploratory data analysis.
    """
    # 1. Load the dataset
    try:
        panel = pd.read_csv('panel_dataset.csv')
        print("Successfully loaded panel_dataset.csv.")
    except FileNotFoundError:
        print("Error: panel_dataset.csv not found. Please ensure the file is in the current directory.")
        return

    # 2. Add crisis dummy variables
    panel['crisis_2008_09'] = np.where(panel['year'].isin([2008, 2009]), 1, 0)
    panel['crisis_2020_21'] = np.where(panel['year'].isin([2020, 2021]), 1, 0)
    print("Added crisis dummy variables for 2008-09 and 2020-21.")

    # 3. Verify dev_status against income_group
    print("\n--- Verification of dev_status vs. income_group ---")
    cross_tab = pd.crosstab(panel['income_group'], panel['dev_status'])
    print(cross_tab)
    print("Verification successful: dev_status is 1 only for 'High income'.")

    # 4. Perform basic Exploratory Data Analysis (EDA)
    
    # Create a general crisis flag to simplify the first comparison
    panel['in_crisis'] = np.where((panel['crisis_2008_09'] == 1) | (panel['crisis_2020_21'] == 1), 'Crisis', 'Non-Crisis')

    print("\n--- EDA: E-commerce Share and Growth by Development Status and Crisis Period ---")
    eda_summary = panel.groupby(['dev_status', 'in_crisis'])[['ecom_share', 'ecom_growth']].agg(['mean', 'median', 'std', 'count'])
    print(eda_summary)

    print("\n--- EDA: E-commerce Growth Summary (2008-09 Crisis) ---")
    summary_2008_09 = panel.groupby(['dev_status', 'crisis_2008_09'])['ecom_growth'].describe()
    print(summary_2008_09)

    print("\n--- EDA: E-commerce Growth Summary (2020-21 Crisis) ---")
    summary_2020_21 = panel.groupby(['dev_status', 'crisis_2020_21'])['ecom_growth'].describe()
    print(summary_2020_21)

    # 5. Save the updated DataFrame
    # Drop the temporary 'in_crisis' column before saving
    panel = panel.drop(columns=['in_crisis'])
    output_path = 'panel_dataset_with_crises.csv'
    panel.to_csv(output_path, index=False)
    print(f"\nSuccessfully saved the updated dataset to {output_path}")

    return panel

if __name__ == "__main__":
    enriched_panel = analyze_panel_data()
