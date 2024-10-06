from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users", response_model=List[User])
def get_users():
    return users


@app.post("/user/{username}/{age}", response_model=User)
def create_user(
        username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20)],
        age: Annotated[int, Path(description="Enter age", ge=18, le=120)]
):
    new_id = len(users) + 1 if not users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}", response_model=User)
def update_user(
        user_id: Annotated[int, Path(description="Enter User ID", ge=1)],
        username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20)],
        age: Annotated[int, Path(description="Enter age", ge=18, le=120)]
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=User)
def delete_user(
        user_id: Annotated[int, Path(description="Enter User ID", ge=1)]
):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user

    raise HTTPException(status_code=404, detail="User was not found")