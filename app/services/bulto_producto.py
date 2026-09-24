from sqlmodel import Session, select

from app.models.bulto_producto import (
    BultoProducto,
    BultoProductoCreate,
)


def crear_bulto_producto(
    session: Session, bulto_producto: BultoProductoCreate
) -> BultoProducto:
    nuevo_bulto_producto = BultoProducto(**bulto_producto.model_dump())

    session.add(nuevo_bulto_producto)
    session.commit()
    session.refresh(nuevo_bulto_producto)

    return nuevo_bulto_producto


def obtener_bulto_producto(
    session: Session,
    codigo_bulto_pedido: str,
) -> BultoProducto | None:
    statement = select(BultoProducto).where(BultoProducto.codigo == codigo_bulto_pedido)

    return session.exec(statement).first()
