from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,registry
from ..DBootstrap import custom_base

#################### Class and Schema definition ###############################

class Step(custom_base):
    __tablename__ = 'step'
    id = Column(Integer, autoincrement=True, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    n_step = Column(Integer)
    image_url = Column(String)
    explaining = Column(String)

    # Relationships
    recipe = relationship('Recipe', back_populates='steps')


class StepSchema(SQLAlchemySchema):
    class Meta:
        model = Step
        load_instance = True

    id = auto_field()
    recipe_id = auto_field()
    n_step = auto_field()
    image_url = auto_field()
    explaining = auto_field()


####################################################################################

