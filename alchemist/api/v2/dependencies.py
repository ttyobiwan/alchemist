from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from alchemist.database import models, repository, session


def get_repository(
    model: type[models.Base],
) -> Callable[[AsyncSession], repository.DatabaseRepository]:
    def func(session: AsyncSession = Depends(session.get_db_session)):
        return repository.DatabaseRepository(model, session)

    return func
