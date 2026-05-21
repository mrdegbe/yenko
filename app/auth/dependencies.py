from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.admin import Admin
from app.auth.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_admin(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    payload = decode_access_token(token)

    if not payload:

        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")

    admin = db.query(Admin).filter(Admin.username == username).first()

    if not admin:

        raise HTTPException(status_code=401, detail="Admin not found")

    return admin
