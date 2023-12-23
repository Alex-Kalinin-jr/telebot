from pydantic import BaseModel, types, ConfigDict, validator, Field, conlist, field_validator, ValidationInfo
from pprint import pprint
from typing import Union

from db.database import Dialog, DB
from quests import QuestInterface as QI


class NPC:
    """
    Represents an NPC.
    """
    def __init__(self, data: dict):
        """
        Initializes the NPC.
        :param data: The data of the NPC.
        :type data: dict
        """
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.level = data.get('level')
        self.dialog_id = data.get('dialog')
        self.db = DB()
        self.messages = self.db.get_dialogs()

    def get_start_messages(self) -> Dialog:
        """
        Get the start messages of the NPC.
        :return: The start messages of the NPC.
        :rtype: Dialog
        """
        return self.messages.get(self.dialog_id)

    def get_messages(self, msg_id: Union[str, None]) -> list[Dialog]:
        """
        Get the messages of the NPC.
        :param msg_id: The ID of the message.
        :type msg_id: str
        :return: The messages of the NPC.
        :rtype: list
        """
        return self.messages.get(msg_id)

    def get_next_messages(self, msg_id: Union[str, None]) -> list[Dialog]:
        """
        Get the next messages of the NPC.
        :param msg_id: The ID of the message.
        :type msg_id: str
        :return: The next messages of the NPC.
        :rtype: list
        """
        if not msg_id:
            return [self.messages.get(self.dialog_id)]
        msg = self.messages.get(msg_id, [])
        return [self.messages.get(resp_msg_id) for resp_msg_id in msg.responses]

    def offer_quest(self) -> tuple[str, str]:
        """
        Offer a quest to the NPC.
        :return: A tuple containing the quest type and quest ID.
        :rtype: tuple
        """
        return QI.get_random_quest()


class Enemy(NPC):
    """Represents an enemy."""
    def __init__(self, data: dict):
        """
        Initializes the enemy.
        :param data: The data of the enemy.
        :type data: dict
        """
        self.artifact = data.get('artifact')
        super().__init__(data)

    def drop_artifact(self) -> str:
        """
        Drops the artifact.
        :return: The name of the artifact.
        :rtype: str
        """
        return self.artifact
