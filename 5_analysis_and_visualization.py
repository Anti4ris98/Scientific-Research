
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def analyze_and_visualize(input_path, output_dir):
    """
    Performs data analysis and creates visualizations to test research hypotheses.
    """
    try:
        print("Starting analysis and visualization...")
        df = pd.read_csv(input_path)

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # --- 1. Correlation Matrix (for H2) ---
        print("Generating correlation matrix...")
        plt.figure(figsize=(10, 8))
        correlation_matrix = df[['ecommerce_sales_usd_millions', 'internet_usage_percent', 'conflict_deaths_total']].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix of Key Variables')
        correlation_path = os.path.join(output_dir, 'correlation_matrix.png')
        plt.savefig(correlation_path)
        plt.close()
        print(f"Correlation matrix saved to {correlation_path}")

        # --- 2. Box Plot for Conflict Intensity vs. E-commerce (for H3) ---
        print("Generating box plot for conflict intensity analysis...")
        # Define "high conflict" vs "low conflict" countries
        # Let's use the total number of deaths as a proxy for conflict intensity
        conflict_intensity = df.groupby('country')['conflict_deaths_total'].sum()
        high_conflict_countries = conflict_intensity[conflict_intensity > conflict_intensity.quantile(0.75)].index

        df['conflict_intensity_group'] = df['country'].apply(lambda x: 'High Conflict' if x in high_conflict_countries else 'Low Conflict')

        # Filter for years with global crises
        df_crisis = df[df['is_global_crisis_year'] == 1]

        plt.figure(figsize=(10, 6))
        sns.boxplot(x='conflict_intensity_group', y='ecommerce_sales_usd_millions', data=df_crisis)
        plt.title('E-commerce Sales During Global Crises: High vs. Low Conflict Countries')
        plt.xlabel('Conflict Intensity Group')
        plt.ylabel('E-commerce Sales (USD Millions)')
        boxplot_path = os.path.join(output_dir, 'conflict_intensity_boxplot.png')
        plt.savefig(boxplot_path)
        plt.close()
        print(f"Box plot saved to {boxplot_path}")

    except Exception as e:
        print(f"An error occurred during analysis: {e}")

def main():
    input_path = 'final_dataset.csv'
    output_dir = 'visualizations'
    analyze_and_visualize(input_path, output_dir)

if __name__ == '__main__':
    main()
