
import pandas as pd

def feature_engineer(input_path, output_path):
    """
    Loads compiled data, creates new features, handles missing values,
    and saves the engineered dataset.
    """
    try:
        print("Starting feature engineering...")
        df = pd.read_csv(input_path)

        # --- 1. Handle Missing Values ---
        print("Handling missing values...")
        # Fill missing deaths and e-commerce sales with 0, assuming NaN means no events/sales
        df['deaths_total'].fillna(0, inplace=True)
        df['ecommerce_sales_usd_millions'].fillna(0, inplace=True)

        # For internet usage, forward-fill and then back-fill within each country group
        df.sort_values(by=['country', 'year'], inplace=True)
        df['internet_usage_percent'] = df.groupby('country')['internet_usage_percent'].ffill().bfill()


        # --- 2. Create New Features ---
        print("Creating new features...")
        # Create a binary flag for conflict
        df['is_conflict'] = (df['deaths_total'] > 0).astype(int)

        # Create a flag for major global crises
        def get_crisis_flag(year):
            if 2000 <= year <= 2001:  # Dot-com bubble burst
                return 1
            if 2008 <= year <= 2009:  # Global Financial Crisis
                return 1
            if 2020 <= year <= 2022:  # COVID-19 Pandemic
                return 1
            return 0

        df['major_crisis_flag'] = df['year'].apply(get_crisis_flag)

        # Save the engineered data
        df.to_csv(output_path, index=False)
        print(f"Feature-engineered data saved to {output_path}")

    except Exception as e:
        print(f"Error during feature engineering: {e}")


def main():
    input_path = 'compiled_data.csv'
    output_path = 'featured_data.csv'

    feature_engineer(input_path, output_path)

if __name__ == '__main__':
    main()
