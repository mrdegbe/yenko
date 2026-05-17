from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.admin import Admin

from app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register-admin")
def register_admin(username: str, password: str, db: Session = Depends(get_db)):

    existing = db.query(Admin).filter(Admin.username == username).first()

    if existing:

        return {"message": "Admin already exists"}

    admin = Admin(username=username, password=hash_password(password))

    db.add(admin)

    db.commit()

    return {"message": "Admin created"}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    admin = db.query(Admin).filter(Admin.username == form_data.username).first()

    if not admin:

        return {"message": "Invalid credentials"}

    if not verify_password(form_data.password, admin.password):

        return {"message": "Invalid credentials"}

    token = create_access_token({"sub": admin.username})

    return {"access_token": token, "token_type": "bearer"}
