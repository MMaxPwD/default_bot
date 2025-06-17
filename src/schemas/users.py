from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str | None = None
    chat_id: int
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    location: str | None = None
    contact: str | None = None
    is_paid: bool | None = None


class UsersSchema(BaseModel):
    users: list[UserSchema]


class UserUpdateSchema(BaseModel):
    username: str | None = None
    chat_id: int | None = None
    user_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    location: str | None = None
    contact: str | None = None
    is_paid: bool | None = None
