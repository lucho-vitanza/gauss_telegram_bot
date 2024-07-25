from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    institution = Column(String)
    audio_count = Column(Integer, default=0)

class Audio(Base):
    __tablename__ = 'audios'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    audio_id = Column(String, unique=True, nullable=False)
    study_number = Column(String)
    timestamp = Column(TIMESTAMP, server_default='now()')
