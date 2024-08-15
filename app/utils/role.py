from enum import Enum


class RoleEnum(Enum):
    SUPERUSER = 'superuser'
    ADMIN = 'admin'
    USER = 'user'

    def __str__(self):
        return self.value
