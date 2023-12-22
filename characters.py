from pydantic import BaseModel, types, ConfigDict, validator, Field, conlist, field_validator, ValidationInfo
from pprint import pprint
from typing import Union

from db.database import Dialog, DB
from quests import QuestInterface as QI


class NPC:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.level = data.get('level')
        self.dialog_id = data.get('dialog')
        self.db = DB()
        self.messages = self.db.get_dialogs()

    def get_start_messages(self) -> Dialog:
        return self.messages.get(self.dialog_id)

    def get_messages(self, msg_id: Union[str, None]) -> list[Dialog]:
        return self.messages.get(msg_id)

    def get_next_messages(self, msg_id: Union[str, None]) -> list[Dialog]:
        if not msg_id:
            return [self.messages.get(self.dialog_id)]
        msg = self.messages.get(msg_id, [])
        return [self.messages.get(resp_msg_id) for resp_msg_id in msg.responses]

    def offer_quest(self):
        return QI.get_random_quest()


class Enemy(NPC):
    def __init__(self, data):
        self.artifact = data.get('artifact')
        super().__init__(data)

    def drop_artifact(self):
        return self.artifact
