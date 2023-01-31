from flask import Flask, render_template, request, redirect, send_file
import requests
import json
from fuzzywuzzy import fuzz
from os import path,mkdir,remove,rmdir,seteuid,environ,setuid
import base64
import shutil

# create the application object
app = Flask(__name__)


@app.route('/barcode/<lang>/<bcode>', methods=['GET',"POST"])
def home(bcode,lang):

    seteuid(int(environ.get('SUDO_GID')))

    soglia_img = 10
    soglia_name = 10

    if request.method=='GET':
        #check if it is in local cache
        for x in data:
            if(bcode==x['barcode']):
                return x

        #o/w use api to get infos
        r = requests.get('https://it.openfoodfacts.org/api/v0/product/{}.json'.format(bcode))
        jsonino = r.json()
        print(r)

        try:
            p_barcode = jsonino['product']['_id']
        except KeyError:
            #make user know that product has no name for this product,so he can do a post inserting a custom
            p_barcode = bcode

        try:
            p_name = jsonino['product']['product_name_{}'.format(lang)]
        except KeyError:
            #make user know that product has no name for this product,so he can do a post inserting a custom
            p_name = "null"

        try:
            p_type = jsonino['product']['categories'][0]
        except KeyError:
            #make user know that product has no name for this product,so he can do a post inserting a custom
            p_type = "null"
            
        try:
            p_img = jsonino['product']['image_front_small_url']

        except KeyError:
            #make user know that product has no name for this product,so he can do a post inserting a custom
            p_img = "null"

        info = {
        'barcode' : bcode,
        'img_prod' : p_img,
        'prodotto' : p_name,
        'tipo': p_type,
        'counter_accepted_img':0,
        'counter_accepted_name':0
        }

        data.append(info)

        #Backup
        with open('./db.json','w') as json_file:
            json.dump(data,json_file)

        return json.dumps(info)

    else:
        #Se la cartella immagini non esiste creala
        if not path.exists('images'): mkdir('images')

        #Se esiste già una foto eliminala
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

        return '{}@{}'.format(data[index]['prodotto'],data[index]['img_prod'])

@app.route('/images/<bcode>.jpeg', methods=['GET'])
def send_image(bcode):
    #metodo semplice per mandare via protocollo http l'immagine
    return send_file('images/{}.jpeg'.format(bcode))

@app.route('/search/<prodotto>', methods=['GET'])
def redir(prodotto):
    #metodo semplice per eseguire una ricerca nei dati in cache
    result=[]
    for product in data:
        if fuzz.partial_ratio(product['prodotto'],prodotto)>80:
            result.append(product)
            
    return json.dumps(result)

# start the server with the 'run()' method
if __name__ == '__main__':

    """ remove("db.json")
    shutil.rmtree("images/") """

    #Tolgo i permessi di root
    seteuid(int(environ.get('SUDO_GID')))

    #load data
    if(path.exists("./db.json")):
        with open('./db.json','r') as json_file:
           data = json.load(json_file)
    else:
        data=[]

    #Rimetto i permessi di root
    setuid(0)

    app.run(debug=True,port=80,host='23.94.219.145')
