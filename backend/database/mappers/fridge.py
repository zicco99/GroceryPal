from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,registry
from marshmallow import fields

from ..DBootstrap import custom_base
#################### Class and Schema definition ###############################

class Fridge(custom_base):
    __tablename__ = 'fridge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    # Relationships
    users = relationship('User', secondary='user_fridge',
                         back_populates='fridges')
    fridge_products = relationship('FridgeProduct', back_populates='fridge')


class FridgeSchema(SQLAlchemySchema):
    class Meta:
        model = Fridge
        load_instance = True

    id = auto_field()
    name = auto_field()

    users = fields.Nested('UserSchema', many=True)
    fridge_products = fields.Nested('FridgeProductSchema', many=True)


####################################################################################
