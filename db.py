from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base       #This is used to define the base class for all your ORM models (like Message).            
from sqlalchemy.orm import sessionmaker                        #Creates database sessions — required to interact with the database
from datetime import datetime
import uuid                                                   # To generate a unique session ID using UUIDs.
from sqlalchemy.sql import func

Base = declarative_base()                                    # Base is the base class from which all models will inherit.


class Message(Base):                                         #Any class that inherits from Base is treated as a database table.
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    session_id = Column(String, default=lambda: str(uuid.uuid4()))
    role = Column(String)  # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=func.now())

engine = create_engine("sqlite:///chat_history.db")                         # Connects to a local SQLite database named chat_history.db ,If the file doesn’t exist, it gets created.
Base.metadata.create_all(bind=engine)                                       #Creates the messages table in the database if it doesn't already exist.


#SessionLocal() creates a new database session when called.
#autocommit=False: You have to manually call commit().
#autoflush=False: Delays writing until you explicitly flush/commit.
#bind=engine: Uses the database engine created above.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_message(session_id, role, content):
    db = SessionLocal()
    msg = Message(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.close()

def get_messages(session_id):
    db = SessionLocal()
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()
    db.close()
    return messages

def clear_messages(session_id):
    db = SessionLocal()
    db.query(Message).filter(Message.session_id == session_id).delete()
    db.commit()
    db.close()
