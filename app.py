# -- Flask Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
from flask import session
## Additional Imports
import datetime as dt
import math
from bson.objectid import ObjectId
import os
# -- Initialization section --
app = Flask(__name__)
app.jinja_env.globals['current_time'] = dt.datetime.now()
app.secret_key = os.urandom(24)
import model as model

from dotenv import load_dotenv
load_dotenv()
from flask_pymongo import PyMongo
MONGO_DBNAME = os.getenv("MONGO_DBNAME")
MONGO_DBUSERNAME = os.getenv("MONGO_DBUSERNAME")
MONGO_DBPASSWORD = os.getenv("MONGO_DBPASSWORD")
MONGO_DBCLUSTER = os.getenv("MONGO_DBCLUSTER","cluster0-kxrbn")
app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_DBUSERNAME}:{MONGO_DBPASSWORD}@{MONGO_DBCLUSTER}.mongodb.net/{MONGO_DBNAME}?retryWrites=true'
mongo = PyMongo(app)
# -- Routes --
@app.route('/')
@app.route('/index')
def index():
    data = {
    }
    return render_template('index.html', data=data)

@app.route('/about_us')
def about_us():
    data = {
    }
    return render_template('about_us.html', data=data)

@app.route('/meals_view')
def meals_view():
    data = {
        'meals_view':model.get_foods_list(),
        'foods_dict': model.foods_dict
    }
    return render_template('meals_view.html', data=data)

@app.route('/sus_ingredients')
def sus_ingredients():
    data = {
        'sus_ingredients':model.sus_foods_list,
        'foods_dict': model.foods_dict
    }
    return render_template('sus_ingredients.html', data=data)

@app.route('/meals_add', methods=['GET','POST'])
def meals_add():
    if request.method == 'GET':
        data = {
            "foods":mongo.db.meals.find({})
        }
        return render_template('meals_add.html', data=data)
    else:
        form = request.form
        ingredients = form.getlist('Ingredients')
        print(ingredients)
        meal = {
        'meal':form['Meal'],
        'ingredients': ingredients,
        'total_emissions' : model.return_total_emissions(ingredients)
        }
        data = {
        'meal':meal
        }
        mongo.db.meals.insert(meal)

        for food in model.error_foods_list:
            if food in [ingredient.split(':')[0].strip() for ingredient in ingredients]:
                flash(f"Carbon emissions too high! Consider removing {food} from your meal; it'll help the environment.", "danger")
        return redirect(url_for('meals_add'))

@app.route('/meal_delete/<meal_id>')
def meal_delete(meal_id):
    meal_id=ObjectId(meal_id)
    query={"_id":meal_id}
    meal=mongo.db.meals.delete_one(query)
    return redirect(url_for('meals_add'))

@app.route('/filters/<meal>')
def filter(meal):
    if meal=='All':
       foods = mongo.db.meals.find({})
    else:
        foods = mongo.db.meals.find({'meal' : meal})
    data = {
    'foods': foods,
    }
    return render_template('meals_add.html', data=data)


