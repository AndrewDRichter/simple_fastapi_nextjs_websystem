from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from my_api.core.database import get_session
from my_api.core.security import authenticate_user, create_access_token, get_current_user
from my_api.schemas.auth import LoginRequest, Token

from my_api.models.users import User

router = APIRouter()


@router.post(
    '/token',
    # response_model=
    status_code=status.HTTP_200_OK,
    summary='Generate access token',
)
async def token(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(login_data.email, login_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect login',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                'code': 'inactive_account',
                'message': 'You have to reactivate your account before proceeding',
                'activation_url': f'/api/v1/auth/activate',
            }
        )

    access_token = create_access_token(data={'sub': str(user.id)})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }

@router.post(
    '/refresh_token',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary='Refresh access token'
)
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    access_token = create_access_token(data={'sub': str(current_user.id)})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }

@router.post(
    path='/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Reactivate user account',
)
async def activate_user(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(email=login_data.email, password=login_data.password, db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad credentials',
        )

    if not user.is_active:
        user.is_active = True
        await db.commit()
        await db.refresh(user)

    return
