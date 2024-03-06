from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import config

db = config.db

class Role(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    permission: Mapped[int] = mapped_column(Integer)
    
    def to_json(self):
        return dict(
            id=self.id,
            name=self.name,
            permission=self.permission
        )