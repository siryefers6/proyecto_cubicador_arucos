from datetime import datetime
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