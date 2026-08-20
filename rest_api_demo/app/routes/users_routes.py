from pydantic import BaseModel
from fastapi import APIRouter
# from app.database import SessionLocal
# from app.models import User as UserModel
from app.services.users_service import get_all_users

#     create_user,
#     fetch_user_by_id,
#     update_user_by_id,
#     update_user_partial,
#     delete_user,
# )


class User(BaseModel):
    name: str = None
    email: str = None
    phonenumber: str = None


router = APIRouter(prefix="/api/v1/users")


# localhost:8000/api/v1/users/- Get
@router.get("/")
def get_users():
    # db = SessionLocal()
    # try:
    #     users = db.query(UserModel).all()
    return get_all_users()


# finally:
#     db.close()


# # localhost:8000/api/v1/users/- Post - add user
# @router.post("/")
# def add_users(user: User):  # capturing the firm data
#     print(user)
#     return create_user(user)


# # localhost:8000/api/v1/users/{user_id}- List
# @router.get("/{user_id}")
# def fetch_user_by_id(user_id):
#     print("Requested user id:" + user_id)
#     return fetch_user_by_id(user_id)


# # localhost:8000/api/v1/users/{user_id}- PUT
# @router.put("/{user_id}")
# def update_user(user_id: str, user: User):
#     print("Requested user id:" + user_id)
#     return update_user_by_id(user_id, user)


# # localhost:8000/api/v1/users/{user_id}- Patch
# @router.patch("/{user_id}")
# def patch_user_partial(user_id: str, user: User):
#     print("Requested user id:" + user_id)
#     return update_user_partial(user_id, user)


# # localhost:8000/api/v1/users/{user_id}- Delete
# @router.delete("/{user_id}")
# def Delete_user_by_id(user_id: str, user: User):
#     print("Requested user id:" + user_id)
#     return delete_user(user_id, user)
