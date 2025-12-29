from sqlalchemy import create_engine, Column, Integer, Text, Boolean, DateTime, String, func
from sqlalchemy.orm import declarative_base, Session

engine = create_engine("mysql+pymysql://root@localhost/to_doapp?charset=utf8mb4")

Base = declarative_base()

class Storage(Base):
    __tablename__ = "storage"

    id = Column(Integer, primary_key = True)
    task = Column(String(100), nullable = False)
    description = Column(Text, nullable = True)
    complete = Column(Boolean, default = False, nullable = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_onupdate=func.now())

    def __repr__(self):
        return f"<Storage(id={self.id}, description={self.description}, complete={self.complete}, task={self.task})"
    
Base.metadata.create_all(engine)
print("Todas as tabelas criadas com sucesso!!!")

with Session(engine) as session:
    pass