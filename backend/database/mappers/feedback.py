from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,registry
from marshmallow import fields

from ..DBootstrap import custom_base

class Feedback(custom_base):
    __tablename__ = 'feedback'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    is_chosen = Column(Boolean)
    rating = Column(Integer)
    notes = Column(String)

    # Relationships
    user = relationship("User", back_populates='feedback',
                        overlaps="feedbacked_recipes")
    recipe = relationship('Recipe', back_populates='feedback',
                          overlaps="feedbacked_recipes")


class FeedbackSchema(SQLAlchemySchema):
    class Meta:
        model = Feedback
        load_instance = True

    id = auto_field()
    user_id = auto_field()
    recipe_id = auto_field()
    rating = auto_field()
    notes = auto_field()
    user = fields.Nested('UserSchema', exclude=('feedback',))
    recipe = fields.Nested('RecipeSchema', exclude=('feedback',))


