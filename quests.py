from db.requests import DB
from pprint import pprint


class SearchArtifactQuest:
    def __init__(self, ident, title, desc, reward, messages):
        self.id = ident
        self.title = title
        self.desc = desc
        self.reward = reward
        self.messages = messages

    def start(self):
        for message in self.messages:
            print(message)

        print("Вы успешно нашли и добавили магический артефакт в свой инвентарь.")
        return self.reward


class RiddleQuest:
    def __init__(self, ident, title, desc, reward, messages):
        self.id = ident
        self.title = title
        self.desc = desc
        self.reward = reward
        self.riddle = messages[0]
        self.correct_answer = messages[1].capitalize()
        self.answer_attempts = 3

    def start(self):
        print(self.desc)
        print(self.riddle)
        answer_attempts = self.answer_attempts
        while answer_attempts > 0:
            user_answer = input("Ваш ответ: ").capitalize()

            if user_answer == self.correct_answer:
                print("Верно! Вы разгадали загадку.")
                return self.reward
            else:
                answer_attempts -= 1
                if answer_attempts > 0:
                    print(f"Неверно. У вас осталось {answer_attempts} {'попытки' if answer_attempts > 1 else 'попытка'}.")
                    print("Подумайте еще раз.")
                else:
                    print("Увы, вы исчерпали все попытки. Попробуйте следующий раз.")


def quest_manager(quest: dict):
    quest_obj = None
    if quest['type'] == 'search_artifact':
        quest_obj = SearchArtifactQuest(
            ident=quest['id'],
            title=quest['title'],
            desc=quest['desc'],
            reward=quest['reward'],
            messages=quest['messages']
        )
    elif quest['type'] == 'riddle':
        quest_obj = RiddleQuest(
            ident=quest['id'],
            title=quest['title'],
            desc=quest['desc'],
            reward=quest['reward'],
            messages=quest['messages']
        )
    if quest_obj:
        quest_obj.start()


if __name__ == '__main__':
    db = DB()
    # pprint(db.get_dialogs())
    quests = db.get_quests()
    for quest in quests:
        quest_manager(quest)
        print("*"*88)

    # quest = SearchArtifactQuest(
    #     1,
    #     "Поиск магического артефакта",
    #     "Описание квеста",
    #     "Магический артефакт",
    #     [
    #         "Вы отправились исследовать древние руины в поисках магического артефакта...",
    #         "Вы находите старинный артефакт, мерцающий магией!",
    #     ]
    # )
    # artifact = quest.start()
    # # print("artifact = ", artifact)
    #
    # quest_riddle = RiddleQuest(
    #     1,
    #     "Поиск магического артефакта",
    #     "Описание - Вы встречаете древнего мудреца, который предлагает вам загадку:",
    #     "Ваша награда - Магический артефакт",
    #     [
    #         "Без оконца, начала и середины, у меня есть ключи, но замков нет. Что это?",
    #         "Река"
    #     ]
    # )
    # artifact_riddle = quest_riddle.start()
    # print("artifact = ", artifact_riddle)

