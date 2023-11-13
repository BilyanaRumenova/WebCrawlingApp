from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

DATABASE_URL = "sqlite:///./screenshots.db"
engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autoflush=False, bind=engine))
Base = declarative_base()

Base.metadata.create_all(bind=engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(String, primary_key=True, index=True)
    start_url = Column(String)

