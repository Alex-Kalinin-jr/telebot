from collections import defaultdict
from pydantic import BaseModel, types, ConfigDict, validator, Field, conlist, field_validator, ValidationInfo
from pprint import pprint
import json
import time
import random

from characters import NPC, Enemy
from db.database import DB, Dialog
from world_map_class import Location
from quests import quest_manager


START_LOCATION = "location_1"


class GameOverError(Exception):
    pass


class Protagonist:
    def __init__(self, name: str, location: Location):
        self.name: str = name
        self.hp: int = 10
        self.level = 1
        self.found_artifacts = set()
        self.inventory = defaultdict(int)
        self.inventory["pocket dust"] += 1
        self.current_location = location
        self.current_quests = []

    def get_current_stats(self):
        return (self.hp, self.level)


    def take(self, item: str):
        """Подобрать инвентарь к себе в сумку"""
        self.inventory[item] += 1

    def get_inventory(self):
        return self.inventory

    def get_current_location(self):
        return self.current_location

    def get_current_quests(self):
        return self.current_quests

    def add_new_quest(self, quest_type, quest_id):
        quest = quest_manager(quest_type, quest_id)
        self.current_quests.append(quest)
        return quest

    def remove_completed_quests(self):
        # удаляет все завершенные квесты и забирает награду за них
        completed_quests = []

        for quest in self.current_quests:
            if quest.is_completed:
                completed_quests.append(quest)

        for completed_quest in completed_quests:
            inventory = completed_quest.pick_up_winnings()
            self.take(inventory)
            self.current_quests.remove(completed_quest)

    def check_win_condition(self):
        return len(self.found_artifacts) == 4

    def check_current_arts_count(self):
        return len(self.found_artifacts)

    def attack(self, enemy: Enemy):
        """Сражение с врагом"""
        while True:
            time.sleep(1)
            player_roll = random.randint(1, 6)
            enemy_roll = random.randint(1, 6)
            print(f"{player_roll} - {enemy_roll}")

            player_total = player_roll + self.level
            enemy_total = enemy_roll + enemy.level

            if player_total > enemy_total:
                self.advance_level()
                artifact = enemy.drop_artifact()
                if artifact:
                    self.found_artifacts.add(artifact)
                return True                             # "Вы выиграли сражение!"
            if player_total < enemy_total:
                self.take_hit(random.randint(1, 3))
                return False                            # Вы проиграли сражение!

    def run_away(self, enemy: Enemy):
        chance_to_escape = self.level / enemy.level if enemy.level != 0 else 0.5
        n = random.random()
        if n < chance_to_escape:
            return True                 # Вы успешно убежали!
        return False                    # Убежать не удалось, сражайтесь!

    def take_hit(self, value=1):
        """Получить удар"""
        self.hp -= value
        if self.hp <= 0:
            raise GameOverError("You died")

    def heal(self, value=1):
        """Лечиться"""
        if "Зелье" in self.inventory and self.inventory["Зелье"] > 0 and self.hp < 10:
            self.hp += value
            self.inventory["potion"] -= 1
            return True
        return False

    def advance_level(self, value: int = 1):
        """Изменения уровня силы"""
        self.level += value

    def go(self, location: Location):
        """Сделать ход к следующей локации"""
        self.current_location = location
        # print(f"Вы выбрали переход в {self.current_location.name}.")

    def whereami(self):
        """Текущее описание локации"""
        return f"Вы находитесь на локации {self.current_location.name}. {self.current_location.description}"

    def give(self, npc: NPC, item: str):
        """Отдать инвентарь"""
        self.inventory[item] -= 1
        if self.inventory[item] == 0:
            del self.inventory[item]
        npc.receive(item)


if __name__ == "__main__":
    db = DB()
    npc = NPC(db.get_npc("1"))
    player = Protagonist("Oleg", 1, Location(START_LOCATION))
    # player.talk_to(npc)
    # enemy = Enemy(characters[25])
    # player.interact_with_enemy(enemy)
    player.interact_with_main_menu()




















    # def attack(self, enemy: Enemy):
    #     """Сражение с врагом"""
    #     while True:
    #         print("Идет сражение...")
    #         time.sleep(1)
    #         player_roll = random.randint(1, 6)
    #         enemy_roll = random.randint(1, 6)
    #
    #         player_total = player_roll + self.level
    #         enemy_total = enemy_roll + enemy.level
    #
    #         if player_total > enemy_total:
    #             print("Вы выиграли сражение!")
    #             return True
    #         if player_total < enemy_total:
    #             print("Вы проиграли сражение!")
    #             self.take_hit(random.randint(1, 3))
    #             return False
    #
    #         print("Ничья! Наступил следующий раунд.")
    #
    # def talk_to(self, npc: NPC):
    #     """Беседа с неигровым персонажем"""
    #     message = npc.get_start_messages()
    #     if message is None:
    #         return
    #     ind_message = message.ident
    #     print(f"\033[1m\033[32m{npc.name}: \033[0m{message.npc}")
    #
    #     while True:
    #         next_messages: list[Dialog] = npc.get_next_messages(ind_message)
    #         if not next_messages or len(next_messages) == 0:
    #             break
    #         for idx, msg in enumerate(next_messages, start=1):
    #             print(f"\t{idx}. {msg.user}")
    #         user_input = input("\tВыберете фразу (введите номер): ")
    #
    #         try:
    #             selected_idx = int(user_input)
    #             if 1 <= selected_idx <= len(next_messages):
    #                 ind_message = next_messages[selected_idx - 1].ident
    #             else:
    #                 print("\t\033[31mНекорректный ввод. Пожалуйста, выберите правильный номер.\033[0m")
    #                 continue
    #         except ValueError:
    #             print("\t\033[31mНекорректный ввод. Пожалуйста, введите число.\033[0m")
    #             continue
    #
    #         message = npc.get_messages(ind_message)
    #         if not message:
    #             break
    #         print(f"\033[1m\033[31m{self.name}: \033[0m{message.user}")
    #         print(f"\033[1m\033[32m{npc.name}: \033[0m{message.npc}")
    #
    # def interact_with_main_menu(self):
    #     while True:
    #         self.show_main_menu()
    #         choice = input("Выберите опцию (0-5): ")
    #
    #         if choice == '0':
    #             print("Выход из игры. До новых приключений!")
    #             break
    #         elif choice == '1':
    #             self.interact_with_npc()
    #         elif choice == '2':
    #             self.interact_with_enemy()
    #         elif choice == '3':
    #             self.change_location()
    #         elif choice == '4':
    #             self.interact_with_inventory_and_potions()
    #         elif choice == '5':
    #             self.whereami()
    #         else:
    #             print("\033[31mНекорректный ввод. Пожалуйста, выберите опцию от 1 до 5.\033[0m")
    #
    # def choose_from_list(self, items, item_type):
    #     while True:
    #         self.show_list(items, item_type)
    #         choice = input(f"Выберите {item_type} для взаимодействия (0-{len(items)}): ")
    #
    #         if choice == '0':
    #             print(f"Выход из меню {item_type}.")
    #             return None
    #
    #         try:
    #             choice_index = int(choice) - 1
    #             if 0 <= choice_index < len(items):
    #                 return items[choice_index]
    #             else:
    #                 print(f"\033[31mПожалуйста, выберите корректный номер {item_type}.\033[0m")
    #         except ValueError:
    #             print(f"\033[31mПожалуйста, введите число или '0' для возврата в основное меню.\033[0m")
    #
    # def interact_with_npc(self):
    #     npc = self.choose_from_list(self.current_location.get_npcs(), "персонажа")
    #     if npc is not None:
    #         self.interact_with_npc_menu(npc)
    #
    # def interact_with_enemy(self):
    #     enemy = self.choose_from_list(self.current_location.get_enemies(), "врага")
    #     if enemy is not None:
    #         self.interact_with_enemy_menu(enemy)
    #
    # def change_location(self):
    #     location = self.choose_from_list(self.current_location.get_linked_locations(), "локацию")
    #     if location is not None:
    #         self.go(location)
    #
    # def interact_with_inventory_and_potions(self):
    #     pass
    #
    # def interact_with_npc_menu(self, npc: NPC):
    #     while True:
    #         self.show_npc_menu()
    #         ind_cmd = input("\tВыберите действие (0-2): ")
    #         if ind_cmd == "0":
    #             print("Выход из меню взаимодействия с персонажем.")
    #             break
    #         elif ind_cmd == "1":
    #             self.talk_to(npc)
    #             break
    #         elif ind_cmd == "2":
    #             break
    #         print("\tНекорректный ввод. Пожалуйста, выберите правильный номер.")
    #
    # def interact_with_enemy_menu(self, enemy: Enemy):
    #     """Взаимодействие с врагом"""
    #     commands = ["Сразиться", "Бежать"]
    #     for ind, cmd_name in enumerate(commands, start=1):
    #         print(f"\t{ind}. {cmd_name}")
    #     while True:
    #         ind_cmd = input("\tВыберите действие: ")
    #         if ind_cmd == "1":
    #             self.attack(enemy)
    #             break
    #         elif ind_cmd == "2":
    #             self.run_away(enemy)
    #             break
    #         else:
    #             print("\tНекорректный ввод. Пожалуйста, выберите правильный номер.")
    #         break
 # def show_main_menu(self):
 #        print("===== Главное меню =====")
 #        print("\t0. Выйти из игры")
 #        print("\t1. Персонажи локации")
 #        print("\t2. Враги локации")
 #        print("\t3. Переход на соседние локации")
 #        print("\t4. Инвентарь и зелья")
 #        print("\t5. Описание текущейлокации локации")
 #
 #    def show_list(self, items, item_type):
 #        print(f"===== Список {item_type} локации =====")
 #        print(f"\t0. Вернуться в главное меню")
 #        for i, item in enumerate(items, start=1):
 #            print(f"\t{i}. {item.name} - {item.description}")
 #
 #    # def show_npc_list(self, npcs: list[NPC]):
 #    #     print("===== Список персонажей локации =====")
 #    #     print(f"\t0. Вернуться в главное меню")
 #    #     for i, npc in enumerate(npcs, start=1):
 #    #         print(f"\t{i}. {npc.name} - {npc.description}")
 #    #
 #    # def show_enemy_list(self, enemies: list[Enemy]):
 #    #     print("===== Список врагов локации =====")
 #    #     print(f"\t0. Вернуться в главное меню")
 #    #     for i, enemy in enumerate(enemies, start=1):
 #    #         print(f"\t{i}. {enemy.name} - {enemy.description}")
 #    #
 #    # def show_location_menu(self, linked_locations: list[Location]):
 #    #     print("===== Меню списка доступных локаций =====")
 #    #     print(f"\t0. Вернуться в главное меню")
 #    #     for i, location in enumerate(linked_locations, start=1):
 #    #         print(f"\t{i}. {location}")
 #
 #    def show_npc_menu(self):
 #        print("===== Меню взаимодействия с персонажем =====")
 #        print("\t0. Вернуться в главное меню")
 #        print("\t1. Поговорить")
 #        print("\t2. Торговать")
 #
 #    def show_enemy_menu(self):
 #        print("===== Меню взаимодействия с врагом =====")
 #        print("\t0. Вернуться в главное меню")
 #        print("\t1. Сразиться")
 #        print("\t2. Убежать")

