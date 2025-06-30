from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

engine = create_engine(
    "sqlite:///senior_citizen.db",
    connect_args={"check_same_thread": False}
)
Base.metadata.bind = engine
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))
