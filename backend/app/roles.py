from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.auth_dependencies import security
from app.security import SECRET_KEY, ALGORITHM


def require_role(role: str):

    def role_checker(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):

        token = credentials.credentials

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            print(payload)  # temporal para pruebas

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        user_role = payload.get("rol")

        print("ROL TOKEN:", user_role)
        print("ROL REQUERIDO:", role)

        if user_role != role:
            raise HTTPException(
                status_code=403,
                detail="No autorizado"
            )

        return payload

    return role_checker