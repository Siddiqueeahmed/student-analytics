"""Auth endpoint — issues JWT tokens via OAuth2 password flow."""
from __future__ import annotations

import asyncio

import passlib.hash  # type: ignore[import-untyped]
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.jwt import create_access_token
from app.auth.models import TokenResponse
from app.core.database import cursor

router = APIRouter(tags=["auth"])


def _lookup_user(email: str) -> tuple[str, str, str] | None:
    """Returns (user_id, hashed_password, role) or None."""
    with cursor() as conn:
        row = conn.execute(
            "SELECT user_id, hashed_password, role FROM users WHERE email = ? AND is_active = TRUE",
            [email],
        ).fetchone()
    return row  # type: ignore[return-value]


@router.post("/auth/token", response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    row = await asyncio.to_thread(_lookup_user, form.username)
    if row is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_id, hashed_password, role = row
    valid = await asyncio.to_thread(passlib.hash.bcrypt.verify, form.password, hashed_password)
    if not valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user_id, role=role)
    return TokenResponse(access_token=token)
