from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# SQLite DB (local file)
DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ------------------ MODELS ------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Relationship with progress
    progress = relationship("Progress", back_populates="user", cascade="all, delete")


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_url = Column(String, index=True, nullable=False)
    status = Column(String(20), default="todo")  # 'todo', 'in_progress', 'done'

    # Back reference
    user = relationship("User", back_populates="progress")


# ------------------ INIT ------------------

Base.metadata.create_all(bind=engine)
