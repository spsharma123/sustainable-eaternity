import pandas as pd 

from app import app
# Read the csv file one time

with app.open_resource("static/data/Food_Production.csv") as f:
    foods_df = pd.read_csv(f)
    foods_df = foods_df[['Food product', 'Total_emissions']]
    foods_df = foods_df.set_index("Food product")
    foods_dict = foods_df.to_dict('index')
    foods_list = list(foods_dict.keys())
    # top5CO2 = foods_df['Total_emissions'].value_counts.head(5)

print(top5CO2)

def get_foods_list():
    return sorted(foods_list)

def return_total_emissions(food):
    return foods_dict.get(food)['Total_emissions']
