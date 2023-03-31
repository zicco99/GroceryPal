from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import time
import sys

# Global vars
# Each mapper should use the same Base instance that 
# you define once in your code. This is usually done by importing the 
# Base instance from a separate module or file, so that all the mappers use the same instance of Base.

#TOCURSE insomma porcamadonna, un'ora per capire che era un oggetto che deve essere passato ad ogni mapper affinchè raccolga
# i metadati dei mapper per generare lo schema del db, relazioni incluse...
custom_base = declarative_base()

from database.mappers.user import *
from database.mappers.ingredient import *
from database.mappers.product import *
from database.mappers.feedback import *  # Import Feedback before Recipe
from database.mappers.step import *
from database.mappers.recipe import *
from database.mappers.fridge import *
from database.mappers.fridgeproduct import *
from database.mappers.recipeingredient import *
from database.mappers.userfridge import *

def bootstrap_db(connection_string):

    # Establishing DB connection
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Running options
    for arg in sys.argv:
        if (arg[0] == '-'):
            for op in arg[1:]:
                match op:
                    case 'n':  # Recreate database
                        print("Deleting old database....")
                        
                        # Drop all tables
                        custom_base.metadata.drop_all(bind=engine)

                        # Recreate all tables
                        custom_base.metadata.create_all(bind=engine)

                        # Wait for all required tables to exist
                        Session = sessionmaker(bind=engine)
                        session = Session()

                        print("Done,starting fetching....")
                        break

    return session, metadata