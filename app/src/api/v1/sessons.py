from fastapi import APIRouter, Body
from pydantic import BaseModel


class Sesson(BaseModel):
    session_id: int


router = APIRouter()


@router.put("/", response_model=Sesson)
async def accounts_parser(
    links: list[str] = Body(
        examples={
            "single link list": {
                "summsry": "With single link",
                "description": "A **single link** list works correctly.",
                "value": ["link_1"],
            },
            "links link": {
                "summsry": "links list",
                "description": "A **links** list works correctly.",
                "value": [
                    "link_1",
                    "link_2",
                    "link_3",
                    "link_4",
                    "link_5",
                ],
            },
        },
    ),
) -> Sesson:

    return Sesson(session_id=42)
