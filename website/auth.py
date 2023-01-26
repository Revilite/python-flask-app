from flask import Blueprint as bp
from flask import render_template as rt
from flask import request as req
from flask import flash
from flask import redirect as red
from flask import url_for as url
from flask_login import login_user as liu
from flask_login import logout_user as lou
from flask_login import login_required as lir
from flask_login import current_user as cu
from . import db
from .models import User
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph


auth = bp("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if req.method == "POST":
        email = req.form.get("email")
        password = req.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if cph(user.password, password):
                flash("Logged in successfully!", category="success")
                liu(user, remember=True) #log in user
                return red(url("views.home"))

            else:
                flash("Incorrect Username or Password!", category="error")
        else:
            flash("Email does not exist!", category="error")

    return rt("login.html", user=cu)


@auth.route("/logout", methods=["GET", "POST"])
@lir #logged in required
def logout():
    lou() #log out user
    return red(url("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def signUp():
    if (req.method == 'POST'):

        email = req.form.get("email")
        username = req.form.get("username")
        password1 = req.form.get("password1")
        password2 = req.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already Exists.", category="error")
        elif len(email) < 4:
            flash("Email is too short!", category="error")
        elif len(username) < 2:
            flash("Username is too short!", category="error")
        elif password1 != password2:
            flash("Passwords do not match!", category="error")
        elif len(password1) < 4:
            flash("Password is too short!", category="error")

        else:
            new_user = User(email=email, username=username,
                            password=gph(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            liu(user)

            flash("Account created!", category="success")
            return red(url("views.home"))

    return rt("sign_up.html", user=cu)
