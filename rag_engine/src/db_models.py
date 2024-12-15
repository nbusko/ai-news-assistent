from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT

from src.database import Base
# from database import Base


class IndexMetainfo(Base):
    __tablename__ = "index_metainfo"

    index_metainf_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    

class Texts(Base):
    __tablename__ = "texts"

    index_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    metainf_id: Mapped[str] = mapped_column(
        BIGINT, ForeignKey("index_metainfo.index_metainf_id")
    )
