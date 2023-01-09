from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=schemas.Token)
def get_token(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # create token and return it
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

