from pydantic import BaseModel

class Image(BaseModel):
    id: int
    file_name: str
    s3_url: str # Usaremos s3_url aunque sea GCS para mantenerlo genérico

    class Config:
        from_attributes = True