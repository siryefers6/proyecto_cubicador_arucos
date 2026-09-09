from sqlmodel import Session, select

from app.models import Pedido


def crear_pedido(
    session: Session,
    pedido: Pedido,
) -> Pedido:

    session.add(pedido)
    session.commit()
    session.refresh(pedido)

    return pedido


def obtener_pedido(
    session: Session,
    pedido_id: int,
) -> Pedido | None:

    return session.get(Pedido, pedido_id)


def obtener_pedidos(
    session: Session,
    offset: int = 0,
    limit: int = 100,
) -> list[Pedido]:

    return session.exec(
        select(Pedido)
        .offset(offset)
        .limit(limit)
    ).all()


def eliminar_pedido(
    session: Session,
    pedido_id: int,
) -> bool:

    pedido = session.get(Pedido, pedido_id)

    if not pedido:
        return False

    session.delete(pedido)
    session.commit()

    return True