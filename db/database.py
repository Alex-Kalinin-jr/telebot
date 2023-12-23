import json
from pydantic import BaseModel, types, ConfigDict, validator, Field, conlist, field_validator, ValidationInfo
from pprint import pprint
import sqlite3


FILE_CHARACTERS = './db/npcs.json'
FILE_ENEMIES = './db/enemies.json'
FILE_DIALOGS = './db/dialogs.json'
FILE_SEARCH_QUESTS = './db/search_quests.json'
FILE_RIDDLE_QUESTS = './db/riddle_quests.json'
FILE_LOCATIONS = './db/locations.json'


class Dialog(BaseModel):
    ident: str
    user: str
    npc: str
    responses: list[str]


class DB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """
        Initializes the class instance.
        """
        self.dialog_messages = {}
        self._init_dialogs()
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()

    def get_npcs(self):
        """
        Read the characters data from a JSON file and return it.

        :return: The characters data.
        """
        try:
            with open(FILE_CHARACTERS) as fp:
                data = json.load(fp)
                return data
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def get_npc(self, ident: str):
        """
        Retrieves a non-player character (NPC) based on its identifier.

        Args:
            ident (str): The identifier of the NPC.

        Returns:
            dict: The NPC data as a dictionary if found, None otherwise.
        """
        try:
            with open(FILE_CHARACTERS) as fp:
                data = json.load(fp)
                return data.get(ident)
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def get_enemies(self):
        """
        Reads the enemies data from the specified file and returns it.

        Parameters:
            self (object): The instance of the class.

        Returns:
            dict: The data containing the enemies.
        """
        try:
            with open(FILE_ENEMIES) as fp:
                data = json.load(fp)
                return data
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def get_enemy(self, ident: str):
        """
        Get the enemy data for the given identifier.

        Parameters:
            ident (str): The identifier of the enemy.

        Returns:
            dict or None: The enemy data if found, None otherwise.
        """
        try:
            with open(FILE_ENEMIES) as fp:
                data = json.load(fp)
                return data.get(ident)
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def get_dialogs(self):
        """
        Get the list of dialog messages.

        Returns:
            list: The list of dialog messages.
        """
        return self.dialog_messages

    def get_search_quests(self):
        """
        Read the contents of the search quests file and return the data as a dictionary.

        Returns:
            dict: The data read from the search quests file.
        """
        try:
            with open(FILE_SEARCH_QUESTS) as fp:
                data = json.load(fp)
                return data
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def get_search_quest(self, ident: str):
        """
        Retrieves a search quest from the specified identifier.

        Parameters:
            ident (str): The identifier of the search quest.

        Returns:
            Any: The search quest associated with the identifier, or None if not found.
        """
        try:
            with open(FILE_SEARCH_QUESTS) as fp:
                data = json.load(fp)
                return data.get(ident)
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def get_riddle_quests(self):
        """
        Opens a file containing riddle quests and returns the data as a Python dictionary.

        Returns:
            dict: The riddle quests data.
        """
        try:
            with open(FILE_RIDDLE_QUESTS) as fp:
                data = json.load(fp)
                return data
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def get_riddle_quest(self, ident: str):
        """
        Retrieves a riddle quest from the JSON file based on the provided identifier.

        Parameters:
            ident (str): The identifier of the riddle quest.

        Returns:
            str: The riddle quest associated with the provided identifier.
        """
        try:
            with open(FILE_RIDDLE_QUESTS) as fp:
                data = json.load(fp)
                return data.get(ident)
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def get_locations(self) -> list[dict]:
        """
        Get the locations from the file.

        :return: A list of dictionaries representing the locations.
        :rtype: list[dict]
        """
        try:
            with open(FILE_LOCATIONS) as fp:
                data = json.load(fp)
                return data
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def get_location(self, key: str) -> dict:
        """
        Retrieves the location associated with the given key.

        Parameters:
            key (str): The key used to retrieve the location.

        Returns:
            dict: The location associated with the given key, or None if the key is not found.
        """
        try:
            with open(FILE_LOCATIONS) as fp:
                data = json.load(fp)
                return data.get(key)
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def _init_dialogs(self):
        """
        Initializes the dialogs by reading the data from the FILE_DIALOGS file
        and converting it to the appropriate format.
        """
        try:
            with open(FILE_DIALOGS) as fp:
                data = json.load(fp)
                self._convert_dialogs(data)
        except FileNotFoundError:
            print(f"Ошибка: Файл {FILE_DIALOGS} не найден.")

    def _convert_dialogs(self, dialogs_lst, prefix=''):
        """
        Converts a list of dialog dictionaries into a list of message identifiers.

        Args:
            dialogs_lst (list): A list of dialog dictionaries representing conversations.
            prefix (str, optional): A prefix to be added to the identifiers of the converted dialogs. Defaults to ''.

        Returns:
            list: A list of message identifiers representing the converted dialogs.
        """
        messages_ids = []
        for dialog in dialogs_lst:
            answers = dialog['next']
            answers_ids = []
            if 'id' in dialog:
                prefix = dialog['id']
            if answers:
                answers_ids = self._convert_dialogs(answers, prefix)
            ident = dialog.get('id') or f'{prefix}_{len(self.dialog_messages)}'
            self.dialog_messages[ident] = Dialog(
                ident=ident,
                user=dialog['user'],
                npc=dialog['npc'],
                responses=answers_ids
            )
            messages_ids.append(ident)

        return messages_ids

    def fill_data(self, path: str) -> dict:
        """
        Fill data from a file.

        Parameters:
            path (str): The path of the file to be opened.

        Returns:
            dict: The data loaded from the file.

        Raises:
            FileNotFoundError: If the file is not found.
        """
        dest = {}
        try:
            f = open(path, 'r')
            dest = json.load(f)
            f.close()
        except FileNotFoundError:
            print("File not found: .db/locations.json")
        finally:
            return dest


    def get_players(self):
        """
        Retrieves all players from the database.

        Returns:
            A list of tuples containing information about each player.
        """
        return self.cur.execute("SELECT * FROM users").fetchall()

    def create_user(self, nickname, password):
        """
        Create a new user with the given nickname and password.

        Parameters:
            nickname (str): The nickname of the user.
            password (str): The password of the user.

        Returns:
            None
        """
        self.cur.execute("INSERT INTO users(name, password, hp, level, location) VALUES(?, ?, ?, ?, ?)",
                        (nickname, password, 10, 100, 'location_1'))
        self.conn.commit()

    def create_tables(self):
        """
        Creates tables for users, user inventory, user artifacts, and user quests.
        """
        self.create_users_table()
        self.create_user_inventory_table()
        self.create_user_artifacts_table()
        self.create_user_quests_table()

    def create_users_table(self):
        """
        Creates a users table in the database if it does not already exist.

        Args:
            self: The current instance of the class.

        Returns:
            None
        """
        self.cur.execute('CREATE TABLE IF NOT EXISTS users(name TEXT PRIMARY KEY, password TEXT, hp INTEGER, level INTEGER, location TEXT)')
        self.conn.commit()

    def create_user_inventory_table(self):
        """
        Create the user inventory table if it does not already exist.

        This function executes an SQL statement to create a table named 'inventory' in the database.
        The table has three columns: 'user_name' of type TEXT, 'item' of type TEXT, and 'count' of type INTEGER.

        Parameters:
            None

        Returns:
            None
        """
        self.cur.execute('CREATE TABLE IF NOT EXISTS inventory(name TEXT, item TEXT, count INTEGER)')
        self.conn.commit()


    def create_user_artifacts_table(self):
        """
        Creates a user artifacts table in the database if it doesn't already exist.

        Parameters:
            None

        Returns:
            None
        """
        self.cur.execute('CREATE TABLE IF NOT EXISTS artifacts(name TEXT, artifact TEXT)')
        self.conn.commit()


    def create_user_quests_table(self):
        """
        Create a table to store user quests.

        This function executes a SQL query to create a table named 'quests' in the current
        database if it doesn't already exist. The table has two columns: 'user_name' of type
        TEXT and 'quest' of type TEXT. After executing the query, the changes are committed to
        the database.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        self.cur.execute('CREATE TABLE IF NOT EXISTS quests(name TEXT, quest TEXT)')
        self.conn.commit()


    def write_all_user_data(self, user):
        """
        Writes all user data.

        Parameters:
            user (User): The user object containing the data to be written.

        Returns:
            None
        """
        self.write_data_from_user(user)
        self.write_inventory_data(user)
        self.write_artifacts_data(user)
        self.write_quests_data(user)


    def load_all_user_data(self, user):
        """
        Load all user data.

        Parameters:
            user (User): The user whose data needs to be loaded.

        Returns:
            None
        """
        self.load_user_data(user)
        self.load_inventory_data(user)
        self.load_artifacts_data(user)
        self.load_quests_data(user)


    def load_user_data(self, user):
        """
        Loads user data from the database and updates the user object with the retrieved information.

        Args:
            user (User): The user object to load data for.

        Returns:
            None
        """
        import world_map_class as wmc
        data = self.cur.execute("SELECT * FROM users WHERE name = ?", (user.name,)).fetchall()
        user.hp = data[0][2]
        user.level = data[0][3]
        user.go(wmc.Location(data[0][4]))


    def write_data_from_user(self, user):
        """
        Updates the user's data in the database.

        Parameters:
            user (User): The user object containing the updated data.

        Returns:
            None
        """
        self.cur.execute("UPDATE users SET hp = ?, level = ?, location = ? WHERE name = ?",
                        (user.hp, user.level, user.current_location.id, user.name))
        self.conn.commit()


    def load_inventory_data(self, user):
        """
        Load inventory data for a user.

        Args:
            user (User): The user object for which to load the inventory data.

        Returns:
            None
        """
        data = self.cur.execute("SELECT * FROM inventory WHERE name = ?", (user.name,)).fetchall()
        for name, item, val in data:
            user.inventory[item] = val


    def write_inventory_data(self, user):
        """
        Writes the inventory data of a user to the database.

        Parameters:
            self (object): The object instance.
            user (User): The user object whose inventory data will be written.

        Returns:
            None
        """
        data = user.get_inventory()
        self.cur.execute("DELETE FROM inventory WHERE name = ?", (user.name,))
        for item, val in data.items():
            self.cur.execute("INSERT INTO inventory VALUES(?, ?, ?)", (user.name, item, val))
        self.conn.commit()


    def load_artifacts_data(self, user):
        """
        Load artifacts data for a user.

        Args:
            user (User): The user object whose artifacts data needs to be loaded.

        Returns:
            None
        """
        data = self.cur.execute("SELECT * FROM artifacts WHERE name = ?", (user.name,)).fetchall()
        for item in data:
            user.found_artifacts.add(item)


    def write_artifacts_data(self, user):
        """
        Deletes the user's existing artifacts data from the 'artifacts' table
        and inserts the new artifacts found by the user into the table.

        Parameters:
            user (User): The user object containing the user's information.

        Returns:
            None
        """
        self.cur.execute("DELETE FROM artifacts WHERE name = ?", (user.name,))
        for artifact in user.found_artifacts:
            self.cur.execute("INSERT INTO artifacts VALUES(?, ?)",
                            (user.name, artifact))
        self.conn.commit()


    def load_quests_data(self, user):
        """
        Load the quests data for a given user.

        Parameters:
            user (User): The user object for which to load the quests data.

        Returns:
            None
        """
        data = self.cur.execute("SELECT * FROM quests WHERE name = ?", (user.name,)).fetchall()
        for item in data:
            user.current_quests.append(item)


    def write_quests_data(self, user):
        """
        Deletes the quests data for a given user and inserts new quest data.

        Parameters:
            user (User): The user for whom the quests data needs to be updated.

        Returns:
            None
        """
        self.cur.execute("DELETE FROM quests WHERE name = ?", (user.name,))
        for quest in user.current_quests:
            self.cur.execute("INSERT INTO quests VALUES(?, ?)", (user.name, quest))
        self.conn.commit()


    def check_nickname_existence(self, nick):
        """
        Check if a nickname exists in the "users" table.

        Args:
            nick (str): The nickname to check.

        Returns:
            bool: True if the nickname exists, False otherwise.
        """
        return self.cur.execute("SELECT * FROM users WHERE name = ?", (nick,)).fetchall() == []




    def check_login_and_password(self, nickname, password):
        """
        Check if the given nickname and password match any user in the database.

        :param nickname: The nickname of the user to check.
        :type nickname: str
        :param password: The password of the user to check.
        :type password: str
        :return: True if the nickname and password match a user in the database,
        False otherwise.
        :rtype: bool
        """
        return self.cur.execute("SELECT * FROM users WHERE name = ? AND password = ?",
                                        (nickname, password)).fetchall() != []



if __name__ == "__main__":
    db = DB()
    pprint(db.get_npcs())
    # pprint(db.get_dialogs())
    # pprint(db.get_quests())
    # pprint(db.get_locations())
    # pprint(db.get_location("location_3"))
    # pprint(db.get_search_quests())
    # pprint(db.get_riddle_quests())
