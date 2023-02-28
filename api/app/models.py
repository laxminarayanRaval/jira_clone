from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql import func

from sqlalchemy import create_engine, func
from app.config import settings


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_tables():
    print("creating tables............")
    metadata.create_all(bind=engine)


@as_declarative()
class ModelBase:
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)

    @classmethod
    def get(cls, pk, db):
        return db.query(cls).filter(cls.id == pk).first()

    @classmethod
    def get_all(cls, db):
        return db.query(cls).all()

    @classmethod
    def delete(cls, pk, db):
        result = db.query(cls).filter(cls.id == pk).delete()
        db.commit()
        return result

    @classmethod
    def update(cls, pk, new_data, db):
        _query = db.query(cls).filter(cls.id == pk)
        _obj = _query.first()

        if not _obj:
            return None

        _query.update(new_data, synchronize_session=False)
        db.commit()
        db.refresh(_obj)

        return _obj


metadata = ModelBase.metadata


class Project(ModelBase):
    __tablename__ = "project"

    name = Column(String, nullable=False)
    url = Column(String)
    description = Column(Text)
    category = Column(String, nullable=False)

    users = relationship("User", back_populates="project")
    issues = relationship("Issue", back_populates="project")


class Issue(ModelBase):
    __tablename__ = "issue"

    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    listPosition = Column(Float(53), nullable=False)
    description = Column(Text)
    descriptionText = Column(Text)
    estimate = Column(Integer)
    timeSpent = Column(Integer)
    timeRemaining = Column(Integer)

    reporterId = Column(Integer, nullable=False)
    projectId = Column(ForeignKey("project.id"), nullable=False)

    project = relationship("Project", foreign_keys="Issue.projectId")
    users = relationship("User", secondary="issue_users_user")
    comments = relationship("Comment", back_populates="issue")


class User(ModelBase):
    __tablename__ = "user"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    avatarUrl = Column(String(2000), nullable=False)

    projectId = Column(ForeignKey("project.id"))

    project = relationship(
        "Project",
        foreign_keys="User.projectId",
        # back_populates="project",
    )
    issue = relationship("Issue", secondary="issue_users_user")
    # comment = relationship("Comment", back_populates="comment")


class Comment(ModelBase):
    __tablename__ = "comment"

    body = Column(Text, nullable=False)

    userId = Column(ForeignKey("user.id"), nullable=False)
    issueId = Column(ForeignKey("issue.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", foreign_keys="Comment.userId")
    issue = relationship("Issue", foreign_keys="Comment.issueId")


t_issue_users_user = Table(
    "issue_users_user",
    metadata,
    Column(
        "issueId",
        ForeignKey("issue.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
    Column(
        "userId",
        ForeignKey("user.id"),
        primary_key=True,
        nullable=False,
        index=True,
    ),
)
