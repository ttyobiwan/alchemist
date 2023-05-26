import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from alchemist.api import models
from alchemist.database import models as db_models
from alchemist.database.session import get_db_session

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/ingredients", status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    data: models.IngredientPayload,
    session: AsyncSession = Depends(get_db_session),
) -> models.Ingredient:
    ingredient = db_models.Ingredient(**data.dict())
    session.add(ingredient)
    await session.commit()
    await session.refresh(ingredient)
    return models.Ingredient.from_orm(ingredient)


@router.get("/ingredients", status_code=status.HTTP_200_OK)
async def get_ingredients(
    session: AsyncSession = Depends(get_db_session),
) -> list[models.Ingredient]:
    ingredients = await session.scalars(select(db_models.Ingredient))
    return [models.Ingredient.from_orm(ingredient) for ingredient in ingredients]


@router.get("/ingredients/{pk}", status_code=status.HTTP_200_OK)
async def get_ingredient(
    pk: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> models.Ingredient:
    ingredient = await session.get(db_models.Ingredient, pk)
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient does not exist",
        )
    return models.Ingredient.from_orm(ingredient)


@router.post("/potions", status_code=status.HTTP_201_CREATED)
async def create_potion(
    data: models.PotionPayload,
    session: AsyncSession = Depends(get_db_session),
) -> models.Potion:
    data_dict = data.dict()
    ingredients = await session.scalars(
        select(db_models.Ingredient).where(
            db_models.Ingredient.pk.in_(data_dict.pop("ingredients"))
        )
    )
    potion = db_models.Potion(**data_dict, ingredients=list(ingredients))
    session.add(potion)
    await session.commit()
    await session.refresh(potion)
    return models.Potion.from_orm(potion)


@router.get("/potions", status_code=status.HTTP_200_OK)
async def get_potions(
    session: AsyncSession = Depends(get_db_session),
) -> list[models.Potion]:
    potions = await session.scalars(select(db_models.Potion))
    return [models.Potion.from_orm(potion) for potion in potions]


@router.get("/potions/{pk}", status_code=status.HTTP_200_OK)
async def get_potion(
    pk: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> models.Potion:
    potion = await session.get(db_models.Potion, pk)
    if potion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Potion does not exist",
        )
    return models.Potion.from_orm(potion)
