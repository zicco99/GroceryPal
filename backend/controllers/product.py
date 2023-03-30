import sys
import requests
sys.path.append("../")
from database.bootstrapDB import *
from flask import Blueprint, jsonify, request

bp = Blueprint('product', __name__)


@bp.route("/product/<barcode>", methods=['GET', "POST"])
def product(barcode):

    if request.method == 'GET':
        return get_product(barcode)

    if request.method == 'POST':
        old_info = get_product(barcode)
        new_info = ProductSchema().load(request.form['product_json_updated'])


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

#Endpoints controller
product_schema = ProductSchema()

# Microservices and daemon threads functions


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


def get_product(barcode):

    # Check if product already exists
    existingProduct = session.query(Product).filter(
        Product.barcode == barcode).first()
    if existingProduct:
        return jsonify(ProductSchema().dump(existingProduct))

    #If it is not in DB -> retrieve info from OpenFood
    r = requests.get(
        'https://it.openfoodfacts.org/api/v0/product/{}.json'.format(barcode))
    info = r.json().get("product")

    #If does not exists on OpenFood -> return an empty product obj
    if (not info):
        p = Product(barcode=barcode, name="", brand="", big_image_url="", mini_image_url="",
                    quantity="", allergens="", eco_score="", nova_score="")
        return jsonify(ProductSchema.dump(p))
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

        insert_product(p)

        return jsonify(ProductSchema.dump(p))
