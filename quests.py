import time
import random
import json


from db.database import DB


db = DB()


class ImplementationError(Exception):
    pass


class QuestInterface:
    QUEST_SEARCH_DATA: dict = db.fill_data('db/search_quests.json')
    QUEST_RIDDLE_DATA: dict = db.fill_data('db/riddle_quests.json')

    @staticmethod
    def get_random_quest() -> tuple[str, str]:
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
    def __init__(self, quest_id):
        self.quest_id = quest_id
        self.is_completed = False
        self.quest_name = QuestInterface.QUEST_SEARCH_DATA[quest_id]["quest_name"]
        self.description = QuestInterface.QUEST_SEARCH_DATA[quest_id]["description"]
        self.artifact_name = QuestInterface.QUEST_SEARCH_DATA[quest_id]["required_item"]

    def get_name(self):
        return self.quest_name

    def get_task(self):
        return self.description

    def start_quest(self):
        return f"Для завершения квеста '{self.quest_name}' вам нужно найти {self.artifact_name}."

    def is_quest_completed(self):
        return self.is_completed

    def perform(self, user_answer=None):
        if random.random() < 0.5:
            self.is_completed = True
            return True                 # Вы обнаружили {self.artifact_name}!
        return False                    # К сожалению, {self.artifact_name} не было найдено. Продолжайте поиски!

    def pick_up_winnings(self):
        if self.is_completed:
            return self.artifact_name
        return None


class AncientRiddleQuest(QuestInterface):
    def __init__(self, quest_id):
        self.quest_id = quest_id
        self.is_completed = False
        self.quest_name = QuestInterface.QUEST_RIDDLE_DATA[quest_id]["quest_name"]
        self.riddle_text = QuestInterface.QUEST_RIDDLE_DATA[quest_id]["riddle_text"]
        self.answer = QuestInterface.QUEST_RIDDLE_DATA[quest_id]["answer"]
        self.artifact_name = QuestInterface.QUEST_RIDDLE_DATA[quest_id]["artifact_name"]

    def get_name(self):
        return self.quest_name

    def get_task(self):
        return self.riddle_text

    def start_quest(self):
        print(f"Для выполнения квеста '{self.quest_name}' вам нужно разгадать древнюю загадку.")
        print(f"Загадка: {self.riddle_text}")
        return self.riddle_text

    def is_quest_completed(self):
        return self.is_completed

    def perform(self, user_answer):
        if user_answer == self.answer.lower():
            self.is_completed = True
            return True             # Верно! Загадка разгадана.
        return False                # Неверный ответ. Продолжайте разгадывать загадку!

    def pick_up_winnings(self):
        if self.is_completed:
            return self.artifact_name
        return None


def quest_manager(quest_type: str, quest_id: str) -> ImplementationError:
    quest_obj = None

    if quest_type == 'search':
        quest_obj = SecretPotionQuest(quest_id)
    elif quest_type == 'riddle':
        quest_obj = AncientRiddleQuest(quest_id)

    return quest_obj


























# if __name__ == '__main__':
#     # from world_map_class import Location
#     # START_LOCATION = "location_1"
#     # player = Protagonist("Oleg", 1, Location(START_LOCATION))
#
#     quest_1 = quest_manager("search", "quest_1", "player")
#     while not quest_1.is_completed:
#         quest_1.interact_with_quest()
#
#     quest_2 = quest_manager("riddle", "quest_3", "player")
#     while not quest_2.is_completed:
#         quest_2.interact_with_quest()

    # quest_1 = SecretPotionQuest("player", "quest_1")
    # while not quest_1.is_completed:
    #     quest_1.interact_with_quest()
    # quest_2 = AncientRiddleQuest("player", "quest_1")
    # while not quest_2.is_completed:
    #     quest_2.interact_with_quest()


# class SecretPotionQuest(QuestInterface):
#     def __init__(self, quest_id):
#         self.quest_id = quest_id
#         self.is_completed = False
#         self.quest_name = QUEST_SEARCH_DATA["quest_name"]
#         self.description = QUEST_SEARCH_DATA["description"]
#         self.required_item = QUEST_SEARCH_DATA["required_item"]
#
#
    # def start_quest(self):
    #     print(f"Для выполнения квеста '{self.quest_name}' вам нужно найти {self.required_item}.")
    #
    # def complete_quest(self):
    #     print("Поздравляю! Вы нашли все необходимые ингредиенты и завершили квест.")
    #     self.is_completed = True
    #
    # def interact_with_quest(self):
    #     if not self.is_completed:
    #         print("===== Квест 'Тайное зелье' =====")
    #         print("1. Искать загадочное растение")
    #         print("2. Проверить текущий прогресс квеста")
    #         print("3. Вернуться в основное меню")
    #         choice = input("Выберите опцию (1-3): ")
    #
    #         if choice == '1':
    #             self.search_for_mysterious_herb()
    #         elif choice == '2':
    #             self.check_quest_progress()
    #         elif choice == '3':
    #             print("Возврат в основное меню.")
    #         else:
    #             print("Некорректный ввод. Пожалуйста, выберите опцию от 1 до 3.")
    #     else:
    #         print("Квест уже завершен.")
    #
    # def search_for_mysterious_herb(self):
    #     print(f"Вы отправились на поиски {self.required_item}...")
    #     time.sleep(1)
    #     if random.random() < 0.5:
    #         print(f"Вы обнаружили {self.required_item}!")
    #         self.player.take(self.required_item)
    #         self.complete_quest()
    #     else:
    #         print(f"К сожалению, {self.required_item} не было найдено. Продолжайте поиски!")
    #
    # def check_quest_progress(self, player_inventory):
    #     print("Текущий прогресс квеста:")
    #     if self.required_item in player_inventory:
    #         print(f"- Вы уже нашли {self.required_item}.")
    #     else:
    #         print(f"- Требуется найти {self.required_item}.")



# class AncientRiddleQuest(QuestInterface):
#     def __init__(self, quest_id):
#         self.quest_id = quest_id
#         self.is_completed = False
#         self.quest_name = QUEST_RIDDLE_DATA["quest_name"]
#         self.riddle_text = QUEST_RIDDLE_DATA["riddle_text"]
#         self.answer = QUEST_RIDDLE_DATA["answer"]
#         self.artifact_name = QUEST_RIDDLE_DATA["artifact_name"]
#
    # def start_quest(self):
    #     print(f"Для выполнения квеста '{self.quest_name}' вам нужно разгадать древнюю загадку.")
    #
    # def complete_quest(self):
    #     print(f"Поздравляю! Вы разгадали загадку и получили древний артефакт: {self.artifact_name}.")
    #     self.is_completed = True
    #
    # def interact_with_quest(self):
    #     if not self.is_completed:
    #         print(f"===== Квест '{self.quest_name}' =====")
    #         print("1. Разгадать загадку")
    #         print("2. Проверить текущий прогресс квеста")
    #         print("3. Вернуться в основное меню")
    #         choice = input("Выберите опцию (1-3): ")
    #
    #         if choice == '1':
    #             self.solve_riddle()
    #         elif choice == '2':
    #             self.check_quest_progress()
    #         elif choice == '3':
    #             print("Возврат в основное меню.")
    #         else:
    #             print("Некорректный ввод. Пожалуйста, выберите опцию от 1 до 3.")
    #     else:
    #         print("Квест уже завершен.")
    # def solve_riddle(self):
    #     print("Загадка: ", self.riddle_text)
    #     print("Вы пытаетесь разгадать древнюю загадку...")
    #     user_answer = input("Введите ваш ответ: ").lower()
    #     if user_answer == self.answer.lower():
    #         print("Верно! Загадка разгадана.")
    #         self.complete_quest()
    #     else:
    #         print("Неверный ответ. Продолжайте разгадывать загадку!")
    #
    # def check_quest_progress(self):
    #     print("Текущий прогресс квеста:")
    #     if self.is_completed:
    #         print("- Квест успешно завершен.")
    #     else:
    #         print("- Требуется разгадать древнюю загадку.")

