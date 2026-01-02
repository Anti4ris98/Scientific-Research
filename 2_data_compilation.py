
import pandas as pd
import os

def compile_data(input_dir, output_path):
    """
    Reads processed data files, merges them into a single DataFrame,
    and saves the result.
    """
    try:
        print("Compiling all processed data...")

        # Define paths to processed files
        conflicts_path = os.path.join(input_dir, 'conflicts.csv')
        internet_usage_path = os.path.join(input_dir, 'internet_usage.csv')
        ecommerce_path = os.path.join(input_dir, 'ecommerce_sales.csv')

        # Read the processed files
        df_conflicts = pd.read_csv(conflicts_path)
        df_internet = pd.read_csv(internet_usage_path)
        df_ecommerce = pd.read_csv(ecommerce_path)

        # Standardize country names before merging
        country_mapping = {
            'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
            'Cambodia (Kampuchea)': 'Cambodia',
            'DR Congo (Zaire)': 'DR Congo',
            'Madagascar (Malagasy)': 'Madagascar',
            'Myanmar (Burma)': 'Myanmar',
            'Netherlands (Kingdom of the)': 'Netherlands',
            'Russia (Soviet Union)': 'Russia',
            'Serbia (Yugoslavia)': 'Serbia',
            'United States of America': 'United States',
            'Yemen (North Yemen)': 'Yemen',
            'Zimbabwe (Rhodesia)': 'Zimbabwe',
        }

        df_conflicts['country'] = df_conflicts['country'].replace(country_mapping)
        df_ecommerce['country'] = df_ecommerce['country'].replace(country_mapping)

        # The internet data uses 'country_or_region', let's rename it to 'country'
        df_internet.rename(columns={'country_or_region': 'country'}, inplace=True)

        # Perform the merges
        # First, merge conflicts and e-commerce data
        df_merged = pd.merge(df_conflicts, df_ecommerce, on=['country', 'year'], how='outer')

        # Now, merge the result with internet usage data
        df_final_merged = pd.merge(df_merged, df_internet, on=['country', 'year'], how='outer')

        # Save the compiled data
        df_final_merged.to_csv(output_path, index=False)
        print(f"Compiled data saved to {output_path}")

    except Exception as e:
        print(f"Error compiling data: {e}")


def main():
    input_dir = 'processed_data'
    output_path = 'compiled_data.csv'

    compile_data(input_dir, output_path)

if __name__ == '__main__':
    main()
