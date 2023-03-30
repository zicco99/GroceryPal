import requests
from db_classes.classes_marsh_schemas import *
from db_classes.classes import *
import datetime
import re
import sys
import time
from flask import jsonify
from config import Config

from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine, func, inspect

sys.path.append("../")

#####################################################################################################################

# Global vars
metadata_obj = None
session = None


fridge_schema = FridgeSchema()

# Microservices and daemon threads functions

def composeRecipe(user_id):
    user_ingredients = session.query(Prod).filter(Recipe.title == title).first()



def InsertRecipe(title, category, ingredients, steps, image_url):
    try:
        # Check if recipe already exists
        existingRecipe = session.query(Recipe).filter(
            Recipe.title == title).first()
        if existingRecipe:
            return

        # Create new recipe object
        new_recipe = Recipe(title=title, category=category,
                            image_url=image_url)

        # Add recipe to session
        session.add(new_recipe)

        # Create and add recipe ingredients to session
        recipe_ingredients = []
        for ingredientName, quantityAndUnit in ingredients:
            match = re.search(r"^(\d+)\s*(g|gr|ml)", quantityAndUnit)
            if match:
                quant = int(match.group(1))
                unit = match.group(2)
            else:
                quant = -1
                unit = ""

            # Check if ingredient already exists
            existingIngr = session.query(Ingredient).filter_by(name=ingredientName).first()

            # If ingredient doesn't exist, create new ingredient object and add to session
            if not existingIngr:
                ingr = Ingredient(name=ingredientName, unit=unit)
                session.add(ingr)
            else:
                ingr = existingIngr

            # Create new recipe ingredient object and add to session
            recipe_ingr = RecipeIngredient(
                ingredient=ingr, recipe=new_recipe, amount=quant, amount_text=quantityAndUnit)

            session.add(recipe_ingr)
            recipe_ingredients.append(recipe_ingr)

            session.commit()

        # Create and add recipe steps to session
        recipe_steps = []
        for i, (url, exp) in enumerate(steps):
            new_step = Step(recipe=new_recipe, n_step=i,
                            image_url=url, explaining=exp)
            session.add(new_step)
            recipe_steps.append(new_step)

        # Commit all changes to session
        session.commit()

    except Exception as e:
        # Roll back changes to session if an error occurs
        session.rollback()
        print("An error occurred while adding recipe:", e)


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


def get_product(b):
    return session.query(Product).filter_by(barcode=b).first()

############################# Endpoints logic ########################################


# Recipe list will be updated by the recipe assemble microservice
def addFeedback(user_id,is_chosen,recipe_id):
    try:
        user = session.query(User).get(user_id)
        recipe = session.query(Recipe).get(recipe_id)
        if not user or not recipe:
            return None

        existingFeeback = session.query(Feedback).filter(
            Feedback.user_id == user_id,Feedback.recipe_id == recipe_id).first()
        if not existingFeeback:
            new_feeback = Feedback(user_id=user_id,recipe_id=recipe_id,is_chosen=is_chosen)
            session.add(new_feeback)
            session.commit()
            return 1

    except Exception as e:
        session.rollback()
        print(e)
        return None

def getRecipeList(user_id):
    # Create a list of serialized recipe dictionaries
    noFeedbackRecipes = session.query(Recipe).outerjoin(Feedback).filter(Feedback.id == None).all()

    recipe_list = []
    for recipe in noFeedbackRecipes:
        recipe_dict = RecipeSchema().dump(recipe)
        recipe_list.append(recipe_dict)
    
    # Return the list of recipe dictionaries in a JSON response
    return jsonify(recipe_list)

def getChosenRecipes(user_id):

    recipes = session.query(Recipe).join(Feedback).filter(Feedback.is_chosen == True,Feedback.user_id == user_id).all()

    recipe_list = []
    for recipe in recipes:
        recipe_dict = RecipeSchema().dump(recipe)
        recipe_list.append(recipe_dict)

    # Return the list of recipe dictionaries in a JSON response
    return jsonify(recipe_list)



def getProduct(barcode):
    
    # Check if product already exists
    existingProduct = session.query(Product).filter(
        Product.barcode == barcode).first()
    if existingProduct:
        return jsonify(ProductSchema().dump(existingProduct))
    
    #If it is not in DB -> retrieve info from OpenFood
    r = requests.get('https://it.openfoodfacts.org/api/v0/product/{}.json'.format(barcode))
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



def insert_db_if_misses(user):
    if not session.query(User).filter_by(id=user.id).first():
        session.add(user)
        session.commit()


def get_user(user_id):
    return session.query(User).filter_by(id=user_id).first()



##################################### Fridge management ################################################

def listFridges(user_id):
    user_fridges = session.query(UserFridge).filter(UserFridge.user_id == user_id).all()

    fridges_json = []
    for uf in user_fridges:
        fridge = session.query(Fridge).get(uf.fridge_id)
        fridges_json.append(fridge_schema.dump(fridge))

    # Return the list of recipe dictionaries in a JSON response
    return jsonify(fridges_json)

def newFridge(user_id,fridge_name):

    user = session.query(User).get(user_id)
    existing_fridge = session.query(Fridge).filter_by(name=fridge_name).first()

    if existing_fridge:
        raise ValueError(f"A fridge with the name '{fridge_name}' already exists.")

    new_fridge = Fridge(name=fridge_name)
    user.fridges.append(new_fridge)
    new_user_fridge = UserFridge(user_id=user.id, fridge_id=new_fridge.id, is_admin=True, is_owner=True)

    session.add(new_fridge)
    session.add(new_user_fridge)
    session.commit()
    
    serialized_fridge = fridge_schema.dump(new_fridge)
    return jsonify(serialized_fridge)


    
    
    



########################################################################################################


def bootstrap_db():
    global session
    global metadata

    # Establishing DB connection
    engine = create_engine(
        'postgresql://{}:{}@{}:{}/{}'.format(Config.USERNAME_ROLE, Config.PASSWORD_ROLE, Config.DB_IP, Config.PORT, Config.DB_NAME))
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Running options
    for arg in sys.argv:
        if (arg[0] == '-'):
            for op in arg[1:]:
                match op:
                    case 'n':  # Recreate database
                        print("Deleting old database....")

                        # Close all sessions and dispose engine
                        session.close_all()
                        engine.dispose()

                        # Drop all tables
                        Base.metadata.drop_all(bind=engine, checkfirst=True)

                        # Create all tables
                        Base.metadata.create_all(bind=engine)

                        inspector = inspect(engine)
                        required_tables = {'user', 'recipe', 'feedback', 'ingredient', 'product',
                                           'recipe_ingredient', 'step', 'fridge', 'user_fridge', 'fridge_product'}

                        while not required_tables.issubset(set(inspector.get_table_names())):
                            time.sleep(1)

                        print("Done,starting fetching....")
                        break
