from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from config import Config
import time
import sys

# Import models
from database.models.userfridge import *
from database.models.user import *
from database.models.step import *
from database.models.recipeingredient import *
from database.models.product import *
from database.models.ingredient import *
from database.models.fridgeproduct import *
from database.models.recipe import *
from database.models.feedback import *
from database.models.fridge import *

# Global vars
Base = declarative_base()


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
