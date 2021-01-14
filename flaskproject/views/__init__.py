# dependancies
from flask import Blueprint

main = Blueprint("main", __name__, template_folder="templates")
apis = Blueprint("apis", __name__, template_folder="templates")

# local
from flaskproject.views.main import routes
from flaskproject.views.api import sign_in
