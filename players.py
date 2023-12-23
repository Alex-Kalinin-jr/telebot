from collections import defaultdict
from pydantic import BaseModel, types, ConfigDict, validator, Field, conlist, field_validator, ValidationInfo
from pprint import pprint
import json
import time
import random

from characters import NPC, Enemy
from db.database import DB, Dialog
from world_map_class import Location
from quests import quest_manager, QuestInterface


START_LOCATION = "location_1"


class GameOverError(Exception):
    """Exception raised when the player's health points become less than or equal to 0."""
    pass


class Protagonist:
    """
    Represents the player in the game.
    """
    def __init__(self, name: str, location: Location):
        """
        Initialize the player.
        :param name: The name of the player.
        :type name: str
        :param location: The starting location of the player.
        :type location: Location
        """
        self.name: str = name
        self.hp: int = 10
        self.level = 1
        self.found_artifacts = set()
        self.inventory = defaultdict(int)
        self.inventory["pocket dust"] += 1
        self.current_location: Location = location
        self.current_quests: list[QuestInterface] = []


    def get_current_stats(self):
        return (self.hp, self.level)

    def take(self, item: str) -> None:
        """
        Increment the count of the given item in the inventory.
        :param item: The item to be added to the inventory.
        :type item: str
        :return: None
        """
        self.inventory[item] += 1

    def get_inventory(self) -> dict:
        """
        Get the inventory dictionary.
        :return: A dictionary representing the inventory.
        :rtype: dict
        """
        return self.inventory

    def get_current_location(self) -> Location:
        """
        Returns the current location.
        :return: The current location.
        :rtype: Location
        """
        return self.current_location

    def get_current_quests(self) -> list[QuestInterface]:
        """
        Returns the list of current quests.
        :return: A list of QuestInterface objects representing the current quests.
        :rtype: list[QuestInterface]
        """
        return self.current_quests

    def add_new_quest(self, quest_type: str, quest_id: str) -> QuestInterface:
        """
        Adds a new quest to the current quests list.
        :param quest_type: The type of the quest.
        :type quest_type: str
        :param quest_id: The ID of the quest.
        :type quest_id: str
        :return: The newly created quest object.
        :rtype: QuestInterface
        """
        quest = quest_manager(quest_type, quest_id)
        self.current_quests.append(quest)
        return quest

    def remove_completed_quests(self) -> None:
        """
        Removes completed quests from the current quests list.
        :return: None
        """
        completed_quests = []

        for quest in self.current_quests:
            if quest.is_completed:
                completed_quests.append(quest)

        for completed_quest in completed_quests:
            inventory = completed_quest.pick_up_winnings()
            self.take(inventory)
            self.current_quests.remove(completed_quest)

    def check_win_condition(self) -> bool:
        """
        Checks if the player has won the game.
        :return: True if the player has won the game, False otherwise.
        :rtype: bool
        """
        return len(self.found_artifacts) == 4

    def check_current_arts_count(self) -> int:
        """
        Returns the number of artifacts found by the player.
        :return: The number of artifacts found by the player.
        :rtype: int
        """
        return len(self.found_artifacts)

    def attack(self, enemy: Enemy) -> bool:
        """
        Simulates the player's attack against an enemy.
        :param enemy: The enemy to attack.
        :type enemy: Enemy
        :return: True if the player wins, False if the player loses.
        :rtype: bool
        """
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
                return True
            if player_total < enemy_total:
                self.take_hit(random.randint(1, 3))
                return False

    def run_away(self, enemy: Enemy) -> bool:
        """
        Simulates the player running away from an enemy.
        :param enemy: The enemy to run away from.
        :type enemy: Enemy
        :return: True if the player successfully ran away, False otherwise.
        :rtype: bool
        """
        chance_to_escape = self.level / enemy.level if enemy.level != 0 else 0.5
        n = random.random()
        if n < chance_to_escape:
            return True
        return False

    def take_hit(self, value=1) -> None:
        """
        Decreases the player's health points by the specified value.
        :param value: The amount by which the player's health points will be decreased. Default is 1.
        :type value: int
        :return: None
        :raise: GameOverError if the player's health points become less than or equal to 0.
        """
        self.hp -= value
        if self.hp <= 0:
            raise GameOverError("You died")

    def heal(self, value=1) -> bool:
        """
        Increases the player's health points by the specified value.
        :param value: The amount by which the player's health points will be increased. Default is 1.
        :type value: int
        :return: True if the player successfully healed, False otherwise.
        """
        if "Зелье" in self.inventory and self.inventory["Зелье"] > 0 and self.hp < 10:
            self.hp += value
            self.inventory["potion"] -= 1
            return True
        return False

    def advance_level(self, value: int = 1) -> None:
        """
        Increases the player's level by the specified value.
        :param value: The amount by which the player's level will be increased. Default is 1.
        :type value: int
        :return: None
        """
        self.level += value

    def go(self, location: Location) -> None:
        """
        Moves the player to the specified location.
        :param location: The location to move to.
        :type location: Location
        :return: None
        """
        self.current_location = location

    def whereami(self) -> str:
        """
        Returns the name of the current location.
        :return: The name of the current location.
        :rtype: str
        """
        return f"Вы находитесь на локации {self.current_location.name}. {self.current_location.description}"

    def give(self, npc: NPC, item: str) -> None:
        """
        Gives an item to the specified NPC.
        :param npc: The NPC to give the item to.
        :type npc: NPC
        :param item: The item to give.
        :type item: str
        :return: None
        """
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
