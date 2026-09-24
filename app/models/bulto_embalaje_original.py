from sqlalchemy import BigInteger, Column, Computed
from sqlmodel import Field, SQLModel


class BultoEmbalajeOriginalBase(SQLModel):
    codigo: str = Field(unique=True, index=True)
    descripcion: str

    ancho_mm: int = Field(gt=0)
    largo_mm: int = Field(gt=0)
    alto_mm: int = Field(gt=0)

    peso_grs: int | None = Field(
        default=None,
        gt=0,
    )


class BultoEmbalajeOriginal(BultoEmbalajeOriginalBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    volumen_mm3: int = Field(
        sa_column=Column(
            BigInteger,
            Computed(
                "ancho_mm * largo_mm * alto_mm",
                persisted=True,
            ),
            nullable=False,
        )
    )


class BultoEmbalajeOriginalCreate(BultoEmbalajeOriginalBase):
    pass


class BultoEmbalajeOriginalUpdate(SQLModel):
    codigo: str | None = None
    descripcion: str | None = None

    ancho_mm: int | None = Field(
        default=None,
        gt=0,
    )

    largo_mm: int | None = Field(
        default=None,
        gt=0,
    )

    alto_mm: int | None = Field(
        default=None,
        gt=0,
    )

    peso_grs: int | None = Field(
        default=None,
        gt=0,
    )


class BultoEmbalajeOriginalRead(BultoEmbalajeOriginalBase):
    id: int
    volumen_mm3: int
