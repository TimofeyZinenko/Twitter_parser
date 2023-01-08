from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from models.common import get_whole_list
from pydantic import BaseModel, dataclasses
from services.sessons_serviсe import AccountsParserService, get_sesson_service


class Sesson(BaseModel):
    session_id: int


router = APIRouter()


@router.post("/", response_model=Sesson)
async def accounts_parser(
    links: List[str] = Body(
        examples={
            "single link list": {
                "summsry": "With single link",
                "description": "A **single link** list works correctly.",
                "value": ["https://twitter.com/MessariCrypto"],
            },
            "links link": {
                "summsry": "links list",
                "description": "A **links** list works correctly.",
                "value": [
                    "https://twitter.com/tyler",
                    "https://twitter.com/novogratz",
                    "https://twitter.com/MessariCrypto",
                    "https://twitter.com/CryptoHayes",
                    "https://twitter.com/CqweGR",
                ],
            },
            "all 500 records": {
                "summsry": "whole test list",
                "description": "A **links** list works correctly.",
                "value": get_whole_list(),
            },
        },
    ),
    sesson_service: AccountsParserService = Depends(get_sesson_service),
) -> Sesson:
    sesson = await sesson_service.data_process(links)
    return sesson
