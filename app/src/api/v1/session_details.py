from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, dataclasses
from src.services.sesson_details_service import (
    SessonDetailsServise,
    get_sesson_details_service,
)


@dataclasses.dataclass
class ParsingDetails:
    username: str
    status: str


router = APIRouter()


@router.get("/users/status", response_model=list[ParsingDetails])
async def users_status(
    session_id: str,
    sssn_details_service: SessonDetailsServise = Depends(get_sesson_details_service),
) -> list[ParsingDetails]:
    details = await sssn_details_service.get_by(session_id)
    if not details:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Sesson with {session_id} has not existed yet or please check its number and try again.",
        )

    return details
