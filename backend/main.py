from flask_login import LoginManager, current_user, login_required, login_user, logout_user, login_manager
from oauthlib.oauth2 import WebApplicationClient
from flask_cors import CORS
from flask_sslify import SSLify
from flask_mobility import Mobility
from flask import Flask, render_template, send_from_directory
from database.bootstrapDB import *
from config import Config
from giallozafferano_scraping.scraping import scrap
import threading
import sys

# Import configuration

# Modules used for database interaction + json

# Modules used for Flask + SSL configuration

# Import controllers
sys.path.append("../")
from database.bootstrapDB import *
from controllers import login,fridge,product,recipe,user,feedback

###################################################################################################

# create the application
app = Flask(__name__, static_folder='../frontend/dist/assets',
            template_folder='../frontend/dist')
app.add_url_rule('/static/<path:path>.css', 'css',
                 lambda path: send_from_directory('static', path + '.css', mimetype='text/css'))
sslify = SSLify(app)
mobile = Mobility(app)

# Enable CORS
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})

app.secret_key = Config.APP_SECRET_KEY.encode('utf8')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_google'
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)


app.register_blueprint(login.bp, url_prefix='/api')
app.register_blueprint(fridge.bp, url_prefix='/api')
app.register_blueprint(product.bp, url_prefix='/api')
app.register_blueprint(recipe.bp, url_prefix='/api')




@app.route('/')
def home():
    return render_template('index.html')


@app.login_manager.user_loader
def load_user(_id):
    user = user.get_user(_id)
    if user:
        return user
    else:
        return None

if __name__ == '__main__':

    # DB Bootstrap
    bootstrap_db()

    # Declare and start the scraping daemon thread
    t = threading.Thread(target=scrap)
    t.daemon = True
    t.start()

    context = ('ssl_certificate/grocerypal.it.crt','ssl_certificate/grocerypal.it.key')
    
    # app.run(debug=True,port=4000,host='localhost',ssl_context=context)
    app.run(debug=True, port=4000, host='localhost')
