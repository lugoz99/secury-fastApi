from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()  # Base para las tablas
engine = create_engine(
    "sqlite:///database.db", echo=True, future=True
)  # Instancia para el motor

# Autoflush no vaciar las transacciones automaticamente
# y se vincula la sesion a el motor
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # Definir nuevas sessones de bd,

# create the permissions table


# Funcion generadora
def get_db():
    db = SessionLocal()
    try:
        # Generadora session
        yield db
    finally:
        db.close()
