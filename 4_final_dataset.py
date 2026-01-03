
import pandas as pd

def finalize_dataset(input_path, output_path):
    """
    Loads feature-engineered data, performs advanced cleaning (removes countries
    without e-commerce data and outliers), and saves the final dataset.
    """
    try:
        print("Finalizing the dataset with advanced cleaning...")
        df = pd.read_csv(input_path)

        # --- 1. Remove Countries with No E-commerce Data ---
        # Get total e-commerce sales for each country
        total_sales = df.groupby('country')['ecommerce_sales_usd_millions'].sum()
        # Find countries with zero total sales
        countries_to_remove = total_sales[total_sales == 0].index

        df = df[~df['country'].isin(countries_to_remove)]
        print(f"Removed {len(countries_to_remove)} countries with no e-commerce data.")

        # --- 2. Remove Outliers from E-commerce Sales ---
        # Calculate IQR for e-commerce sales
        Q1 = df['ecommerce_sales_usd_millions'].quantile(0.25)
        Q3 = df['ecommerce_sales_usd_millions'].quantile(0.75)
        IQR = Q3 - Q1

        # Define the outlier boundary
        outlier_boundary = Q3 + 1.5 * IQR

        # Filter out the outliers
        num_outliers = df[df['ecommerce_sales_usd_millions'] > outlier_boundary].shape[0]
        df = df[df['ecommerce_sales_usd_millions'] <= outlier_boundary]
        print(f"Removed {num_outliers} outliers from e-commerce sales data.")

        # --- 3. Final Formatting ---
        df['internet_usage_percent'].fillna(0, inplace=True)
        df['year'] = df['year'].astype(int)
        df['deaths_total'] = df['deaths_total'].astype(int)
        df['is_conflict'] = df['is_conflict'].astype(int)
        df['major_crisis_flag'] = df['major_crisis_flag'].astype(int)

        df.rename(columns={
            'deaths_total': 'conflict_deaths_total',
            'is_conflict': 'is_conflict_year',
            'major_crisis_flag': 'is_global_crisis_year'
        }, inplace=True)

        final_columns = [
            'country', 'year', 'ecommerce_sales_usd_millions', 'internet_usage_percent',
            'conflict_deaths_total', 'is_conflict_year', 'is_global_crisis_year'
        ]
        df = df[final_columns]

        # --- 4. Save Final Dataset ---
        df.to_csv(output_path, index=False)
        print(f"Final, cleaned dataset saved to {output_path}")

    except Exception as e:
        print(f"An error occurred during finalization: {e}")

if __name__ == '__main__':
    input_path = 'featured_data.csv'
    output_path = 'final_dataset.csv'
    finalize_dataset(input_path, output_path)
