from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import datetime
import os

Base = declarative_base()

class Opportunity(Base):
    __tablename__ = 'opportunities'
    id = Column(Integer, primary_key=True)
    source = Column(String(50))
    category = Column(String(50))
    title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    link = Column(String(500), unique=True)
    description = Column(Text)
    posted_date = Column(DateTime)
    relevance_score = Column(Integer)
    summary = Column(Text)
    is_notified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db(db_url):
    if db_url.startswith("sqlite:///") and not db_url.endswith(":memory:"):
        db_path = db_url.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)

    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
