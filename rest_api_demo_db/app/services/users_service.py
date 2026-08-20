def get_all_users():
    # connect to db and excute query mutation
    return [
        {
            "id": "1",
            "email": "a@1.com",
            "name": "Steve",
            "phonenumber": "12345",
        },
        {
            "id": "2",
            "email": "a@1.com",
            "name": "John",
            "phonenumber": "67890",
        },
    ]


# def create_user(user):
#     # connect to db and excute query mutation
#     return {
#         # "user": user,
#         "id": 3,
#         # "name": user.name,
#         # "email": user.phone,
#         # "phone": user.phone,
#         **user.model_dump(),
#         "message": "successfully created",
#     }


# def fetch_user_by_id(user_id):
#     print(user_id)
#     # connect to db and excute query mutation
#     return {
#         "user_id": user_id,
#         "name": "Kapil",
#         "phonenumber": "99999",
#     }


# def update_user_by_id(user_id, user):
#     print("New From Data :")
#     print(user)
#     # connect to db and excute query mutation
#     return {
#         "id": user_id,
#         "email": user.email,
#         "name": user.name,
#         "phonenumber": user.phonenumber,
#         "message": "successfully posted",
#     }


# def update_user_partial(user_id, user):
#     print("Updated data:")
#     print(user)
#     return {
#         "id": user_id,
#         "updated_data": user.model_dump(exclude_unset=True),
#         # "email": user.email,
#         # "name": user.name,
#         # "phonenumber": user.phonenumber,
#         "message": "successfully updated",
#     }


# def delete_user(user_id, user):
#     print("Deleted user:")
#     print(user)
#     return {
#         "id": user_id,
#         # "Deleted_data": user.model_dump(exclude_unset=True),
#         "email": user.email,
#         "name": user.name,
#         "phonenumber": user.phonenumber,
#         "message": "successfully deleted",
#     }
