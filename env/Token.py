from pydantic import BaseModel
import jwt

SECRET_KEY = 'your-secret-key'  # Reemplaza esto con tu propia clave secreta


class UsuarioBase(BaseModel):
    nombre: str
    id: int

def verify_token(token) -> UsuarioBase:
    try:
        # Intenta decodificar el token con la clave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return UsuarioBase(nombre=payload["nombre"], id=payload['id'])
    except jwt.ExpiredSignatureError:
        # El token ha expirado
        return 
    except jwt.InvalidTokenError:
        # El token es inválido
        return 
