from datetime import date
from typing import Optional, Literal
from fastapi import Body
from pydantic import BaseModel
from enum import Enum


class Stats(BaseModel):
    stats_date: date = Body(alias="date")
    views: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[float] = None


class Order(BaseModel):
    order: Literal['date', 'views', 'clicks', 'cost'] = 'date'


class OrderDirection(BaseModel):
    direction: Literal['ASC', 'DESC'] = 'ASC'
