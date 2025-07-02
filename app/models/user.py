from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

# No olvides añadir 'DateTime' y 'func' a tus importaciones de sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    google_id = Column(String, unique=True, index=True)
    full_name = Column(String)
    picture_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # La relación se llama 'images' y se conecta con la propiedad 'owner' en el modelo Image
    images = relationship("Image", back_populates="owner")