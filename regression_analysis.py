import pandas as pd
import statsmodels.formula.api as smf

def run_regression_analysis():
    """
    Loads the final panel dataset and runs two panel OLS regressions
    with country and year fixed effects.
    """
    # 1. Load the dataset
    try:
        panel = pd.read_csv('panel_dataset_with_crises.csv')
        print("Successfully loaded panel_dataset_with_crises.csv.")
    except FileNotFoundError:
        print("Error: panel_dataset_with_crises.csv not found.")
        return

    # 2. Prepare the data for regression
    # The dependent variable is ecom_growth. Drop rows where it's missing.
    # This happens for the first year of data for each country.
    reg_data = panel.dropna(subset=['ecom_growth'])
    print(f"Prepared data for regression. Using {len(reg_data)} observations.")

    # 3. Define and run Model 1 for the 2008-09 crisis
    # Note: The data only starts from 2015, so the crisis_2008_09 dummy will be all zeros.
    # The regression will still run, but the crisis coefficient will likely be dropped
    # or result in an error if there's no variation. We will proceed to show how it's done.
    
    formula_2008_09 = (
        "ecom_growth ~ crisis_2008_09 + dev_status + crisis_2008_09 * dev_status "
        "+ C(country_code) + C(year)"
    )
    
    print("\n--- Model 1: Regression for 2008-09 Crisis ---")
    print(f"Formula: {formula_2008_09}")
    
    # Check if there is any variation in the crisis dummy
    if reg_data['crisis_2008_09'].nunique() > 1:
        model_2008_09 = smf.ols(formula=formula_2008_09, data=reg_data).fit()
        print(model_2008_09.summary())
    else:
        print("Skipping regression for 2008-09: No crisis years present in the dataset.")

    # 4. Define and run Model 2 for the 2020-21 crisis
    formula_2020_21 = (
        "ecom_growth ~ crisis_2020_21 + dev_status + crisis_2020_21 * dev_status "
        "+ C(country_code) + C(year)"
    )
    
    print("\n--- Model 2: Regression for 2020-21 Crisis ---")
    print(f"Formula: {formula_2020_21}")

    model_2020_21 = smf.ols(formula=formula_2020_21, data=reg_data).fit()
    
    # Print a focused summary of coefficients
    print("\n--- Regression Summary (Coefficients, Std. Err., R-squared) ---")
    summary_table = model_2020_21.summary2().tables[1]
    rsquared = model_2020_21.rsquared_adj
    
    print(summary_table[['Coef.', 'Std.Err.', 'P>|t|']])
    print(f"\nAdjusted R-squared: {rsquared:.4f}")

if __name__ == "__main__":
    run_regression_analysis()
