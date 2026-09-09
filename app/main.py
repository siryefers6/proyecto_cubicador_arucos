from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session

from app.database import create_db_and_tables, get_session
from app.models import Pedido, PedidoCreate, PedidoPublic
from app.services.pedidos import (
    crear_pedido,
    eliminar_pedido,
    obtener_pedido,
    obtener_pedidos,
)


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/pedidos", response_model=PedidoPublic)
def crear(pedido: PedidoCreate, session: SessionDep):
    pedido_db = Pedido.model_validate(pedido)
    return crear_pedido(session, pedido_db)


@app.get("/pedidos", response_model=list[Pedido])
def listar(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return obtener_pedidos(session, offset, limit)


@app.get("/pedidos/{pedido_id}", response_model=Pedido)
def obtener(pedido_id: int, session: SessionDep):

    pedido = obtener_pedido(session, pedido_id)

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado",
        )

    return pedido


@app.delete("/pedidos/{pedido_id}")
def eliminar(pedido_id: int, session: SessionDep):

    if not eliminar_pedido(session, pedido_id):
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado",
        )

    return {"ok": True}