from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import config

db = config.db

class LoginData(db.Model):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped["User"] = relationship(uselist=False)
    password_hash: Mapped[str] = mapped_column(String)