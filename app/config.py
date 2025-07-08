from fastapi.templating import Jinja2Templates

# Aquí definimos la configuración de las plantillas UNA SOLA VEZ.
# Esta es la única fuente de verdad para la ubicación de las plantillas.
templates = Jinja2Templates(directory="templates")