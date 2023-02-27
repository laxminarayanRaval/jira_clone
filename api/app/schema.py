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


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    avatarUrl: str | None
    projectId: int | None


class UserShowSchema(UserBaseSchema, BaseShowSchema):
    ...


class IssueBaseSchema(BaseModel):
    title: str
    type: str
    status: str
    priority: str
    listPosition: float
    reporterId: int
    description: str | None
    descriptionText: str | None
    estimate: int | None
    timeSpent: int | None
    timeRemaining: int | None


class IssueShowSchema(IssueBaseSchema, BaseShowSchema):
    userIds: list[int] | None
    ...


class ProjectBaseSchema(BaseModel):
    name: str
    url: str | None
    description: str | None
    category: str | None


class ProjectShowSchema(ProjectBaseSchema, BaseShowSchema):
    users: list[UserShowSchema]
    issues: list[IssueShowSchema]


class OneProject(BaseModel):
    project: ProjectShowSchema


class CommentBaseSchema(BaseModel):
    body: str
    userId: int
    issueId: int


class CommentShowSchema(CommentBaseSchema, BaseShowSchema):
    ...
