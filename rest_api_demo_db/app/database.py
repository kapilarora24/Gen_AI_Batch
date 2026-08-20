from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

DATABASE_URL = "postgresql://postgres:Pass%40123@localhost:5432/localhost:8000"

# engine = create_engine(DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


with engine.connect() as conn:
    print("Connected successfully!")
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())
