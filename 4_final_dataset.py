
import pandas as pd

def finalize_dataset(input_path, output_path):
    """
    Loads the feature-engineered data, performs final cleaning and formatting,
    and saves the final dataset ready for visualization.
    """
    try:
        print("Finalizing the dataset...")
        df = pd.read_csv(input_path)

        # --- 1. Final Missing Value Treatment ---
        # Fill any remaining NaNs in internet_usage_percent with 0.
        # This is an assumption that no data means 0% penetration, which simplifies visualization.
        df['internet_usage_percent'].fillna(0, inplace=True)
        print("Filled remaining missing values.")

        # --- 2. Correct Data Types ---
        df['year'] = df['year'].astype(int)
        df['deaths_total'] = df['deaths_total'].astype(int)
        df['is_conflict'] = df['is_conflict'].astype(int)
        df['major_crisis_flag'] = df['major_crisis_flag'].astype(int)
        print("Corrected data types.")

        # --- 3. Rename and Reorder Columns for Clarity ---
        df.rename(columns={
            'deaths_total': 'conflict_deaths_total',
            'is_conflict': 'is_conflict_year',
            'major_crisis_flag': 'is_global_crisis_year'
        }, inplace=True)

        final_columns = [
            'country',
            'year',
            'ecommerce_sales_usd_millions',
            'internet_usage_percent',
            'conflict_deaths_total',
            'is_conflict_year',
            'is_global_crisis_year'
        ]
        df = df[final_columns]
        print("Renamed and reordered columns.")

        # --- 4. Save the Final Dataset ---
        df.to_csv(output_path, index=False)
        print(f"Final, clean dataset saved to {output_path}")

    except Exception as e:
        print(f"An error occurred during finalization: {e}")

def main():
    input_path = 'featured_data.csv'
    output_path = 'final_dataset.csv'

    finalize_dataset(input_path, output_path)

if __name__ == '__main__':
    main()
