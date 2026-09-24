from sqlmodel import Session, select

from app.models.bulto_embalaje_original import (
    BultoEmbalajeOriginal,
    BultoEmbalajeOriginalCreate,
)


def crear_bulto_embalaje_original(
    session: Session, bulto_embalaje_original: BultoEmbalajeOriginalCreate
) -> BultoEmbalajeOriginal:
    nuevo_bulto_producto = BultoEmbalajeOriginal(**bulto_embalaje_original.model_dump())

    session.add(nuevo_bulto_producto)
    session.commit()
    session.refresh(nuevo_bulto_producto)

    return nuevo_bulto_producto


def obtener_bulto_embalaje_original(
    session: Session,
    codigo_bulto_pedido: str,
) -> BultoEmbalajeOriginal | None:
    statement = select(BultoEmbalajeOriginal).where(
        BultoEmbalajeOriginal.codigo == codigo_bulto_pedido
    )

    return session.exec(statement).first()
