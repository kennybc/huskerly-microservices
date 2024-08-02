from fastapi import APIRouter, HTTPException, Depends, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from core.user import get_user_from_userpool, get_user_permission_level, list_invites

router = APIRouter()


def get_session_token(session_token: str = Header(...)):
    if not session_token:
        raise HTTPException(status_code=400, detail="Session token missing")
    # TODO: add logic to validate the session token here
    return session_token


@router.get("/users/{user_email}", response_model=dict)
# TODO: use session token , session_token: str = Depends(get_session_token)
def get_user(user_email: str):
    try:
        user = get_user_from_userpool(user_email)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"""Error getting user information: {str(e)}""")


@router.get("/permission/{user_email}", response_model=str)
def get_permission(user_email):
    try:
        permission = get_user_permission_level(user_email)
        return permission
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"""Error authenticating user permissions: {str(e)}""")


@router.get("/permission/{user_email}/{org_id}", response_model=str)
# TODO: should use session token
def get_permission(user_email: str, org_id: int):
    try:
        permission = get_user_permission_level(user_email, org_id)
        return permission
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"""Error authenticating user permissions: {str(e)}""")


@router.get("/invites/{user_email}", response_model=List[tuple])
def list_user_invites(user_email: str):
    try:
        invites = list_invites(user_email)
        return invites
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"""Error fetching invites for user {
                            user_email}: {str(e)}""")
