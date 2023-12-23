class Location():
    def __init__(self, data: dict):
        self.name = data.keys()[0]
        self.description = data["description"]
        self.linked_locations = data["linked_locations"]

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

