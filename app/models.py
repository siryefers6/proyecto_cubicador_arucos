from datetime import datetime

from sqlalchemy import BigInteger, Column, Computed
from sqlmodel import Field, SQLModel


class PedidoBase(SQLModel):
    num_pedido: int
    cantidad_bultos: int
    num_bulto: int

    ancho_mm: float
    largo_mm: float
    alto_mm: float
    volumen_mm: float
    peso: float
    valor_volumetrico: int


class Pedido(PedidoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    fecha_creacion: datetime = Field(default_factory=datetime.now)

    imagen_respaldo: str | None = None
    imagen_medidas: str | None = None


class PedidoCreate(PedidoBase):
    pass


class PedidoPublic(PedidoBase):
    id: int
    fecha_creacion: datetime
    imagen_respaldo: str | None = None
    imagen_medidas: str | None = None


class BultoProductoBase(SQLModel):
    codigo: str = Field(unique=True, index=True)
    descripcion: str

    ancho_mm: int = Field(gt=0)
    largo_mm: int = Field(gt=0)
    alto_mm: int = Field(gt=0)

    peso_grs: int | None = Field(
        default=None,
        gt=0,
    )


class BultoProducto(BultoProductoBase, table=True):
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


class BultoProductoCreate(BultoProductoBase):
    pass


class BultoProductoUpdate(SQLModel):
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


class BultoProductoRead(BultoProductoBase):
    id: int
    volumen_mm3: int
