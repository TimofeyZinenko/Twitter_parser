from fastapi import APIRouter
from pydantic import BaseModel


class ParsingDetails(BaseModel):
    username: str
    status: str


router = APIRouter()


@router.get("/users/status", response_model=list[ParsingDetails])
async def users_status(session_id: int) -> list[ParsingDetails]:
    return list(
        ParsingDetails(username="elonmusk", status="success"),
        ParsingDetails(username="tyler", status="pending"),
    )
