from enum import Enum, IntEnum


class ProjectCategory(str, Enum):
    SOFTWARE = "software"
    MARKETING = "marketing"
    BUSINESS = "business"


class IssueType(str, Enum):
    TASK = "task"
    BUG = "bug"
    STORY = "story"


class IssueStatus(str, Enum):
    BACKLOG = "backlog"
    SELECTED = "selected"
    INPROGRESS = "inprogress"
    DONE = "done"


class IssuePriority(IntEnum):
    HIGHEST = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    LOWEST = 1
