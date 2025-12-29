import pandas as pd
import os

def analyze_datasets(directory):
    files = [f for f in os.listdir(directory) if f.endswith(('.csv', '.xlsx'))]
    for file in files:
        filepath = os.path.join(directory, file)
        print(f"Analyzing file: {file}")
        try:
            if file.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath, engine='openpyxl')
            print("Columns:", df.columns.tolist())
            print("Head:")
            print(df.head())
        except Exception as e:
            print(f"Could not read file {file}. Error: {e}")
        print("-" * 50)

if __name__ == "__main__":
    analyze_datasets('diploma_project/diplom/datasets')
