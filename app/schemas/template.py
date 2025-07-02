from pydantic import BaseModel

class Template(BaseModel):
    id: int
    template_name: str
    description: str | None = None

    class Config:
        from_attributes = True