import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from alchemist.api import models
from alchemist.api.v2.dependencies import get_repository
from alchemist.database import models as db_models
from alchemist.database.repository import DatabaseRepository

router = APIRouter(prefix="/v2", tags=["v2"])

IngredientRepository = Annotated[
    DatabaseRepository[db_models.Ingredient],
    Depends(get_repository(db_models.Ingredient)),
]
PotionRepository = Annotated[
    DatabaseRepository[db_models.Potion],
    Depends(get_repository(db_models.Potion)),
]


@router.post("/ingredients", status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    data: models.IngredientPayload,
    repository: IngredientRepository,
) -> models.Ingredient:
    ingredient = await repository.create(data.dict())
    return models.Ingredient.from_orm(ingredient)


@router.get("/ingredients", status_code=status.HTTP_200_OK)
async def get_ingredients(repository: IngredientRepository) -> list[models.Ingredient]:
    ingredients = await repository.filter()
    return [models.Ingredient.from_orm(ingredient) for ingredient in ingredients]


@router.get("/ingredients/{pk}", status_code=status.HTTP_200_OK)
async def get_ingredient(
    pk: uuid.UUID,
    repository: IngredientRepository,
) -> models.Ingredient:
    ingredient = await repository.get(pk)
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient does not exist",
        )
    return models.Ingredient.from_orm(ingredient)


@router.post("/potions", status_code=status.HTTP_201_CREATED)
async def create_potion(
    data: models.PotionPayload,
    ingredient_repository: IngredientRepository,
    potion_repository: PotionRepository,
) -> models.Potion:
    data_dict = data.dict()
    ingredients = await ingredient_repository.filter(
        db_models.Ingredient.pk.in_(data_dict.pop("ingredients"))
    )
    potion = await potion_repository.create({**data_dict, "ingredients": ingredients})
    return models.Potion.from_orm(potion)


@router.get("/potions", status_code=status.HTTP_200_OK)
async def get_potions(repository: PotionRepository) -> list[models.Potion]:
    potions = await repository.filter()
    return [models.Potion.from_orm(potion) for potion in potions]


@router.get("/potions/{pk}", status_code=status.HTTP_200_OK)
async def get_potion(pk: uuid.UUID, repository: PotionRepository) -> models.Potion:
    potion = await repository.get(pk)
    if potion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Potion does not exist",
        )
    return models.Potion.from_orm(potion)
