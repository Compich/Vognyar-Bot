import datetime as dt
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, func, int64, str_40


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int64] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[Optional[str_40]]
    subscribed: Mapped[bool] = mapped_column(server_default=text('false'))
    min_scoville_heat_units: Mapped[int] = mapped_column(
        server_default=text('0')
    )
    reg_time: Mapped[dt.datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return str(self.username)
