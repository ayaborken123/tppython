from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Movies(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    director = Column(String, nullable=False)

    actors = relationship("Actors", back_populates="movie", cascade="all, delete-orphan")

class Actors(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True, index=True)
    actor_name = Column(String, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'))

    movie = relationship("Movies", back_populates="actors")
