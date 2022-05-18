from dataclasses import dataclass
from datetime import date, datetime
import time
from xmlrpc.client import Boolean
import json
from .status_enum import StatusEnum


@dataclass
class Todo:
    uuid: str
    title: str
    description: str
    status: int
    status_changed_on: datetime
    created_at: datetime
    updated_at: datetime

    def update_status(self, status) -> Boolean:
        new_status = None
        if isinstance(status, int):
            if status == self.status:
                return False
            try:
                StatusEnum(status)
                new_status = status
            except ValueError:
                return False

        elif isinstance(status, str):
            try:
                if StatusEnum(self.status).value == StatusEnum[status].value:
                    return False
            except KeyError:
                return False
            new_status = StatusEnum[status].value
        else:
            return False

        self.status = new_status
        self.status_changed_on = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return True

    def update_title(self, title) -> Boolean:
        self.title = title
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return True

    def update_description(self, description) -> Boolean:
        self.description = description
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return True
