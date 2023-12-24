import datetime as dt
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, func, str_255, str_2048


class Sauce(Base):
    __tablename__ = 'sauces'

    sauce_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str_255]
    scoville_heat_units: Mapped[int]
    in_stock: Mapped[bool]
    price: Mapped[int]
    link: Mapped[str_2048]
    img_url: Mapped[Optional[str_2048]]
    create_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    last_update_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
