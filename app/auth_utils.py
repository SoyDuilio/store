from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from .database import get_db
from .models import user as user_model

def get_current_user(request: Request, db: Session = Depends(get_db)) -> user_model.User:
    """
    Obtiene el usuario actual desde la sesión, verifica que exista en la BD.
    Lanza un error 401 si el usuario no está autenticado.
    """
    user_info = request.session.get('user')
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(user_model.User).filter(user_model.User.email == user_info['email']).first()
    if user is None:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in database",
         )
    return user