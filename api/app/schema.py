from pydantic import BaseModel, EmailStr
import datetime


class EmailSchema(BaseModel):
    mail_to: list[EmailStr]
    subject: str
    # template_name: str
    # user_name: str
    # project_name: str


class BaseShowSchema(BaseModel):
    id: int
    createdAt: datetime.datetime
    updatedAt: datetime.datetime

    class Config:
        orm_mode = True


class ProjectBaseSchema(BaseModel):
    name: str
    url: str
    description: str
    category: str


class ProjectShowSchema(ProjectBaseSchema, BaseShowSchema):
    ...


class IssueBaseSchema(BaseModel):
    title: str
    type: str
    status: str
    priority: str
    listPosition: float
    description: str
    descriptionText: str
    estimate: int
    timeSpent: int
    timeRemaining: int | None


class IssueShowSchema(IssueBaseSchema, BaseShowSchema):
    ...


class CommentBaseSchema(BaseModel):
    body: str
    userId: int
    issueId: int


class CommentShowSchema(CommentBaseSchema, BaseShowSchema):
    ...


class UserBaseSchema(BaseModel):
    name: str
    email: str
    avatarUrl: str
    projectId: int | None


class UserShowSchema(UserBaseSchema, BaseShowSchema):
    ...
