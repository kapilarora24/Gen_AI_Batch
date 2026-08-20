from app.main import User, app


@app.post("/api/v1/users")
def add_user(user: User):
    print(user)
    return {
        "user": user,
        "message": "Successflly posted user.",
    }
