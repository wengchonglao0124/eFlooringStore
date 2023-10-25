from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
  app = Flask(__name__)
  app.debug = True

  app.secret_key = 'IFN557_Assignment2_WengChong_Lao_&_Zhiyun_Pan'

  #set the app configuration data 
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eFlooringStore.sqlite'

  # initialise db with flask app - necessary because scope of app
  # is only here in create_app, but db is defined globally
  db.init_app(app)

  Bootstrap4(app)
  
  #importing modules here to avoid circular references, register blueprints of routes
  from . import views
  app.register_blueprint(views.bp)

  # Load the data into database
  '''
  from . import admin
  app.register_blueprint(admin.admin_bp)
  '''

  @app.errorhandler(404) 
  # Inbuilt function (to Flask) which takes error as parameter
  def not_found(e): 
    return render_template('error.html', error=e)


  # Handles server errors (look-up 'HTTP response status codes')
  @app.errorhandler(500)
  def internal_error(e):
    return render_template('error.html', error=e)   
 
  
  return app
