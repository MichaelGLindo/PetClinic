from fastapi import Depends, HTTPException
from jose import jwt

from app.auth_dependencies import oauth2_scheme
from app.security import SECRET_KEY, ALGORITHM


def require_role(role: str):

    def role_checker(token: str = Depends(oauth2_scheme)):

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            user_role = payload.get("rol")

            if user_role != role:
                raise HTTPException(
                    status_code=403,
                    detail="No autorizado"
                )

            return payload

        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

    return role_checker