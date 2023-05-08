import sys
from marshmallow import ValidationError
from psycopg2 import IntegrityError
import requests
from sqlalchemy import Engine
sys.path.append("../")
from database.DBootstrap import *
from flask import Blueprint, jsonify, request
from config import Config

bp = Blueprint('product', __name__)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

engine = None

# CRUD endpoints

#get
@bp.route("/<int:barcode>", methods=["GET"])
def get_product(barcode):
    Session = sessionmaker(bind=engine)
    session = Session()
    product = session.query(Product).filter(Product.barcode == barcode).first()
    if not product:
        openfood_product = get_by_openfood(barcode)
        if not openfood_product:
            return product_schema.dump(Product(barcode)), 404
        else:
            return product_schema.dump(openfood_product), 200

    return product_schema.dump(product), 200

#create
@bp.route("/<int:barcode>", methods = ["POST"])
def create_product(barcode):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        product = product_schema.load(request.json, session=session)
    except (ValidationError,ValueError) as err:
        print(str(err))
        return jsonify({"error": str(err)}), 400

    if session.query(Product).filter(Product.barcode == barcode).first():
        return jsonify({"error": "Product already exists"}), 409

    session.add(product)
    session.commit()

    return jsonify(request.json), 201
    
#update


@bp.route("/<int:barcode>", methods=["PUT"])
def update_product(barcode):
    global session
    try:
        product = product_schema.load(request.json, session=session)
    except ValidationError as err:
        print(str(err))
        return jsonify({"error": str(err)}), 400

    existing_product = session.query(Product).get(barcode)
    if not existing_product:
        return None, 404

    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.brand = product.brand
    existing_product.category = product.category
    existing_product.weight = product.weight
    existing_product.image_url = product.image_url

    session.commit()
    return jsonify(product_schema.dump(existing_product)), 204



#delete
@bp.route("/<int:barcode>", methods=["DELETE"])
def delete_product(barcode):
    global session
    product = product_schema.load(request.json, session=session)
    existing_product = session.query(Product).get(barcode)
    if not existing_product:
        return None, 404

    session.delete(existing_product)
    session.commit()
    return jsonify(product_schema.dump(existing_product)), 204



""" 
    @app.route('/product/<barcode>', methods=['GET',"POST"])
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


def insert_product(p):
    try:
        session.add(p)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


def update_product(p):
    try:
        # Obtain reference and update
        session.query(Product).filter_by(barecode=p.barecode).first().update(p)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


""" def create_product():
    # Get data from the request body
    data = request.get_json()

    # Load data into the Product schema
    try:
        product = product_schema.load(data, session=db.session)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Add the new Product to the database
    db.session.add(product)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A product with that barcode already exists."}), 400

    # Return the created Product object in the response
    return product_schema.jsonify(product), 201


def get_product(id):
    # Find the Product object with the given id
    product = Product.query.get(id)

    # If the Product doesn't exist, return a 404 error
    if not product:
        return jsonify({"error": "Product not found."}), 404

    # Return the Product object in the response
    return product_schema.jsonify(product)


def update_product(id):
    # Find the Product object with the given id
    product = Product.query.get(id)

    # If the Product doesn't exist, return a 404 error
    if not product:
        return jsonify({"error": "Product not found."}), 404

    # Get data from the request body
    data = request.get_json()

    # Load data into the Product schema
    try:
        product = product_schema.load(
            data, instance=product, session=db.session)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Update the Product in the database
    db.session.add(product)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A product with that barcode already exists."}), 400

    # Return the updated Product object in the response
    return product_schema.jsonify(product)


def delete_product(id):
    # Find the Product object with the given id
    product = Product.query.get(id)

    # If the Product doesn't exist, return a 404 error
    if not product:
        return jsonify({"error": "Product not found."}), 404

    # Delete the Product from the database
    db.session.delete(product)
    db.session.commit()

    # Return a success message in the response
    return jsonify({"message": "Product successfully deleted."}) """


# Auxiliary functions 

def get_by_openfood(barcode):
    r = requests.get('https://it.openfoodfacts.org/api/v0/product/{}.json'.format(barcode))
    info = r.json().get("product")

    #If does not exists on OpenFood -> return an empty product obj
    if (not info):
        return None
    
    else:
        #Basic info
        name = info.get("product_name")
        brand = info.get("brands")
        big = info.get("image_front_small_url")
        mini = info.get("image_front_url")
        quantity = info.get("product_quantity")

        #Additional info
        allergens = []
        for all in info.get("allergens").split(","):
            allergens.append(all)

        eco_score = None
        if (info.get("ecoscore_extended_data")):
            eco_score = info["ecoscore_extended_data"].get(
                "ecoscore_grade")

        nova_score = info.get("nova_group")

        p = Product(barcode=barcode, name=name, brand=brand, big_image_url=big, mini_image_url=mini,
                    quantity=quantity, allergens=allergens, eco_score=eco_score, nova_score=nova_score)

        return p
