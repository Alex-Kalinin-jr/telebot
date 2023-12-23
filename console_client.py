import time

from players import Protagonist
from characters import NPC, Enemy
from world_map_class import Location
from quests import SecretPotionQuest, AncientRiddleQuest, QuestInterface
from db.database import Dialog


START_LOCATION = "location_1"


class Game:
    """The console client for the game."""
    def __init__(self, player: Protagonist):
        """
        Initialize the game.
        :param player: The player of the game.
        :type player: Protagonist
        """
        self.player = player

    def handle_npc(self, npc: NPC) -> None:
        """
        Взаимодействие с NPC
        :param npc: NPC
        :type npc: NPC
        :return: None
        """
        while True:
            self.show_npc_menu()
            ind_cmd = input("\tВыберите действие (0-2): ")
            if ind_cmd == "0":
                # print("Выход из меню взаимодействия с персонажем.")
                break
            elif ind_cmd == "1":
                # self.talk_to(npc)
                break
            elif ind_cmd == "2":
                break
            print("\tНекорректный ввод. Пожалуйста, выберите правильный номер.")

    def handle_enemy(self, enemy: Enemy) -> None:
        """
        Handles the interaction with an enemy.
        :param enemy: Enemy
        :type enemy: Enemy
        :return: None
        """
        commands = ["Сразиться", "Бежать"]
        for ind, cmd_name in enumerate(commands, start=1):
            print(f"\t{ind}. {cmd_name}")
        while True:
            ind_cmd = input("\tВыберите действие: ")
            if ind_cmd == "1":
                self.player.attack(enemy)
                break
            elif ind_cmd == "2":
                self.player.run_away(enemy)
                break
            else:
                print("\tНекорректный ввод. Пожалуйста, выберите правильный номер.")
            break

    def exec(self) -> None:
        """
        Start the game.
        :return: None
        """
        while True:
            self.show_main_menu()
            choice = input("Выберите опцию (0-8): ")

            if choice == '0':
                print("Выход из игры. До новых приключений!")
                break
            elif choice == '1':
                self.go_to_npcs_menu()
            elif choice == '2':
                self.go_to_enemies_menu()
            elif choice == '3':
                self.go_to_location_menu()
            elif choice == '4':
                self.go_to_inventory_menu()
            elif choice == '5':
                print(self.player.whereami())
            elif choice == '6':
                print(self.go_to_quests_menu())
            elif choice == '7':
                self.show_player_profile()
            elif choice == '8':
                self.heal()
            else:
                print("\033[31mНекорректный ввод. Пожалуйста, выберите опцию от 0 до 8.\033[0m")

            if self.player.check_win_condition():
                print("Поздравляю! Вы успешно собрали все необходимые артефакты и спасли Арканию.")
                break

    def go_to_npcs_menu(self) -> None:
        """
        Go to the NPCs menu.
        :return: None
        """
        npcs = self.player.current_location.get_full_npcs_data()
        while True:
            self.show_menu(npcs, "Список персонажей на текущей локации")
            choice = input(f"Выберите персонажа для взаимодействия (0-{len(npcs)}): ")

            if choice == '0':
                return None

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index <= len(npcs):
                    self.go_to_npc_menu(npcs[choice_index])
                else:
                    print(f"\033[31mПожалуйста, выберите корректный номер.\033[0m")
            except ValueError:
                print(f"\033[31mПожалуйста, введите число или '0' для возврата в основное меню.\033[0m")

    def go_to_enemies_menu(self) -> None:
        """
        Go to the enemies menu.
        :return: None
        """        
        enemies = self.player.current_location.get_full_enemies_data()
        while True:
            self.show_menu(enemies, "Список врагов на текущей локации")
            choice = input(f"Выберите врага для взаимодействия (0-{len(enemies)}): ")

            if choice == '0':
                return None

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index <= len(enemies):
                    self.go_to_enemy_menu(enemies[choice_index])
                else:
                    print(f"\033[31mПожалуйста, выберите корректный номер.\033[0m")
            except ValueError:
                print(f"\033[31mПожалуйста, введите число или '0' для возврата в основное меню.\033[0m")

    def go_to_location_menu(self) -> None:
        """
        Go to the location menu.
        :return: None
        """
        locations = self.player.get_current_location().get_linked_locations()
        while True:
            self.show_menu(locations, "Список соседних локаций")
            choice = input(f"Выберите локацию для перехода (0-{len(locations)}): ")

            if choice == '0':
                return None

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index <= len(locations):
                    self.player.go(Location(locations[choice_index]['id']))
                    print(f"Вы перешли на локацию '{locations[choice_index]['name']}'")
                    break
                else:
                    print(f"\033[31mПожалуйста, выберите корректный номер.\033[0m")
            except ValueError:
                print(f"\033[31mПожалуйста, введите число или '0' для возврата в основное меню.\033[0m")

    def go_to_inventory_menu(self) -> None:
        """
        Go to the inventory menu.
        :return: None
        """
        print(f"===== Список ваших инструментов =====")
        inventories = self.player.get_inventory()
        for i, (name, count) in enumerate(inventories.items(), start=1):
            print(f"\t{i}. {name} - {count} шт.")

    def go_to_quests_menu(self) -> None:
        """
        Go to the quests menu.
        :return: None
        """
        while True:
            quests = self.player.get_current_quests()
            self.show_quests(quests)
            choice = input(f"Выберите квест для выполнения (0-{len(quests)}): ")

            if choice == '0':
                return None

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index <= len(quests):
                    self.got_to_quest(quests[choice_index])
                else:
                    print(f"\033[31mПожалуйста, выберите корректный номер.\033[0m")
            except ValueError:
                print(f"\033[31mПожалуйста, введите число или '0' для возврата в основное меню.\033[0m")

    def go_to_npc_menu(self, npc_data: dict) -> None:
        """
        Go to the NPC menu.
        :param npc_data: NPC data
        :type npc_data: dict
        :return: None
        """
        npc = NPC(npc_data)
        while True:
            self.show_npc_menu()
            choice = input("Выберите опцию (0-2): ")

            if choice == '0':
                break
            elif choice == '1':
                self.talk_to(npc)
            elif choice == '2':
                quest_type, quest_id = npc.offer_quest()
                quest = self.player.add_new_quest(quest_type, quest_id)
                print(f"Получен квест '{quest.get_name()}'")
            else:
                print("\033[31mНекорректный ввод. Пожалуйста, выберите опцию от 0 до 2.\033[0m")

    def go_to_enemy_menu(self, enemy_data: dict) -> None:
        """
        Go to the enemy menu.
        :param enemy_data: Enemy data
        :type enemy_data: dict
        :return: None
        """
        enemy = Enemy(enemy_data)
        while True:
            self.show_enemy_menu()
            choice = input("Выберите опцию (0-2): ")

            if choice == '0':
                break
            elif choice == '1':
                self.player_attack(enemy)
            elif choice == '2':
                self.player_run_away(enemy)
            else:
                print("\033[31mНекорректный ввод. Пожалуйста, выберите опцию от 0 до 2.\033[0m")

    def player_attack(self, enemy: Enemy) -> None:
        """
        Handles the interaction with an enemy.
        :param enemy: Enemy
        :type enemy: Enemy
        :return: None
        """
        if self.player.attack(enemy):
            print("Вы выиграли бой!")
        else:
            print("Вы проиграли бой!")

    def player_run_away(self, enemy: Enemy) -> None:
        """
        Handles the interaction with an enemy.
        :param enemy: Enemy
        :type enemy: Enemy
        :return: None
        """
        if self.player.run_away(enemy):
            print("Вы избежали боя!")
        else:
            print("Вы не смогли убежать")
            self.player_attack(enemy)

    def show_player_profile(self) -> None:
        """
        Show the player profile.
        :return: None
        """
        print("===== Ваш профиль =====")
        print(f"Имя: {self.player.name}")
        print(f"Здоровье: {self.player.hp}")
        print(f"Уровень: {self.player.level}")
        print("Инвентарь:")
        for item, count in self.player.inventory.items():
            print(f"\t- {item}: {count}")

    def heal(self) -> None:
        """
        Heals the player.
        :return: None
        """
        self.player.heal()

    def got_to_quest(self, quest: QuestInterface) -> None:
        """
        Handles the interaction with a quest.
        :param quest: Quest
        :type quest: Quest
        :return: None
        """
        print(quest.start_quest())
        print(quest.get_task())
        result = ""
        if isinstance(quest, SecretPotionQuest):
            print("Выполняем квест...")
            time.sleep(1)
            res = quest.perform()
            if res:
                result = f"Вы обнаружили {quest.artifact_name}!"
            else:
                result = f"К сожалению, {quest.artifact_name} не было найдено. Продолжайте поиски!"
        else:
            answer = input("Напишите ответ: ")
            res = quest.perform(answer)
            if res:
                result = "Верно! Загадка разгадана."
            else:
                result = "Неверный ответ. Продолжайте разгадывать загадку!"
        print(result)
        self.player.remove_completed_quests()

    def talk_to(self, npc: NPC) -> None:
        """
        Handles the interaction with an NPC.
        :param npc: NPC
        :type npc: NPC
        :return: None
        """
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
                    print("\t\033[31mНекорректный ввод. Пожалуйста, выберите правильный номер.\033[0m")
                    continue
            except ValueError:
                print("\t\033[31mНекорректный ввод. Пожалуйста, введите число.\033[0m")
                continue

            message = npc.get_messages(ind_message)
            if not message:
                break
            print(f"\033[1m\033[31m{self.player.name}: \033[0m{message.user}")
            print(f"\033[1m\033[32m{npc.name}: \033[0m{message.npc}")

    def show_menu(self, items: list[dict], title: str) -> None:
        """
        Shows the menu.
        :param items: list
        :type items: list
        :param title: str
        :type title: str
        :return: None
        """
        print(f"===== {title} =====")
        print(f"\t0. Вернуться в главное меню")
        for i, item in enumerate(items, start=1):
            print(f"\t{i}. {item.get('name', '')} - {item.get('description', '')}")

    def show_main_menu(self) -> None:
        """
        Shows the main menu.
        :return: None
        """
        print("===== Главное меню =====")
        print("\t0. Выйти из игры")
        print("\t1. Персонажи локации")
        print("\t2. Враги локации")
        print("\t3. Переход на соседние локации")
        print("\t4. Инвентарь")
        print("\t5. Описание текущей локации локации")
        print("\t6. Активные квесты")
        print("\t7. Показать профиль пользователя")
        print("\t8. Лечиться")

    def show_npc_menu(self) -> None:
        """
        Shows the NPC menu.
        :return: None
        """
        print("===== Меню взаимодействия с персонажем =====")
        print("\t0. Вернуться в меню персонажей")
        print("\t1. Поговорить")
        print("\t2. Получить квест")

    def show_enemy_menu(self) -> None:
        """
        Shows the enemy menu.
        :return: None
        """
        print("===== Меню взаимодействия с врагом =====")
        print("\t0. Вернуться в меню персонажей")
        print("\t1. Сразиться")
        print("\t2. Убежать")

    def show_quests(self, quests: list[QuestInterface]) -> None:
        """
        Shows the quests.
        :param quests: list
        :type quests: list
        :return: None
        """
        print("===== Меню квестов =====")
        print("\t0. Вернуться в основное меню")
        for i, quest in enumerate(quests, start=1):
            print(f"\t{i}. {quest.get_name()}")


if __name__ == "__main__":
    location = Location(START_LOCATION)
    player = Protagonist("tesst user", location)
    game = Game(player)
    game.exec()
