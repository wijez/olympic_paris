from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, BackgroundTasks, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import MessageSchema, FastMail

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.templating import Jinja2Templates

from app.api.Depends.authorization import authenticate_user, create_access_token, get_current_active_user, \
    get_user
from app.core import settings, get_async_session
from app.crud import users_crud
from app.models.user_model import User
from app.schemas import Token
from app.schemas.auth_schema import PasswordResetRequest
from app.schemas.users_schema import UserCreate
from app.services import UsersService
from app.services.auth_service import AuthService
from app.utils import generate_verification_code
from app.utils.security import get_password_hash, generate_password_reset_token, verify_password_reset_token
from app.utils.send_verification_email import send_verification_email, send_password_reset_email

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

templates = Jinja2Templates(directory="templates")


@router.post("/verify")
async def verify_user(username: str, code: str, db: AsyncSession = Depends(get_async_session)):
    db_user = await get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.verify_code == code:
        db_user.is_active = True
        db_user.verify_code = None
        await db.commit()
        await db.refresh(db_user)
        return {"message": "Account successfully verified"}
    else:
        raise HTTPException(status_code=400, detail="Invalid verification code")


@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    db_user = await get_user(db, username=user.username)
    db_email = await users_crud.get(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    verify_code = generate_verification_code()
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        verify_code=verify_code
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    await send_verification_email(user.email, verify_code)
    return {"username": new_user.username}


@router.post("/token")
async def login_for_access_token(db: Annotated[AsyncSession, Depends(get_async_session)],
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login")
async def login_for_tokens(
        db: AsyncSession = Depends(get_async_session),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    # Authenticate the user
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = AuthService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = AuthService.create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/password-reset-request/")
async def password_reset_request(request: PasswordResetRequest,
                                 db: AsyncSession = Depends(get_async_session),
                                 ):
    user_service = UsersService(db)
    user = await user_service.get_user_by_email(email=request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = generate_password_reset_token(user.email)
    await send_password_reset_email(user.email, token)

    return {"msg": "Password reset email has been sent"}


@router.get("/reset-password/")
def render_reset_password_form(request: Request, token: str):
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return templates.TemplateResponse("reset_password.html", {"request": request, "token": token})


@router.post("/reset-password/")
async def reset_password(token: str = Form(...), new_password: str = Form(...),
                         db: AsyncSession = Depends(get_async_session)):
    users_service = UsersService(session=db)
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await users_service.get_user_by_email(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(new_password)
    await users_service.update_user_password(user=user, new_password=user.hashed_password)

    return {"msg": "Password has been reset successfully"}


@router.get("/me/")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]
