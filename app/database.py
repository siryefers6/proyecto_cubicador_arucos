from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy import event

sqlite_url = "sqlite:///data/cubicador.db"

connect_args = {"check_same_thread": False}

engine = create_engine(
    sqlite_url,
    connect_args=connect_args,
)

@event.listens_for(engine, "connect")
def configurar_sqlite(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()

    cursor.execute("PAGMA journal_mode=WAL")
    cursor.execute("PAGMA synchronous=NORMAL")

    cursor.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session