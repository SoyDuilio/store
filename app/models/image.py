from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

# No olvides añadir 'DateTime' y 'func' a tus importaciones de sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    s3_url = Column(String, nullable=False) # Mantenemos el nombre genérico
    user_id = Column(Integer, ForeignKey("users.id"))

    # ... otros campos ...
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # No solemos actualizar imágenes, pero onupdate no hace daño
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # La relación se llama 'owner' y se conecta con la propiedad 'images' en el modelo User
    owner = relationship("User", back_populates="images")