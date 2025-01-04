from flask import redirect, render_template, url_for, flash, request
from pogoda_app import app
from pogoda_app.forms import CityForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = CityForm()
    if form.validate_on_submit():
        # results = get_search_results()
        results = []
        return render_template('home.html', title='Pogoda', form=form, results=results)  
        
    return render_template('home.html', title='Pogoda', form=form) 
 