from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import config

db = config.db


class User(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship()

    devices: Mapped[List["Device"]] = relationship(back_populates="user")

    def to_json(self):
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            phone_number=self.phone_number,
            role=self.role.to_json() if self.role else "None",
            devices=[device.to_json(False) for device in self.devices]
        )
