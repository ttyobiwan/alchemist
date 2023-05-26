import uuid

from sqlalchemy import Column, ForeignKey, Table, orm
from sqlalchemy.dialects.postgresql import UUID


class Base(orm.DeclarativeBase):
    """Base database model."""

    pk: orm.Mapped[uuid.UUID] = orm.mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


potion_ingredient_association = Table(
    "potion_ingredient",
    Base.metadata,
    Column("potion_id", UUID(as_uuid=True), ForeignKey("potion.pk")),
    Column("ingredient_id", UUID(as_uuid=True), ForeignKey("ingredient.pk")),
)


class Ingredient(Base):
    """Ingredient database model."""

    __tablename__ = "ingredient"

    name: orm.Mapped[str]


class Potion(Base):
    """Potion database model."""

    __tablename__ = "potion"

    name: orm.Mapped[str]
    ingredients: orm.Mapped[list["Ingredient"]] = orm.relationship(
        secondary=potion_ingredient_association,
        backref="potions",
        lazy="selectin",
    )
