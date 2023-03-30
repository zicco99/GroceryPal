from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from marshmallow import fields

Base = declarative_base()

#################### Class and Schema definition ###############################


class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    category = Column(String)
    image_url = Column(String)

    # Relationships
    feedback = relationship('Feedback', back_populates='recipe')
    users_who_feedback = relationship(
        'User', secondary='feedback', back_populates='feedbacked_recipes', lazy='dynamic', overlaps="feedback,user,recipe")
    steps = relationship('Step', back_populates='recipe')
    recipe_ingredients = relationship(
        'RecipeIngredient', back_populates='recipe')


class RecipeSchema(SQLAlchemySchema):
    class Meta:
        model = Recipe
        load_instance = True

    id = auto_field()
    title = auto_field()
    category = auto_field()
    image_url = auto_field()

    feedback = fields.Nested('FeedbackSchema', many=True,
                             exclude=('recipe', 'user'))
    users_who_feedback = fields.List(fields.Nested(
        'UserSchema', exclude=('feedbacked_recipes', 'fridges', 'feedback')))
    steps = fields.Nested('StepSchema', many=True, exclude=())
    recipe_ingredients = fields.Nested(
        'RecipeIngredientSchema', many=True, exclude=('ingredient',))


####################################################################################