from datetime import date
from sqlalchemy.orm import relationship

from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column


from database.connection import Base




class Patient(Base):


   __tablename__ = "patients"


   id: Mapped[str] = mapped_column(
       String,
       primary_key=True,
   )


   first_name: Mapped[str] = mapped_column(
       String,
       nullable=False,
   )


   last_name: Mapped[str] = mapped_column(
       String,
       nullable=False,
   )


   rut: Mapped[str] = mapped_column(
       String,
       nullable=False,
       unique=True,
   )


   birth_date: Mapped[date] = mapped_column(
       Date,
       nullable=False,
   )


   sex: Mapped[str] = mapped_column(
       String,
       nullable=False,
   )


   email: Mapped[str] = mapped_column(
       String,
       nullable=False,
   )


   phone: Mapped[str] = mapped_column(
       String,
       nullable=False,
   )


   current_height: Mapped[float] = mapped_column(
       nullable=False,
   )


   current_weight: Mapped[float] = mapped_column(
       nullable=False,
   )


   lives_alone: Mapped[bool] = mapped_column(
       nullable=False,
   )


   bmi: Mapped[float] = mapped_column(
       nullable=False,
   )


   context: Mapped[str] = mapped_column(
       Text,
       nullable=False,
   )


   psychological_profile: Mapped[str] = mapped_column(
       String,
       nullable=False,
   )


