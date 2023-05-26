import uuid

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    """Ingredient model."""

    pk: uuid.UUID
    name: str

    class Config:
        orm_mode = True


class IngredientPayload(BaseModel):
    """Ingredient payload model."""

    name: str = Field(min_length=1, max_length=127)


class Potion(BaseModel):
    """Potion model."""

    pk: uuid.UUID
    name: str
    ingredients: list[Ingredient]

    class Config:
        orm_mode = True


class PotionPayload(BaseModel):
    """Potion payload model."""

    name: str = Field(min_length=1, max_length=127)
    ingredients: list[uuid.UUID] = Field(min_items=1)
