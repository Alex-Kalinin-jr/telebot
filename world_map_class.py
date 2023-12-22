from db.database import DB

db = DB()

class Location:
    game_locations = db.fill_data('db/locations.json')
    game_enemies = db.fill_data('db/enemies.json')
    game_npcs = db.fill_data('db/npcs.json')

    def __init__(self, key: str):
        data = Location.game_locations[key]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.linked_locations: list[str] = data["linked_locations"]
        self.npc: list[str] = data["npc"]
        self.enemies: list[str] = data["enemies"]
        self.id = key

    def get_linked_locations(self):
        linked_locations = [Location.game_locations[location_key]
                            for location_key in self.linked_locations]
        return linked_locations

    def get_linked_location_id_by_name(self, name):
        for location_key in self.linked_locations:
            if Location.game_locations[location_key]["name"] == name:
                return location_key

    def get_full_npcs_data(self):
        npc_data = [Location.game_npcs[npc_key]
                    for npc_key in self.npc]
        return npc_data

    def get_enemies(self):
        linked_enemies = [{enemy_key : Location.game_enemies[enemy_key]["name"]}
                          for enemy_key in self.enemies]
        return linked_enemies

    def get_full_enemies_data(self):
        linked_enemies = [Location.game_enemies[enemy_key] for enemy_key in self.enemies]
        return linked_enemies

    def get_description(self):
        return self.description

    def get_npcs(self):
        linked_enemies = [{npc_key: Location.game_npcs[npc_key]["name"]}
                          for npc_key in self.npc]
        return linked_enemies

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.description

    def __eq__(self, other):
        if isinstance(other, Location):
            return (self.name == other.name
                    and self.linked_locations == other.linked_locations
                    )

    def __hash__(self):
        return hash((self.name,
                     self.description,
                     self.linked_locations
                     ))

    def __ne__(self, other):
        if isinstance(other, Location):
            return not self.__eq__(other)


if __name__ == "__main__":
    loc = Location("location_1")
    # print(len(loc.get_linked_locations()))
    print(loc.get_npcs())
