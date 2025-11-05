from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "tu_clave_secreta_super_segura"  # ¡Pon una clave fuerte y mantenla secreta!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # El token expira en 60 minutos

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload    # aquí puedes obtener los datos del usuario
    except JWTError:
        return None