from typing import Optional

from sqlmodel import SQLModel, Field


class SolarPanel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    price: float
    power_output: int
    current: int
    warranty_years: int
    weight: float
    height: float
    monocrystal: bool = False
    available: bool = True

