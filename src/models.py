import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

         
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    followers = relationship("Follower", foreign_keys="[Follower.user_to_id]", back_populates="user_to")
    following = relationship("Follower", foreign_keys="[Follower.user_from_id]", back_populates="user_from")
    favorites = relationship("Favorites", back_populates="user") 

class Post(Base):
     __tablename__ = 'post'
     id = Column(Integer, primary_key=True)
     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

     user = relationship("User", back_populates="posts")
     comments = relationship("Comment", back_populates="post")
     favorited_by = relationship("Favorites", back_populates="post")
    

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)  

    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="followers")


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment_text = Column(Text, nullable=False)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def to_dict(self):
        return {}

class Favorites(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    user = relationship("User", back_populates="favorites")
    post = relationship("Post", back_populates="favorited_by")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
