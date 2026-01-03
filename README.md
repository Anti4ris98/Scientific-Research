# Analysis of the Impact of World Crises on E-commerce

This project is designed to process and combine various datasets to create a single, clean dataset. The final dataset allows for the analysis of how world crises, conflicts, and internet penetration levels affect e-commerce volumes across different countries and regions.

## Project Structure

The project consists of five main scripts that must be run sequentially. Each script performs a specific stage of data processing.

### 1. `1_data_preparation.py`
- **Task:** Initial processing and cleaning of raw data.
- **Description:** This script reads the source files (`.xlsx` and `.csv`), extracts the necessary information (data on conflicts, internet usage, e-commerce sales), cleans it, and saves it into separate `.csv` files in the `processed_data/` directory.

### 2. `2_data_compilation.py`
- **Task:** Compiling the processed data into a single file.
- **Description:** This script takes the cleaned files from `processed_data/` and merges them into a single comprehensive dataset, `compiled_data.csv`, using "country/region" and "year" as keys.

### 3. `3_feature_engineering.py`
- **Task:** Creating new features.
- **Description:** This script uses `compiled_data.csv` to create new, more informative features. It handles missing values and adds flags to indicate whether a country was in conflict (`is_conflict_year`) and to mark periods of major global crises (`is_global_crisis_year`). The result is saved in `featured_data.csv`.

### 4. `4_final_dataset.py`
- **Task:** Final cleaning and formatting of the dataset.
- **Description:** This script performs advanced cleaning, including removing countries with no e-commerce data and filtering out statistical outliers. The final, clean dataset is saved to `final_dataset.csv`.

### 5. `5_analysis_and_visualization.py`
- **Task:** Performing analysis and generating visualizations.
- **Description:** This script reads the final dataset and generates a correlation matrix and a box plot to analyze the relationship between key variables and the impact of conflicts on e-commerce during crises. The visualizations are saved in the `visualizations/` directory.

## How to Run

To generate the final dataset and visualizations, you need to run all the scripts sequentially. Make sure you have the required libraries installed.

```bash
# Install dependencies
pip install -r requirements.txt
pip install matplotlib seaborn

# 1. Prepare Data
python 1_data_preparation.py

# 2. Compile Data
python 2_data_compilation.py

# 3. Feature Engineering
python 3_feature_engineering.py

# 4. Create Final Dataset
python 4_final_dataset.py

# 5. Analyze and Visualize
python 5_analysis_and_visualization.py
```

After completing all steps, you will have the `final_dataset.csv` file and a `visualizations` directory containing the generated plots.
