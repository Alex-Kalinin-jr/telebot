from collections import defaultdict
from pydantic import BaseModel, types, ConfigDict, validator, Field, conlist, field_validator, ValidationInfo
from pprint import pprint
import json
import random

from characters import NPC, Enemy
from db.requests import DB, Dialog


class Protagonist:
    def __init__(self, name: str, ident: str):
        self.id = ident
        self.name: str = name
        self.hp: int = 10
        self.level = 1
        self.strength, self.craft = (1, 1)
        self.inventory = defaultdict(int)
        self.inventory["pocket dust"] += 1

    def interact_with_npc(self, npc: NPC):
        commands = ["Поговорить", "Торговать"]
        for ind, cmd_name in enumerate(commands, start=1):
            print(f"\t{ind}. {cmd_name}")
        while True:
            ind_cmd = input("\tВыберите действие: ")
            if ind_cmd == "1":
                self.talk_to(npc)
                break
            elif ind_cmd == "2":

                break
            else:
                print("\tНекорректный ввод. Пожалуйста, выберите правильный номер.")
            break

    def interact_with_enemy(self, enemy: Enemy):
        """Взаимодействие с врагом"""
        commands = ["Сразиться", "Бежать"]
        for ind, cmd_name in enumerate(commands, start=1):
            print(f"\t{ind}. {cmd_name}")
        while True:
            ind_cmd = input("\tВыберите действие: ")
            if ind_cmd == "1":
                self.attack(enemy)
                break
            elif ind_cmd == "2":
                self.run_away(enemy)
                break
            else:
                print("\tНекорректный ввод. Пожалуйста, выберите правильный номер.")
            break

    def talk_to(self, npc: NPC):
        """Беседа с неигровым персонажем"""
        message = npc.get_start_messages()
        if message is None:
            return
        ind_message = message.ident
        print(f"\033[1m\033[32m{npc.name}: \033[0m{message.npc}")

        while True:
            next_messages: list[Dialog] = npc.get_next_messages(ind_message)
            if not next_messages or len(next_messages) == 0:
                break
            for idx, msg in enumerate(next_messages, start=1):
                print(f"\t{idx}. {msg.user}")
            user_input = input("\tВыберете фразу (введите номер): ")

            try:
                selected_idx = int(user_input)
                if 1 <= selected_idx <= len(next_messages):
                    ind_message = next_messages[selected_idx - 1].ident
                else:
                    print("\tНекорректный ввод. Пожалуйста, выберите правильный номер.")
                    continue
            except ValueError:
                print("\tНекорректный ввод. Пожалуйста, введите число.")
                continue

            message = npc.get_messages(ind_message)
            if not message:
                break
            print(f"\033[1m\033[31m{self.name}: \033[0m{message.user}")
            print(f"\033[1m\033[32m{npc.name}: \033[0m{message.npc}")

    def attack(self, enemy: Enemy):
        """Сражение с врагом"""
        while True:
            player_roll = random.randint(1, 6)
            enemy_roll = random.randint(1, 6)

            player_total = player_roll + self.level
            enemy_total = enemy_roll + enemy.level

            if player_total > enemy_total:
                print("Вы победили сражение")
                return True
            if player_total < enemy_total:
                print("Вы проиграли сражение")
                self.take_hit(random.randint(1, 3))
                return False

            print("Ничья! Наступил следующий раунд.")

    def run_away(self, enemy: Enemy):
        chance_to_escape = self.level / enemy.level
        n = random.random()
        if n < chance_to_escape:
            print("Вы успешно убежали!")
            return True
        else:
            print("Убежать не удалось, сражайтесь!")
            self.attack(enemy)
            return False

    def take_hit(self, value=1):
        """Получить удар"""
        self.hp -= value
        if self.hp <= 0:
            raise Exception("You died")

    def heal(self, value=1):
        """Лечиться"""
        self.strength, self.craft = (1, 1)
        self.hp += 1

    def advance_strength(self, value: int = 1):
        """Изменения уровня силы"""
        self.strength += value

    def advance_craft(self, value: int = 1):
        """Изменения уровня ремесла (навыков)"""
        self.craft += value

    # def go(self, direction: Direction):
    #     """Сделать ход к следующей локации"""
    #     pass

    def whereami(self):
        """Текущее описание локации"""
        pass

    def take(self, item: str):
        """Подобрать инвентарь к себе в сумку"""
        self.inventory[item] += 1

    def give(self, npc: NPC, item: str):
        """Отдать инвентарь"""
        self.inventory[item] -= 1
        if self.inventory[item] == 0:
            del self.inventory[item]
        npc.receive(item)


if __name__ == "__main__":
    db = DB()
    characters = db.get_characters()
    npc = NPC(characters[4])
    player = Protagonist("Oleg", 1)
    # player.talk_to(npc)
    enemy = Enemy(characters[25])
    player.interact_with_enemy(enemy)
