from pipo_ai.db.base import Base


class Pipeline(Base):
    __tablename__ = "pipeline"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="pipelines")
    tasks = relationship(
        "Task", back_populates="pipeline", cascade="all, delete-orphan"
    )
    # ...
