from world import World


class Player:
    def __init__(self, player_id, transport):
        self.id = player_id
        self.transport = transport
        self.position = World().player_spawn

    def serialize(self):
        return {
            "id": self.id,
            "position": {
                "x": self.position[0],
                "y": self.position[1]
            }
        }
