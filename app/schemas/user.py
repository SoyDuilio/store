from pydantic import BaseModel, EmailStr

# Schema para mostrar la información de un usuario
class User(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    picture_url: str | None = None

    class Config:
        from_attributes = True # Permite crear el schema desde un objeto SQLAlchemy