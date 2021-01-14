# dependancies
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# local
from flaskproject.views.main import main
#from flaskproject.views.api import apis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uusaofy73cn487cn38047vb35849c7n34809ncv7389478xb78'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


app.register_blueprint(main)
# app.register_blueprint(apis)
