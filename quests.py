import time
import random
import json


from db.database import DB


db = DB()


class ImplementationError(Exception):
    """Base class for exceptions in this module."""
    pass


class QuestInterface:
    """
    Represents an interface for all quests.
    """
    QUEST_SEARCH_DATA: dict = db.fill_data('db/search_quests.json')
    QUEST_RIDDLE_DATA: dict = db.fill_data('db/riddle_quests.json')

    @staticmethod
    def get_random_quest() -> tuple[str, str]:
        """
        Returns a random quest type and quest ID.
        :return: A tuple containing the quest type and quest ID.
        :rtype: tuple
        """
        if random.random() < 0.5:
            quest_id = random.choice(list(QuestInterface.QUEST_SEARCH_DATA.keys()))
            return 'search', quest_id
        else:
            quest_id = random.choice(list(QuestInterface.QUEST_RIDDLE_DATA.keys()))
            return 'riddle', quest_id

    def get_name(self):
        raise ImplementationError()

    def get_task(self):
        raise ImplementationError()

    def start_quest(self):
        raise ImplementationError()

    def is_quest_completed(self):
        raise ImplementationError()

    def perform(self, user_answer):
        raise ImplementationError()

    def pick_up_winnings(self):
        raise ImplementationError()


class SecretPotionQuest(QuestInterface):
    """
    Represents a quest to find a secret potion.
    """
    def __init__(self, quest_id: str):
        """
        Initialize the quest.
        :param quest_id: The ID of the quest.
        :type quest_id: str
        """
        self.quest_id = quest_id
        self.is_completed = False
        self.quest_name = QuestInterface.QUEST_SEARCH_DATA[quest_id]["quest_name"]
        self.description = QuestInterface.QUEST_SEARCH_DATA[quest_id]["description"]
        self.artifact_name = QuestInterface.QUEST_SEARCH_DATA[quest_id]["required_item"]

    def get_name(self) -> str:
        """
        Returns the name of the quest.
        :return: The name of the quest.
        :rtype: str
        """
        return self.quest_name

    def get_task(self) -> str:
        """
        Returns the task of the quest.
        :return: The task of the quest.
        :rtype: str
        """
        return self.description

    def start_quest(self) -> str:
        """
        Starts the quest.
        :return: The task of the quest.
        :rtype: str
        """
        return f"Для завершения квеста '{self.quest_name}' вам нужно найти {self.artifact_name}."

    def is_quest_completed(self) -> bool:
        """
        Checks if the quest is completed.
        :return: True if the quest is completed, False otherwise.
        :rtype: bool
        """
        return self.is_completed

    def perform(self, user_answer=None) -> bool:
        """
        Performs the quest.
        :param user_answer: The user's answer to the quest.
        :type user_answer: Any
        :return: True if the quest is completed, False otherwise.
        :rtype: bool
        """
        if random.random() < 0.5:
            self.is_completed = True
            return True
        return False

    def pick_up_winnings(self) -> str:
        """
        Picks up the artifact if the quest is completed.
        :return: The name of the artifact if the quest is completed, None otherwise.
        :rtype: str
        """
        if self.is_completed:
            return self.artifact_name
        return None


class AncientRiddleQuest(QuestInterface):
    """
    Represents a quest to solve an ancient riddle.
    """
    def __init__(self, quest_id: str):
        """
        Initialize the quest.
        :param quest_id: The ID of the quest.
        :type quest_id: str
        """
        self.quest_id = quest_id
        self.is_completed = False
        self.quest_name = QuestInterface.QUEST_RIDDLE_DATA[quest_id]["quest_name"]
        self.riddle_text = QuestInterface.QUEST_RIDDLE_DATA[quest_id]["riddle_text"]
        self.answer = QuestInterface.QUEST_RIDDLE_DATA[quest_id]["answer"]
        self.artifact_name = QuestInterface.QUEST_RIDDLE_DATA[quest_id]["artifact_name"]

    def get_name(self) -> str:
        """
        Returns the name of the quest.
        :return: The name of the quest.
        :rtype: str
        """
        return self.quest_name

    def get_task(self) -> str:
        """
        Returns the task of the quest.
        :return: The task of the quest.
        :rtype: str
        """
        return self.riddle_text

    def start_quest(self):
        return self.riddle_text

    def is_quest_completed(self) -> bool:
        """
        Checks if the quest is completed.
        :return: True if the quest is completed, False otherwise.
        :rtype: bool
        """
        return self.is_completed

    def perform(self, user_answer: str) -> bool:
        """
        Performs the quest.
        :param user_answer: The user's answer to the quest.
        :type user_answer: str
        :return: True if the quest is completed, False otherwise.
        :rtype: bool
        """
        if user_answer == self.answer.lower():
            self.is_completed = True
            return True
        return False

    def pick_up_winnings(self):
        """
        Picks up the artifact if the quest is completed.
        :return: The name of the artifact if the quest is completed, None otherwise.
        :rtype: str | None
        """
        if self.is_completed:
            return self.artifact_name
        return None


def quest_manager(quest_type: str, quest_id: str) -> QuestInterface:
    """
    Returns a quest object based on the quest type and ID provided.
    :param quest_type: The type of the quest. Can be either 'search' or 'riddle'.
    :type quest_type: str
    :param quest_id: The ID of the quest.
    :type quest_id: str
    :return: The quest object based on the quest type and ID. Returns None if the quest type is invalid.
    :rtype: QuestInterface
    """
    quest_obj = None

    if quest_type == 'search':
        quest_obj = SecretPotionQuest(quest_id)
    elif quest_type == 'riddle':
        quest_obj = AncientRiddleQuest(quest_id)

    return quest_obj
