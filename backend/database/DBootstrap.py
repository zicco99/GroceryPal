from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import time
import sys

# Each mapper should use the same Base instance. This is usually done by importing the 
# Base instance from a separate module or file, so that all the mappers use the same instance of Base.

#TOCURSE insomma porcamadonna, un'ora per capire che era un oggetto che deve essere passato ad ogni mapper affinchè raccolga
#i metadati dei mapper per generare lo schema del db, relazioni incluse...
custom_base = declarative_base()

from database.mappers.user import *
from database.mappers.ingredient import *
from database.mappers.product import *
from database.mappers.feedback import * 
from database.mappers.step import *
from database.mappers.recipe import *
from database.mappers.fridge import *
from database.mappers.fridgeproduct import *
from database.mappers.recipeingredient import *
from database.mappers.userfridge import *

def bootstrap_db(connection_string,is_debug_db):

    # Establishing DB connection
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Running options
    if (is_debug_db): recreate_db(engine)
    
    else:
        for arg in sys.argv:
            if (arg[0] == '-'):
                for op in arg[1:]:
                    match op:
                        case 'n':  # Recreate database
                            recreate_db(engine)
                            break

    return session, metadata, engine 

def recreate_db(engine):

    print("Deleting old database....")

    # Drop all tables
    custom_base.metadata.drop_all(bind=engine)

    # Recreate all tables
    custom_base.metadata.create_all(bind=engine)

    required_tables = ['ingredient', 'product', 'user', 'feedback', 'recipe',
                        'step', 'user_fridge', 'fridge', 'fridge_product', 'recipe_ingredient']

    while True:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        if all(table in existing_tables for table in required_tables):
            break
        # Wait for 1 second before checking again
        time.sleep(1)

    print("Done,starting fetching....")

