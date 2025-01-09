from flask import redirect, render_template, url_for, flash, request, session
from . import app
from .forms import CityForm
from backend.weather import get_forecast
from backend.bookings import get_accommodation_data, get_all_location_data
from datetime import datetime, timedelta, date


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = CityForm()
    if form.validate_on_submit():
        date_from = datetime.combine(date.today(), datetime.min.time())
        date_to = date_from + timedelta(days=6)

        weather_data = get_forecast(form.city.data, date_from, date_to)
        if weather_data["code"] != 200:
            session['error_code'] = weather_data['code']
            session['error_message'] = weather_data['error']['message']
            return redirect(url_for('error_page'))
        #results = []
        
        bookings_data = get_accommodation_data(weather_data['lat'], weather_data['lon'])
        if bookings_data["code"] != 200:
            session['error_code'] = bookings_data['code']
            if 'Message' in bookings_data:
                session['error_message'] = bookings_data['Message']  
            else: 
                session['error_message'] = bookings_data['error']['message']
            return redirect(url_for('error_page'))

        all_location_data = get_all_location_data(bookings_data)

        return render_template('home.html', title='Pogoda', form=form, weather_data=weather_data,
            bookings_data=all_location_data)

    return render_template('home.html', title='Pogoda', form=form, weather_data=[],
            bookings_data=[]) 

@app.route('/error', methods=['GET', 'POST'])
def error_page(): 
    form = CityForm()
    error_code = session.pop('error_code', 400)
    error_message = session.pop('error_message', 'Nieznany błąd')
    return render_template('error_page.html', title='Error', form=form,
                           api_errors=True,
                           error_code=error_code,
                           error_message=error_message) 
