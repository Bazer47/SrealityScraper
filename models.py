from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from database import Base

class Property(Base):
    __tablename__ = "property"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100)) 
    title_url: Mapped[str] = mapped_column(String(1000))
    description: Mapped[str] = mapped_column(String(1000))

    def __repr__(self) -> str:
        return f"Property(id={self.id}, title={self.title}, title_url={self.title_url}, description={self.description})"
    
class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id"))
    url: Mapped[str] = mapped_column(String(1000))

    def __repr__(self) -> str:
        return f"Image(id={self.id}, property_id={self.property_id}, url={self.url})"