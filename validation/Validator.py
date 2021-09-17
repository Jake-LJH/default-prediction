from flask import Flask,jsonify, render_template, request,g,redirect
from config.Settings import Settings
import functools
import jwt
import re


def login_required(func):
    @functools.wraps(func)
    def secure_login(*args, **kwargs):
        
        auth = True
        token = request.cookies.get("jwt")
        print(token)
       
        if token == None:
            auth = False
        
        if token:
            try:
                payload = jwt.decode(token,Settings.secretKey,"HS256")
                g.username = payload['username']
                g.userid = payload['userid']
            except jwt.exceptions.InvalidSignatureError as err:
                print(err)
                auth = False

        if auth == False:

            return redirect("login.html")

        return func(*args, **kwargs)
    return secure_login

def validateRegister(func):
    @functools.wraps(func)
    def validate(*args, **kwargs):
        pw = request.form['password']
        password = request.form['cfmPassword']
        email = request.form['email']
        username = request.form['username']
        pattern = re.compile('^[a-zA-Z0-9]{8,}$')
        error = None

        if (pw == password and pattern.match(password)):

            print('Input Match')
            return func(*args, **kwargs)

        elif pw != password:
            error = "Password not Match!"
            return render_template("registration.html", error = error)
        else:
            error = "Password has to be at least 8 characters"
            print('Input Not Match')
            return render_template("registration.html", error = error)

    return validate


