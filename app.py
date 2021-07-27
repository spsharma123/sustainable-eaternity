# -- Flask Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
## Additional Imports
import datetime as dt

# -- Initialization section --
app = Flask(__name__)
app.jinja_env.globals['current_time'] = dt.datetime.now()
import model as model
import os
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
        'meals_view':model.get_foods_list()
    }
    return render_template('meals_view.html', data=data)

@app.route('/sus_ingredients')
def sus_ingredients():
    data = {
    'sus_ingredients': mongo.db.sus_ingredients.find({}),
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
        meal = {
        'meal':form['Meal'],
        'ingredients':form.getlist('Ingredients'),
        }
        data = {
        'meal':meal
        }
        mongo.db.meals.insert(meal)
        return redirect(url_for('meals_add'))