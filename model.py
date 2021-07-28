import pandas as pd 

from app import app
# Read the csv file one time

with app.open_resource("static/data/Food_Production.csv") as f:
    foods_df = pd.read_csv(f)
    foods_df = foods_df[['Food product', 'Total_emissions']]
    foods_df = foods_df.set_index("Food product")
    foods_df = foods_df.sort_values(by=['Total_emissions'])
    foods_dict = foods_df.to_dict('index')
    foods_list = list(foods_dict.keys())

def get_foods_list():
    return sorted(foods_list)

def return_total_emissions(ingredients):
    total_emissions = 0
    for ingredient in ingredients:
        ingredient = ingredient.split(':')[0]
        ingredient = ingredient.strip()
        temporary = foods_dict.get(ingredient)['Total_emissions']
        total_emissions += temporary
    return total_emissions

# print(return_total_emissions('Milk'))
