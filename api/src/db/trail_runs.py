from typing import Optional
from pydantic import BaseModel
from sqlalchemy import JSON, Column, ForeignKey, Integer
from sqlmodel import Field, SQLModel
from enum import Enum

from src.db.trail_steps import TrailStep


class TrailRunEnum(str, Enum):
    RUN_TYPE_COURSE = "RUN_TYPE_COURSE"


class StatusEnum(str, Enum):
    STATUS_IN_PROGRESS = "STATUS_IN_PROGRESS"
    STATUS_COMPLETED = "STATUS_COMPLETED"
    STATUS_PAUSED = "STATUS_PAUSED"
    STATUS_CANCELLED = "STATUS_CANCELLED"


class TrailRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: dict = Field(default={}, sa_column=Column(JSON))
    status: StatusEnum = StatusEnum.STATUS_IN_PROGRESS
    # foreign keys
    trail_id: int = Field(
        sa_column=Column(Integer, ForeignKey("trail.id", ondelete="CASCADE"))
    )
    course_id: int = Field(
        sa_column=Column(Integer, ForeignKey("course.id", ondelete="CASCADE"))
    )
    org_id: int = Field(
        sa_column=Column(Integer, ForeignKey("organization.id", ondelete="CASCADE"))
    )
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    )
    # timestamps
    creation_date: str
    update_date: str


class TrailRunCreate(TrailRun):
    pass


# trick because Lists are not supported in SQLModel (runs: list[TrailStep] )
class TrailRunRead(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: dict = Field(default={}, sa_column=Column(JSON))
    status: StatusEnum = StatusEnum.STATUS_IN_PROGRESS
    # foreign keys
    trail_id: int = Field(default=None, foreign_key="trail.id")
    course_id: int = Field(default=None, foreign_key="course.id")
    org_id: int = Field(default=None, foreign_key="organization.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    # course object
    course: Optional[dict]
    # timestamps
    creation_date: Optional[str]
    update_date: Optional[str]
    # number of activities in course
    course_total_steps: int
    steps: list[TrailStep]
    pass
