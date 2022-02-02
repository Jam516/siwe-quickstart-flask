#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import re
import requests
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort, session
from flask_cors import CORS
from flask_session import Session
from siwe.siwe import SiweMessage, generate_nonce, ValidationError, ExpiredMessage, MalformedSession, InvalidSignature
from web3 import Web3, HTTPProvider
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#----------------------------------------------------------------------------#
# CORS.
#----------------------------------------------------------------------------#

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/nonce')
def nonce():
    session['nonce'] = generate_nonce()
    return session['nonce']

@app.route('/verify', methods = ['POST'])
def verify():
    body = request.get_json()
    if body['message'] is None:
        return jsonify('Expected prepareMessage object as body.')
    # print(body['message'])

    siwe_message = SiweMessage(
                message={
                    re.sub(r"(?<!^)(?=[A-Z])", "_", k).lower(): v
                    for k, v in body['message'].items()
                }
            )

    # Validate signature
    w3 = Web3(HTTPProvider("https://mainnet.infura.io/v3/69bbfab4edd94ae0ae6a78d63f908d42"))
    try:
        siwe_message.validate(provider=w3)

        if (siwe_message.nonce != session['nonce']):
            return 'invalid nonce'

        session['siwe'] = siwe_message
        return 'Successful sign in'
    except ValidationError:
        session.pop('siwe', default=None)
        session.pop('nonce', default=None)
        print("Authentication attempt rejected due to invalid message.")
        return None
    except ExpiredMessage:
        session.pop('siwe', default=None)
        session.pop('nonce', default=None)
        print("Authentication attempt rejected due to expired message.")
        return None
    except MalformedSession as e:
        session.pop('siwe', default=None)
        session.pop('nonce', default=None)
        print(
            f"Authentication attempt rejected due to missing fields: {', '.join(e.missing_fields)}"
        )
        return None
    except InvalidSignature:
        session.pop('siwe', default=None)
        session.pop('nonce', default=None)
        print("Authentication attempt rejected due to invalid signature.")
        return None

@app.route('/personal_information')
def personal_information():
    if session['siwe'] is None:
        return 'You have to sign in first.'
        # return jsonify({'message': 'You have to sign in first.'})
    print('User authenticated')
    return jsonify('You are authenticated and your address is:' + session['siwe'].address)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
