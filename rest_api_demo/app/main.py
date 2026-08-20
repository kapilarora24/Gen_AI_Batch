from fastapi import FastAPI

# from app.database import Base, engine
# from app.models import User
from app.routes.users_routes import router as users_router

# Base.metadata.create_all(bind=engine)

# localhost:8000/
app = FastAPI()


# localhost:8000
@app.get("/")
def read_root():
    return {"Hello": "World"}


# localhost:8000/about
@app.get("/about")
def about_root():
    return {"Welcome to about page"}


# localhost:8000/contact
@app.get("/contact")
def contact_root():
    return {"Welcome to contact page"}


app.include_router(users_router)
