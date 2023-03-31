from flask import Flask, redirect, render_template, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, login_required, logout_user
from flask_mobility import Mobility
from flask_sslify import SSLify
from influxdb_client import User
from oauthlib.oauth2 import WebApplicationClient

from config import Config
from database.bootstrapDB import bootstrap_db
from giallozafferano_scraping.scraping import scrap

import threading


def create_app(config_class, connection_string):

    app = Flask(__name__, static_folder='../frontend/dist/assets',
                template_folder='../frontend/dist')
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})

    # Set up SSL if config calls for it
    if app.config.get('SSL_REDIRECT', False):
        SSLify(app)

    # Set up mobile detection if config calls for it
    if app.config.get('USE_MOBILE_DETECT', False):
        Mobility(app)

    # Set up Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = 'login_google'

    # Set up OAuth2 client for Google
    WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

    # Register blueprints
    from controllers import (feedback_contr, fridge_contr, fridgeproduct_contr, ingredient_contr, login_contr,
                             product_contr, recipe_contr, recipeingredient_contr, step_contr, user_contr, userfridge_contr)

    app.register_blueprint(feedback_contr.bp, url_prefix='/api/feedbacks')
    app.register_blueprint(fridge_contr.bp, url_prefix='/api/fridges')
    app.register_blueprint(fridgeproduct_contr.bp, url_prefix='/api/fridgeproducts')
    app.register_blueprint(ingredient_contr.bp, url_prefix='/api/ingredients')
    app.register_blueprint(login_contr.bp, url_prefix='/api/login')
    app.register_blueprint(product_contr.bp, url_prefix='/api/products')
    app.register_blueprint(recipe_contr.bp, url_prefix='/api/recipes')
    app.register_blueprint(recipeingredient_contr.bp, url_prefix='/api/recipeingredient')
    app.register_blueprint(step_contr.bp, url_prefix='/api/steps')
    app.register_blueprint(user_contr.bp, url_prefix='/api/users')
    app.register_blueprint(userfridge_contr.bp, url_prefix='/api/userfridges')

    # Set up route for serving static CSS files
    @app.route('/static/<path:path>.css')
    def css(path):
        return send_from_directory('static', path + '.css', mimetype='text/css')

    # Set up route for serving index page
    @app.route('/')
    def index():
        return render_template('index.html')

    # Set up Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    session, metadata = bootstrap_db(connection_string)

    feedback_contr.session = session
    fridge_contr.session = session
    fridgeproduct_contr.session = session
    ingredient_contr.session = session
    login_contr.session = session
    recipe_contr.session = session
    user_contr.session = session

    # Start a background thread for web scraping
    threading.Thread(target=scrap, daemon=True).start()

    return app, session, metadata


if __name__ == '__main__':
    connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(
        Config.USERNAME_ROLE, Config.PASSWORD_ROLE, Config.DB_IP, Config.PORT, Config.DB_NAME)
    app, session, metadata = create_app(Config, connection_string)
    app.run(debug=True, port=4000, host='localhost')
    # app.run(debug=True,port=4000,host='localhost',ssl_context=context)
