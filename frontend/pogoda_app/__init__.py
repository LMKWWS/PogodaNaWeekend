from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cf96b87105c8acc995de975bd52ded12'

from pogoda_app import routes