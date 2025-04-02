from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from os import path 
from flask_socketio import SocketIO

db = SQLAlchemy()
socketio = SocketIO()

def createapp():
    # initializing the app 
    app = Flask(__name__)
    app.config['SECRET_KEY']='hello'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)
    loginmanager = LoginManager(app)
    loginmanager.login_view = '/'
    socketio.init_app(app)

    # making the routes
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .models import Users
    createdatabase(app)

    @loginmanager.user_loader
    def userloader(id):
        return Users.query.filter_by(id = int(id)).first()
    
    # returning the app 
    return socketio, app

def createdatabase(app):
    if not path.exists("website/database.db"):
        with app.app_context():
            db.create_all()
        print('created')