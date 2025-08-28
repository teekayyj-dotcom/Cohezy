import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class MemberRole(str, enum.Enum):
    OWNER = "owner"
    CO_HOST = "co_host"
    MEMBER = "member"
