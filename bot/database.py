from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

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

def init_db():
    Base.metadata.create_all(engine)

