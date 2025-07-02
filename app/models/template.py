from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

# No olvides añadir 'DateTime' y 'func' a tus importaciones de sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String, unique=True, nullable=False) # ej: "page_4_cards.html"
    description = Column(String)
    best_for_content_type = Column(String, index=True) # ej: "TESTIMONIAL", "BENEFIT_LIST"
    tags = Column(JSON) # ej: ["tarjetas", "4-elementos"]

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())