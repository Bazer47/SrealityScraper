from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Property(Base):
    __tablename__ = "property"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100)) 
    prop_url_endp: Mapped[str] = mapped_column(String(1000))
    price: Mapped[str] = mapped_column(String(30))
    locality: Mapped[str] = mapped_column(String(500))

    def __repr__(self) -> str:
        return f"Property(id={self.id}, name={self.name}, prop_url_endp={self.prop_url_endp}, price={self.price}, locality={self.locality})"
    
class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id"))
    url: Mapped[str] = mapped_column(String(1000))

    def __repr__(self) -> str:
        return f"Image(id={self.id}, property_id={self.property_id}, url={self.url})"