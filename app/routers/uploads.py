import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from google.cloud import storage
from dotenv import load_dotenv

# Importaciones de tu proyecto
from ..database import get_db
from ..models import user as user_model
from ..models import image as image_model
from ..schemas import image as image_schema # Asegúrate de tener este schema
from ..auth_utils import get_current_user

load_dotenv()
router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)

# --- Configuración del Cliente de Storage ---
storage_client = storage.Client()
bucket_name = os.getenv("GCS_BUCKET_NAME")
# --- Fin de la Configuración ---


# --- Endpoints ---

@router.post("/image", response_model=image_schema.Image, status_code=201)
async def upload_image(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    if not bucket_name:
        raise HTTPException(status_code=500, detail="GCS_BUCKET_NAME no está configurado en el servidor.")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El formato del archivo no es válido. Solo se permiten imágenes.")

    try:
        bucket = storage_client.bucket(bucket_name)
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        blob_path = f"users/{current_user.id}/{unique_filename}"
        
        blob = bucket.blob(blob_path)
        
        blob.upload_from_file(file.file, content_type=file.content_type)

        blob.make_public()  
        
        # CONSTRUIMOS LA URL MANUALMENTE - ¡ESTO ESTÁ BIEN!
        public_url = f"https://storage.googleapis.com/{bucket_name}/{blob_path}"

        new_image = image_model.Image(
            file_name=file.filename,
            s3_url=public_url,
            user_id=current_user.id
        )
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return new_image

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor al subir el archivo: {str(e)}")


@router.get("/my-images", response_model=list[image_schema.Image])
async def get_my_images(
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """
    Devuelve una lista de todas las imágenes que pertenecen al usuario logueado.
    """
    images = db.query(image_model.Image).filter(image_model.Image.user_id == current_user.id).order_by(image_model.Image.id.desc()).all()
    return images