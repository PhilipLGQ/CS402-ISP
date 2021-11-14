from flask import Flask, request, make_response
import time  # For timestamp
import hmac  # Standard HMAC lib
from hashlib import sha1  # Hashing library provided to HMAC
import base64  # Base64 encoding/decoding

# Define the secret key
SECRET_KEY = 'whisky'.encode()


# Function for creating cookies with HMAC
def create_cookies(username, password):
    # basic cookie info
    timestamp = str(int(time.time()))  # save only integer part into string
    domain = 'com402'
    hw = 'hw2'
    ex = 'ex2'

    # judge login's role by username and password
    if username == 'admin' and password == '42':
        role = 'admin'
    else:
        role = 'user'

    # create cookie without HMAC, later hashed and appended by HMAC
    cookie = ','.join([username, timestamp, domain, hw, ex, role])

    # compute its HMAC by secret key
    HMAC = hmac.new(SECRET_KEY, cookie.encode(), digestmod=sha1)

    # get final cookie appended with HMAC and do base64 encoding
    cookie_HMAC = cookie + ',' + HMAC.hexdigest()
    cookie_HMAC_base64 = base64.b64encode(cookie_HMAC.encode())

    return cookie_HMAC_base64.decode('utf-8')

# Function for validating if the cookie is legit in user authentication
def validate_cookies(cookie):
    # tampered cookie may not even be a base64 one
    try:
        cookie_decoded = base64.b64decode(cookie.encode()).decode('utf-8')
    except:
        return False

    base_cookie, HMAC = cookie_decoded.rsplit(',', 1)

    # check if the HMAC are still the same
    expected_HMAC = hmac.new(SECRET_KEY, base_cookie.encode(), digestmod=sha1).hexdigest()
    return expected_HMAC == HMAC


app = Flask(__name__)

cookie_name = "LoginCookie"


@app.route("/login",methods=['POST'])
def login():
    # get username and password from payload
    username = request.form.get('username')
    password = request.form.get('password')

    # do a simple sanity check
    if not (username and password):
        return 'Invalid login info!', 401

    # create cookie with HMAC
    cookie = create_cookies(username, password)

    # set the cookie with correct cookie name, return response
    response = make_response('login')
    response.set_cookie(cookie_name, cookie)

    return response


@app.route("/auth",methods=['GET'])
def auth():
    cookie_saved = request.cookies.get(cookie_name)

    # check if the cookie exists or has been tampered
    if cookie_saved is None or validate_cookies(cookie_saved) is False:
        return 'Cookie not found or has been tampered', 403

    # decode it if passed
    cookie_saved_decoded = base64.b64decode(cookie_saved.encode()).decode('utf-8')

    # Check the role included in the cookie
    cookie_role = cookie_saved_decoded.split(',')[5]
    if cookie_role == 'admin':
        return 'You are admin!', 200
    else:
        return 'You are user!', 201


if __name__ == '__main__':
    app.run()
