from os import path,mkdir,remove,rmdir,seteuid,environ
import sys
sys.path.append("../")
import threading
from giallozafferano_scraping.scraping import scrap

#Import configuration
from config import Config

#Modules used for database interaction + json 
from databaseDTO import *
from db_classes.classes import *
from db_classes.classes_marsh_schemas import *
import json

#Modules used for Flask + SSL configuration
from flask import Flask, render_template, request, redirect, send_file, send_from_directory, url_for, jsonify, abort
from flask_mobility import Mobility
import requests
from http import client
from flask_sslify import SSLify
from flask_cors import CORS

#Modules used for google login
from oauthlib.oauth2 import WebApplicationClient
from flask_login import LoginManager,current_user,login_required,login_user,logout_user,login_manager


###################################################################################################

# create the application 
app = Flask(__name__, static_folder='../frontend/dist/assets', template_folder='../frontend/dist')
app.add_url_rule('/static/<path:path>.css', 'css', lambda path: send_from_directory('static', path + '.css', mimetype='text/css'))
sslify = SSLify(app)
mobile = Mobility(app)

#Enable CORS
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})

app.secret_key = Config.APP_SECRET_KEY.encode('utf8')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_google'
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)


#Initialize schemas to serialize
product_schema = ProductSchema()
user_schema = UserSchema()

############################## ENDPOINTS ##########################################################

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check_login', methods=['GET'])
def check_login():
    if current_user.is_authenticated:
        return user_schema.dump(get_user(current_user.id)) | {'logged_in':True}
    else:
        return jsonify(logged_in=False)

@app.route('/login_google')
def login_google():
    # Find out what URL to hit for Google login
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        uri = authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route('/login_google/callback')
def google_callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

        # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(id=unique_id, name=users_name, email=users_email, profile_pic=picture)

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect("/#/home")



@app.route("/fake_login")
def fake_login():

    user = User(id=100000, name="vai mo", email="tina cipollari", profile_pic="www.goo")
    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    return redirect("/my_recipes")


@app.route("/recipes", methods=["GET"])
def recipes():
    user = User(id=100000,name="vai mo", email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    return getRecipeList(current_user.id)

@app.route("/chosen-recipes", methods=["GET"])
def chosen_recipes():
    
    user = User(id=100000,name="vai mo", email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    return getChosenRecipes(current_user.id)


@app.route("/add-recipe", methods=["POST"])
def add_feeback():

    user = User(id=100000,name="vai mo", email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)
    result = addFeedback(current_user.id, request.json["is_chosen"], request.json["recipe_id"])
    if result is None:
        abort(404)
    else:
        return jsonify(result)


@app.route("/product/<barcode>", methods=['GET', "POST"])
def product(barcode):

    if request.method == 'GET':
        return getProduct(barcode)
    
    if request.method == 'POST':
        old_info = getProduct(barcode)
        new_info = product_schema.load(request.form['product_json_updated'])

    

@app.route("/list-fridges", methods=['GET'])
def list_fridges():
    user = User(id=100000,name="vai mo", email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    if request.method == 'GET':
        return listFridges(user.id)

@app.route("/new-fridge", methods=['POST'])
def new_fridge():

    user = User(id=100000,name="vai mo", email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    if request.method == 'POST':
        return newFridge(user_id=user.id,fridge_name=request.json)






















@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.login_manager.user_loader
def load_user(_id):
    user = get_user(_id)
    if user:
      return user
    else:
      return None




































    

    """ @app.route('/product/<barcode>', methods=['GET',"POST"])
    def barcode(barcode):
        if request.method=='GET':
            getProd

        
        #it's a POST -> the user changed some infos -> update database
        else:

            #Decifrazione del payload (chiave simmetrica)


            #Data check, extract data (photos) as each attribute has this structure put in vote system enque
            for attr,value in prod.__dict__: #__dict__ give the list of attributes of the CLASS, instead of the instance (avoids huge dictionary payload attacks)
                if(attr!='_sa_instance_state'):
                    old_new = getattr(prod, attr)
                    old,new = old_new.split('@')

                    #Evaluate changes
                    
                    #Extract also photos here

                    #Add photo, generate links and set new links

                    #PHOTOS ARE SAVED dir (barcode) \ <n>photo.jpg

                    setattr(prod, attr ,new)

            update_product(prod)
            
    
    
    #If the image folder does not exits -> create it
    if not path.exists('images'): mkdir('images')

    #
    if path.exists('./images/{}.jpeg'.format(bcode)): remove('./images/{}.jpeg'.format(bcode))
    
    #Ottieni dal body i parametri
    img_file = request.form['image64']
    new_name = request.form['name']

    #Ottengo l'indice
    for prod in data:
        if(bcode==prod['barcode']):
            index=data.index(prod)
            break

    #GESTIONE FOTO

    #Distinguo il caso in cui l'utente ha modificato o no la foto
    if(img_file=='not_changed'):

        c=data[index]['counter_accepted_img']

        if(c<soglia_img):
            data[index]['counter_accepted_img']= c+1

    else:
        #Elimino la vecchia foto
        if path.exists('images/{}.jpeg'.format(bcode)): remove('./images/{}.jpeg'.format(bcode))

        #Decodifico la stringa e salvo la foto ottenuta
        with open('images/{}.jpeg'.format(bcode), "wb") as fh:
            fh.write(base64.b64decode(request.form['image64']))
        
        #Ottengo la nuova url
        new_img_url = 'http://23.94.219.145/images/{}.jpeg'.format(bcode)

        #Cambio il nome del prodotto e azzero il counter
        data[index]['img_prod'] = new_img_url
        data[index]['counter_accepted_img'] = 0
    
    #GESTIONE NOME

    #Distinguo il caso in cui l'utente ha modificato o no il nome
    if(new_name=='not_changed'):

        c=data[index]['counter_accepted_name']

        if(c<soglia_img):
            data[index]['counter_accepted_name']= c+1

    else:
        data[index]['prodotto'] = new_name
        data[index]['counter_accepted'] = 0

    #Backup
    with open('./db.json','wt') as json_file:
        json.dump(data,json_file)

    return '{}@{}'.format(data[index]['prodotto'],data[index]['img_prod']) """

# start the server with the 'run()' method
if __name__ == '__main__':

    # DB Bootstrap
    bootstrap_db()

    # Declare and start the scraping daemon thread
    t = threading.Thread(target=scrap)
    t.daemon = True
    t.start()

    # Declare and start the recipe composer daemon thread
    t = threading.Thread(target=scrap)
    t.daemon = True
    t.start()

    context = ('ssl_certificate/grocerypal.it.crt', 'ssl_certificate/grocerypal.it.key')
    #app.run(debug=True,port=4000,host='localhost',ssl_context=context)
    app.run(debug=True,port=4000,host='localhost')
