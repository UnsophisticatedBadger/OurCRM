"""Shared SQLAlchemy declarative base and ORM row models."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CategoryRow(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)


class CallOutcomeRow(Base):
    __tablename__ = "call_outcomes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"))
    outcome: Mapped[str] = mapped_column(String)
    logged_at: Mapped[datetime] = mapped_column(DateTime)
    callback_start_date: Mapped[date | None] = mapped_column(Date, default=None)
    callback_end_date: Mapped[date | None] = mapped_column(Date, default=None)


class ContactRow(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, default="")
    last_name: Mapped[str] = mapped_column(String, default="")
    email: Mapped[str] = mapped_column(String, default="")
    phone: Mapped[str] = mapped_column(String, default="")
    address_street: Mapped[str] = mapped_column(String, default="")
    address_city: Mapped[str] = mapped_column(String, default="")
    address_state: Mapped[str] = mapped_column(String, default="")
    address_zip: Mapped[str] = mapped_column(String, default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[str] = mapped_column(Text, default="")
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), default=None)


class LeadRow(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, default="")
    email: Mapped[str] = mapped_column(String, default="")
    phone: Mapped[str] = mapped_column(String, default="")
    status: Mapped[str] = mapped_column(String, default="")
    source: Mapped[str] = mapped_column(String, default="")
    budget_min: Mapped[int | None] = mapped_column(default=None)
    budget_max: Mapped[int | None] = mapped_column(default=None)
    desired_location: Mapped[str] = mapped_column(String, default="")
    property_type: Mapped[str] = mapped_column(String, default="")
    timeline: Mapped[str] = mapped_column(String, default="")
    notes: Mapped[str] = mapped_column(Text, default="")
