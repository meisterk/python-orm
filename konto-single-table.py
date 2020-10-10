from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Objektorientiertes Modell
Base = declarative_base()


class Konto(Base):
    __tablename__ = "konto"
    id = Column(Integer, primary_key=True)
    kontostand = Column(Numeric(10, 2))
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "konto",
        "polymorphic_on": type,
    }


class Girokonto(Konto):
    dispo = Column(Numeric(10, 2))
    __mapper_args__ = {"polymorphic_identity": "girokonto"}


class Sparkonto(Konto):
    zinssatz = Column(Numeric(10, 1))
    __mapper_args__ = {"polymorphic_identity": "sparkonto"}


# Datenbank und Tabellen erstellen
engine = create_engine("sqlite:///konto-single-table.db", echo=True)
Base.metadata.create_all(engine)

# Python-Objekte erstellen
konto1 = Konto(kontostand=11.11)
konto2 = Girokonto(kontostand=22.22, dispo=50.00)
konto3 = Sparkonto(kontostand=33.33, zinssatz=1.5)

# Python-Objekte in Datenbank speichern
session = Session(engine)
session.add_all([konto1, konto2, konto3])
session.commit()
