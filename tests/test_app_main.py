import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app
from app.models import Pedido


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


def test_crear_pedido(client: TestClient):
    response = client.post(
        "/pedidos",
        json={
            "num_pedido": "PED-001",
            "cantidad_bultos": 2,
            "num_bulto": 1,
            "ancho_mm": 300,
            "largo_mm": 500,
            "alto_mm": 200,
            "volumen_mm": 30000000,
            "peso": 15.5,
            "valor_volumetrico": 30,
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["num_pedido"] == "PED-001"
    assert data["cantidad_bultos"] == 2
    assert data["num_bulto"] == 1
    assert data["ancho_mm"] == 300
    assert data["largo_mm"] == 500
    assert data["alto_mm"] == 200
    assert data["volumen_mm"] == 30000000
    assert data["peso"] == 15.5
    assert data["valor_volumetrico"] == 30
    assert data["id"] is not None
    assert data["fecha_creacion"] is not None


def test_crear_pedido_incompleto(client: TestClient):
    response = client.post(
        "/pedidos",
        json={
            "num_pedido": "PED-001",
        },
    )

    assert response.status_code == 422


def test_obtener_pedidos(session: Session, client: TestClient):
    pedido_1 = Pedido(
        num_pedido="PED-001",
        cantidad_bultos=2,
        num_bulto=1,
        ancho_mm=300,
        largo_mm=500,
        alto_mm=200,
        volumen_mm=30000000,
        peso=15.5,
        valor_volumetrico=30,
    )

    pedido_2 = Pedido(
        num_pedido="PED-002",
        cantidad_bultos=1,
        num_bulto=1,
        ancho_mm=400,
        largo_mm=600,
        alto_mm=250,
        volumen_mm=60000000,
        peso=20.0,
        valor_volumetrico=60,
    )

    session.add(pedido_1)
    session.add(pedido_2)
    session.commit()

    response = client.get("/pedidos")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2

    assert data[0]["num_pedido"] == pedido_1.num_pedido
    assert data[0]["id"] == pedido_1.id
    assert data[0]["peso"] == pedido_1.peso

    assert data[1]["num_pedido"] == pedido_2.num_pedido
    assert data[1]["id"] == pedido_2.id
    assert data[1]["peso"] == pedido_2.peso


def test_obtener_pedido(session: Session, client: TestClient):
    pedido = Pedido(
        num_pedido="PED-001",
        cantidad_bultos=2,
        num_bulto=1,
        ancho_mm=300,
        largo_mm=500,
        alto_mm=200,
        volumen_mm=30000000,
        peso=15.5,
        valor_volumetrico=30,
    )

    session.add(pedido)
    session.commit()

    response = client.get(f"/pedidos/{pedido.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == pedido.id
    assert data["num_pedido"] == "PED-001"
    assert data["ancho_mm"] == 300
    assert data["largo_mm"] == 500
    assert data["peso"] == 15.5


def test_obtener_pedido_no_existente(client: TestClient):
    response = client.get("/pedidos/999")

    assert response.status_code == 404


def test_eliminar_pedido(session: Session, client: TestClient):
    pedido = Pedido(
        num_pedido="PED-001",
        cantidad_bultos=1,
        num_bulto=1,
        ancho_mm=300,
        largo_mm=500,
        alto_mm=200,
        volumen_mm=30000000,
        peso=15.5,
        valor_volumetrico=30,
    )

    session.add(pedido)
    session.commit()

    response = client.delete(f"/pedidos/{pedido.id}")

    pedido_en_db = session.get(Pedido, pedido.id)

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert pedido_en_db is None