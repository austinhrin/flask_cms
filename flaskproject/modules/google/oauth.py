from google.oauth2 import id_token
from google.auth.transport import requests


class oauth():
    def __init__(self, client_id):
        #
        self.CLIENT_ID = client_id

    def authenticate(self, token):
        # token is given as input from the frontend
        try:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), self.CLIENT_ID)

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            #user_id = id_info['sub']
        except ValueError:
            # Invalid token
            id_info = None
            pass
        return id_info
