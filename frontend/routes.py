from flask import redirect, render_template, url_for, flash, request
from . import app
from .forms import CityForm
from backend.weather import get_forecast
from datetime import datetime, timedelta


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = CityForm()
    print(form.validate_on_submit())
    print(form.errors)
    if form.validate_on_submit():
        print('1')
        # return redirect(url_for('home2'))  
        date_from = datetime.now()
        date_to = date_from + timedelta(days=10)

        response = get_forecast(form.city.data, date_from, date_to)
        #results = []
        print(response)
        return render_template('home.html', title='Pogoda', form=form, response=response)
        # return redirect(url_for('home2'))  
    else:
        print('2') 
        flash(form.errors)  
    return render_template('home.html', title='Pogoda', form=form, response=[]) 

@app.route('/home2', methods=['GET', 'POST'])
def home2():
    return 'Hello World'
 