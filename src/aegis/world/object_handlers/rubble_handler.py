from typing import override

from aegis.common.world.objects import Rubble, WorldObject
from aegis.parsers.helper.world_file_type import Arguments
from aegis.world.object_handlers.object_handler import ObjectHandler


class RubbleHandler(ObjectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.rb_map: dict[int, Rubble] = {}

    @override
    def get_keys(self) -> list[str]:
        return ["RB", "RUBBLE"]

    @override
    def create_world_object(self, params: dict[Arguments, int]) -> WorldObject | None:
        if len(params) < 2:
            print(
                "WARNING: RubbleHandler: incorrect Parameter setting: missing remove_energy and/or remove_agents"
            )
            return None

        remove_energy = params["remove_energy"]
        remove_agents = params["remove_agents"]
        rubble = Rubble(self.world_object_count, remove_energy, remove_agents)
        self.rb_map[self.world_object_count] = rubble
        self.world_object_count += 1
        return rubble

    @override
    def reset(self) -> None:
        self.rb_map.clear()
