from datetime import datetime, timedelta
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import config

db = config.db

class Session(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(uselist=False)
    access_token: Mapped[str] = mapped_column(String, unique=True)
    refresh_token: Mapped[str] = mapped_column(String, unique=True)
    a_create_time: Mapped[datetime] = mapped_column(DateTime)
    r_create_time: Mapped[datetime] = mapped_column(DateTime)
    a_expire: Mapped[int] = mapped_column(Integer)
    r_expire: Mapped[int] = mapped_column(Integer)
    
    @property
    def is_access_expired(self) -> bool:
        now = datetime.now()
        return now > self.a_create_time + timedelta(seconds=self.a_expire)
            
    
    @property
    def is_refresh_expired(self) -> bool:
        now = datetime.now()
        return now > self.r_create_time + timedelta(seconds=self.r_expire)