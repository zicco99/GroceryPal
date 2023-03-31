from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,registry
from marshmallow import fields

from ..DBootstrap import custom_base

#################### Class and Schema definition ###############################


class FridgeProduct(custom_base):
    __tablename__ = 'fridge_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fridge_id = Column(Integer, ForeignKey('fridge.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)

    # Relationships
    fridge = relationship('Fridge', back_populates='fridge_products')
    product = relationship('Product', back_populates='used_in_fridge_product')


class FridgeProductSchema(SQLAlchemySchema):
    class Meta:
        model = FridgeProduct
        load_instance = True

    id = auto_field()
    fridge_id = auto_field()
    product_id = auto_field()
    quantity = auto_field()
    fridge = fields.Nested('FridgeSchema')
    product = fields.Nested('ProductSchema')


####################################################################################
