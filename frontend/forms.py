from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo

woj_choices = [
    ('ALL', ''),
    ('DS', 'dolnośląskie'), ('KP', 'kujawsko-pomorskie'),
    ('LU', 'lubelskie'), ('LB', 'lubuskie'),
    ('LD', 'łódzkie'), ('MA', 'małopolskie'),
    ('MZ', 'mazowieckie'), ('OP', 'opolskie'),
    ('PK', 'podkarpackie'), ('PD', 'podlaskie'),
    ('PM', 'pomorskie'), ('SL', 'śląskie'),
    ('SK', 'świętokrzyskie'), ('WN', 'warmińsko-mazurskie'),
    ('WP', 'wielkopolskie'), ('ZP', 'zachodniopomorskie')
]

class CityForm(FlaskForm):
    # city = StringField('Miasto', validators=[DataRequired()])
    city = StringField('Miasto')
    # voivodeship = SelectField(u'Województwo', choices=woj_choices)
    submit = SubmitField('Szukaj')