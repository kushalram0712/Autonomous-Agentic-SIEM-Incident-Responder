from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

DATABASE_URL = "sqlite:///./siem_metrics.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True, index=True)
    metric_value = Column(Float)
    message = Column(String)
    vector = Column(String)
    timestamp = Column(Float, default=time.time)

class IncidentRecord(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(Float, default=time.time)
    message = Column(String)
    vector = Column(String)
    z_score = Column(Float)
    status = Column(String)
    action_taken = Column(String)
    agent_reasoning = Column(String)
    severity = Column(String)

# Initialize database tables
Base.metadata.create_all(bind=engine)