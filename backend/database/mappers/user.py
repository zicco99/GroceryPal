from flask_login import UserMixin
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry, relationship

from ..DBootstrap import custom_base


class User(custom_base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    profile_pic = Column(String)

    # Relationships
    feedback = relationship('Feedback', back_populates='user')
    feedbacked_recipes = relationship(
        'Recipe', secondary='feedback', back_populates='users_who_feedback', overlaps="feedback")
    fridges = relationship('Fridge', secondary='user_fridge',
                           back_populates='users', overlaps='user')


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    name = auto_field()
    email = auto_field()
    profile_pic = auto_field()

    feedback = fields.Nested('FeedbackSchema', many=True,
                             exclude=('user', 'recipe'))
    feedbacked_recipes = fields.List(fields.Nested('RecipeSchema', many=True, exclude=(
        'users_who_feedback', 'steps', 'recipe_ingredient', 'feedback')))
    fridges = fields.List(fields.Nested(
        'FridgeSchema', many=True, exclude=('users',)))


