import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.models import BultoProductoCreate
from app.services.bulto_producto import crear_bulto_producto, obtener_bulto_producto


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


def test_crear_bulto_producto(session: Session):
    # Arrange
    data = BultoProductoCreate(
        codigo="0074711352086",
        descripcion="CORCHETES ESTANDAR 26/6 SWINGLINE 5000",
        ancho_mm=44,
        largo_mm=30,
        alto_mm=113,
        peso_grs=100,
    )

    # Act
    bulto_producto = crear_bulto_producto(session, data)

    # Assert
    assert bulto_producto.id is not None
    assert bulto_producto.codigo == "0074711352086"
    assert bulto_producto.descripcion == "CORCHETES ESTANDAR 26/6 SWINGLINE 5000"
    assert bulto_producto.ancho_mm == 44
    assert bulto_producto.largo_mm == 30
    assert bulto_producto.alto_mm == 113
    assert bulto_producto.peso_grs == 100

    # El volumen lo calcula la BD
    assert bulto_producto.volumen_mm3 == 44 * 30 * 113

def test_obtener_bulto_producto(session: Session):
    # Arrange
    data = BultoProductoCreate(
        codigo="0074711352086",
        descripcion="CORCHETES ESTANDAR 26/6 SWINGLINE 5000",
        ancho_mm=44,
        largo_mm=30,
        alto_mm=113,
        peso_grs=100,
    )

    crear_bulto_producto(session, data)

    # Act
    bulto_producto = obtener_bulto_producto(
        session,
        codigo_bulto_pedido="0074711352086",
    )

    # Assert
    assert bulto_producto is not None
    assert bulto_producto.id is not None
    assert bulto_producto.codigo == "0074711352086"
    assert bulto_producto.descripcion == "CORCHETES ESTANDAR 26/6 SWINGLINE 5000"
    assert bulto_producto.ancho_mm == 44
    assert bulto_producto.largo_mm == 30
    assert bulto_producto.alto_mm == 113
    assert bulto_producto.peso_grs == 100

    # El volumen lo calcula la BD
    assert bulto_producto.volumen_mm3 == 44 * 30 * 113

def test_obtener_bulto_producto_no_existente(session: Session):
    # Act
    bulto_producto = obtener_bulto_producto(
        session,
        codigo_bulto_pedido="9999999999999",
    )

    # Assert
    assert bulto_producto is None


# def test_read_heroes(session: Session):
#     hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
#     hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
#     session.add(hero_1)
#     session.add(hero_2)
#     session.commit()

#     response = client.get("/heroes/")
#     data = response.json()

#     assert response.status_code == 200

#     assert len(data) == 2
#     assert data[0]["name"] == hero_1.name
#     assert data[0]["secret_name"] == hero_1.secret_name
#     assert data[0]["age"] == hero_1.age
#     assert data[0]["id"] == hero_1.id
#     assert data[1]["name"] == hero_2.name
#     assert data[1]["secret_name"] == hero_2.secret_name
#     assert data[1]["age"] == hero_2.age
#     assert data[1]["id"] == hero_2.id


# def test_read_hero(session: Session, client: TestClient):
#     hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
#     session.add(hero_1)
#     session.commit()

#     response = client.get(f"/heroes/{hero_1.id}")
#     data = response.json()

#     assert response.status_code == 200
#     assert data["name"] == hero_1.name
#     assert data["secret_name"] == hero_1.secret_name
#     assert data["age"] == hero_1.age
#     assert data["id"] == hero_1.id


# def test_update_hero(session: Session, client: TestClient):
#     hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
#     session.add(hero_1)
#     session.commit()

#     response = client.patch(f"/heroes/{hero_1.id}", json={"name": "Deadpuddle"})
#     data = response.json()

#     assert response.status_code == 200
#     assert data["name"] == "Deadpuddle"
#     assert data["secret_name"] == "Dive Wilson"
#     assert data["age"] is None
#     assert data["id"] == hero_1.id


# def test_delete_hero(session: Session, client: TestClient):
#     hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
#     session.add(hero_1)
#     session.commit()

#     response = client.delete(f"/heroes/{hero_1.id}")

#     hero_in_db = session.get(Hero, hero_1.id)

#     assert response.status_code == 200

#     assert hero_in_db is None
