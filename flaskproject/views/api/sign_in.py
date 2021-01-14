from flaskproject.views import apis
from flaskproject.modules.google.oauth import oauth
from secrets import secrets

from flask import request, session, jsonify


@apis.route("/api/google/authenticate", methods=["POST"])
def authenticate():
    result = request.form.to_dict()
    token = result["token"]

    if token == "undefined" or token == "":
        return jsonify({"error": "token is undefined"})

    google = oauth(secrets.google.client)
    auth_info = google.authenticate(token)
    if auth_info != None:
        # user is authenticated

        # create flask session for user
        session["user_id"] = auth_info["sub"]
        session["email"] = auth_info["email"]
        session["name"] = auth_info["name"]
        session["given_name"] = auth_info["given_name"]
        session["family_name"] = auth_info["family_name"]
        session["picture"] = auth_info["picture"]
        session["locale"] = auth_info["locale"]

        # add user to database or update user in database.

        return jsonify({"sucess": "user is authenticated"})
    else:
        return jsonify({"error": "user could not be authenticated"})
