from flask import Flask
from flask_sqlalchemy import  SQLAlchemy as sql
from os import path
from flask_login import LoginManager

db = sql()
DB_NAME = "database.db"

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'the end is never the end si enver the end'
  app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
  db.init_app(app)



  #import routes
  from .views import views
  from .auth import auth

  #assigns routes on websites
  app.register_blueprint(views, url_prefix="/")
  app.register_blueprint(auth, url_prefix="/")

  from .models import User, Note

  with app.app_context():
        db.create_all()
        print("Database created")

  lim = LoginManager()
  lim.login_view = "auth.login"
  lim.init_app(app)

  @lim.user_loader
  def load_user(id):
    return User.query.get(int(id))


  return app

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')