from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,registry
from marshmallow import fields

from ..DBootstrap import custom_base
#################### Class and Schema definition ###############################


class UserFridge(custom_base):
    __tablename__ = 'user_fridge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    fridge_id = Column(Integer, ForeignKey('fridge.id'))
    is_admin = Column(Boolean)
    is_owner = Column(Boolean)


class UserFridgeSchema(SQLAlchemySchema):
    class Meta:
        model = UserFridge
        load_instance = True

    id = auto_field()
    user_id = auto_field()
    fridge_id = auto_field()
    is_admin = auto_field()
    is_owner = auto_field()


####################################################################################

