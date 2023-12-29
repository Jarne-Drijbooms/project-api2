from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Speler(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    naam = Column(String, index=True)
    achternaam = Column(String, index=True)
    leeftijd = Column(Integer, index=True)
    email = Column(String, unique=True, index=True)
    nationaliteit = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    enkelspel = relationship("Single", back_populates="enkel")
    dubbelspel = relationship("Dubble", back_populates="dubbel")


class Enkelspel(Base):
    __tablename__ = "single"

    id = Column(Integer, primary_key=True, index=True)
    hoogste_positie = Column(Integer, index=True)
    huidige_positie = Column(Integer, index=True)
    enkelspel_id = Column(Integer, ForeignKey("spelers.id"))

    enkel = relationship("player", back_populates="single")

class Dubbelspel(Base):
    __tablename__ = "dubble"

    id = Column(Integer, primary_key=True, index=True)
    hoogste_positie = Column(Integer, index=True)
    huidige_positie = Column(Integer, index=True)
    dubbelspel_id = Column(Integer, ForeignKey("spelers.id"))

    dubbel = relationship("player", back_populates="dubble")