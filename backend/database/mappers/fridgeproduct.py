from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry, relationship

from ..DBootstrap import custom_base



class FridgeProduct(custom_base):
    __tablename__ = 'fridge_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fridge_id = Column(Integer, ForeignKey('fridge.id'))
    product_barcode = Column(Integer, ForeignKey('product.barcode'))
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
    product_barcode = auto_field()
    quantity = auto_field()
    fridge = fields.Nested('FridgeSchema')
    product = fields.Nested('ProductSchema')


