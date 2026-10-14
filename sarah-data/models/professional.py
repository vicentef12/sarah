from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base

class Professional(Base):
    __tablename__ = "professionals"

    id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False)
    rut: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)
    birth_date: Mapped[str] = mapped_column(String(10), nullable=False)
    sex: Mapped[str] = mapped_column(String(1), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    health_center_id: Mapped[str] = mapped_column(String, ForeignKey("health_centers.id"), nullable=False)

    health_center: Mapped["HealthCenter"] = relationship(back_populates="professionals")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="professional")


