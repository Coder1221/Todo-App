from dataclasses import dataclass
from datetime import date, datetime
import time
from .status_enum import Status


@dataclass
class Todo:
    id: str
    user_id: str
    title: str
    description: str
    status: int
    status_changed_on: datetime
    created_at: datetime
    updated_at: datetime

    def update_status(self, status) -> None:
        new_status = None
        if isinstance(status, str):
            try:
                if Status(self.status).value == Status[status].value:
                    raise Exception("Status is already {}".format(status))
            except KeyError:
                raise KeyError("Status {} is not valid".format(status))

            new_status = Status[status].value
        else:
            raise ValueError("Status must be a string")

        self.status = new_status
        self.status_changed_on = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def update_title(self, title) -> bool:
        self.title = title
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return True

    def update_description(self, description) -> bool:
        self.description = description
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return True
