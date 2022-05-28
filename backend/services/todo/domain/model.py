from dataclasses import dataclass
from datetime import date, datetime
import time
from .status_enum import Status
from typing import List
import uuid


@dataclass
class Todo:
    user_id: str
    title: str
    description: str
    status: str
    priority: int = 0
    updated_at: datetime = None
    status_changed_on: datetime = None
    created_at: datetime = datetime.now()
    id: str = str(uuid.uuid4())
    deleted: bool = False

    def update_status(self, status: str) -> None:
        """raising keyerror in case if we don't have the key in status enum"""
        if status not in Status.__members__:
            raise KeyError("Status {} is not valid".format(status))

        self.status = Status[status].value
        self.status_changed_on = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def update_title(self, title: str) -> None:
        self.title = title
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def update_description(self, description: str) -> None:
        self.description = description
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def increase_priority(self) -> None:
        self.priority = self.priority + 1
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def decrease_priority(self) -> None:
        self.priority = self.priority - 1
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
